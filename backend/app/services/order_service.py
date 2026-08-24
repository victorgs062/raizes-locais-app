from app.models import db, Order, OrderItem, Product, User

class OrderService:
    """
    Serviço para gerenciamento do ciclo de vida dos pedidos, 
    como checagem de estoque e atualização de status.
    """

    @staticmethod
    def create_checkout(consumer_id: int, items_data: list[dict]) -> list[Order]:
        """
        Recebe um carrinho de compras e cria os pedidos agrupando por produtor.
        Desconta a quantidade comprada do estoque.

        Parâmetros:
        - consumer_id (int): O ID do usuário consumidor.
        - items_data (list): A lista de dicionários com 'product_id' e 'quantity'.

        Retorno:
        - list[Order]: Uma lista contendo os pedidos criados (um por produtor).

        Exceções:
        - ValueError: Se o carrinho estiver vazio, se um produto não for encontrado,
          ou se não houver estoque suficiente.
        """
        if not items_data:
            raise ValueError("Cart is empty")
            
        # Agrupa itens do carrinho por produtor. 
        # Um cliente pode comprar de múltiplos produtores ao mesmo tempo, 
        # mas geramos um pedido distinto para cada produtor para facilitar a gestão.
        producer_items = {}
        for item_data in items_data:
            product = Product.query.get(item_data['product_id'])
            if not product:
                raise ValueError(f"Product {item_data['product_id']} not found")
                
            if product.producer_id not in producer_items:
                producer_items[product.producer_id] = []
                
            producer_items[product.producer_id].append({
                'product': product,
                'quantity': item_data['quantity']
            })
            
        created_orders = []
        for producer_id, p_items in producer_items.items():
            # Soma do total deste pedido específico do produtor
            total_price = sum(i['product'].price * i['quantity'] for i in p_items)
            
            order = Order(
                consumer_id=consumer_id,
                producer_id=producer_id,
                status='Pendente',
                total_price=total_price
            )
            db.session.add(order)
            db.session.flush() # Flush garante que o order.id é gerado para uso no OrderItem
            
            for i in p_items:
                product = i['product']
                quantity = i['quantity']
                
                # Regra de Negócio Crítica: Impedir vendas caso não haja estoque
                if product.stock_quantity < quantity:
                    db.session.rollback() # Previne estados inconsistentes no banco
                    raise ValueError(f"Estoque insuficiente para {product.name}")
                    
                # Deduz a quantidade vendida do estoque do produto
                product.stock_quantity -= quantity
                
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.price
                )
                db.session.add(order_item)
                
            created_orders.append(order)
            
        # Confirma as alterações (criação das ordens, itens e desconto em estoque) todas juntas
        db.session.commit()
        
        # Enriquecendo o retorno com campos que os schemas esperam, para compatibilidade
        for order in created_orders:
            OrderService._enrich_order(order)
            
        return created_orders

    @staticmethod
    def get_user_orders(user_id: int) -> list[Order]:
        """
        Retorna todos os pedidos vinculados a um usuário, independentemente 
        deste ser consumidor ou produtor no pedido.

        Parâmetros:
        - user_id (int): ID do usuário logado.

        Retorno:
        - list[Order]: Lista de pedidos com ordenação do mais recente ao mais antigo.
        """
        user = User.query.get(user_id)
        if not user:
            return []
            
        if user.role == 'consumer':
            orders = Order.query.filter_by(consumer_id=user_id).order_by(Order.created_at.desc()).all()
        else:
            orders = Order.query.filter_by(producer_id=user_id).order_by(Order.created_at.desc()).all()
            
        for order in orders:
            OrderService._enrich_order(order)
            
        return orders

    @staticmethod
    def update_order_status(order_id: int, new_status: str, producer_id: int) -> Order:
        """
        Atualiza o status de um pedido e realiza as lógicas colaterais (como devolução de estoque).

        Parâmetros:
        - order_id (int): O ID do pedido.
        - new_status (str): O novo status que será aplicado ('Cancelado', 'Concluído', etc.).
        - producer_id (int): ID do produtor solicitando a alteração. Apenas ele pode modificar.

        Retorno:
        - Order: O pedido atualizado.

        Exceções:
        - ValueError Se o pedido não existir ou o produtor não for autorizado.
        """
        order = Order.query.get(order_id)
        if not order:
            raise ValueError("Order not found")
            
        if producer_id != order.producer_id:
            raise ValueError("Only the producer can update the order status")
            
        old_status = order.status
        
        # Se um pedido é cancelado, os itens deverão retornar para o estoque disponível
        if new_status == 'Cancelado' and old_status != 'Cancelado':
            for item in order.items:
                product = Product.query.get(item.product_id)
                if product:
                    product.stock_quantity += item.quantity
        
        order.status = new_status
        db.session.commit()
        
        OrderService._enrich_order(order)
        return order

    @staticmethod
    def _enrich_order(order: Order) -> None:
        """
        Função auxiliar para adicionar os atributos que o Schema necessita 
        para visualização sem precisar de um complexo Join na query inicial.
        """
        order.producer_name = order.producer.name if order.producer else ''
        order.producer_phone = order.producer.phone if order.producer else ''
        order.producer_address = order.producer.address if order.producer else ''
        order.producer_latitude = order.producer.latitude if order.producer else None
        order.producer_longitude = order.producer.longitude if order.producer else None
        
        order.consumer_name = order.consumer.name if order.consumer else ''
        order.consumer_phone = order.consumer.phone if order.consumer else ''
