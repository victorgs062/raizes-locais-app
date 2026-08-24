import os
import uuid
import base64
from flask import current_app
from app.models import db, Product, User
from app.utils import calculate_distance

class ProductService:
    """
    Serviço para gerenciar o catálogo de produtos e salvamento de imagens.
    """

    @staticmethod
    def _save_image(photo_base64: str) -> str:
        """
        Decodifica e salva a string de imagem em base64 localmente.

        Parâmetros:
        - photo_base64 (str): String com os dados da imagem em base64.

        Retorno:
        - str: URL relativa para a foto salva.

        Exceções:
        - Exception: Se houver erro na decodificação ou salvamento.
        """
        upload_dir = os.path.join(current_app.root_path, 'static', 'products')
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(upload_dir, filename)
        
        with open(filepath, "wb") as fh:
            fh.write(base64.b64decode(photo_base64))
        
        return f"/static/products/{filename}"

    @staticmethod
    def create_product(data: dict) -> Product:
        """
        Cria um novo produto. Se for fornecida uma imagem em base64, salva o arquivo.

        Parâmetros:
        - data (dict): Dados para criação do produto, incluindo foto base64 opcional.

        Retorno:
        - Product: O produto recém criado no banco de dados.
        """
        photo_base64 = data.pop('photo_base64', None)
        new_product = Product(**data)
        
        if photo_base64:
            new_product.photo_url = ProductService._save_image(photo_base64)
                
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def update_product(product_id: int, data: dict) -> Product:
        """
        Atualiza um produto existente.

        Parâmetros:
        - product_id (int): O ID do produto a ser editado.
        - data (dict): Os novos dados.

        Retorno:
        - Product: O produto atualizado, ou None se não for encontrado.
        """
        product = Product.query.get(product_id)
        if not product:
            return None
            
        if 'name' in data: product.name = data['name']
        if 'category' in data: product.category = data['category']
        if 'price' in data: product.price = data['price']
        if 'stock_quantity' in data: product.stock_quantity = data['stock_quantity']
        if 'unit' in data: product.unit = data['unit']
        
        photo_base64 = data.pop('photo_base64', None)
        if photo_base64:
            product.photo_url = ProductService._save_image(photo_base64)
                
        db.session.commit()
        return product

    @staticmethod
    def delete_product(product_id: int) -> bool:
        """
        Deleta um produto específico.

        Parâmetros:
        - product_id (int): O ID do produto a ser deletado.

        Retorno:
        - bool: True se deletado com sucesso, False se o produto não for encontrado.
        """
        product = Product.query.get(product_id)
        if not product:
            return False
            
        db.session.delete(product)
        db.session.commit()
        return True

    @staticmethod
    def get_product(product_id: int) -> Product:
        """Busca um produto pelo ID."""
        return Product.query.get(product_id)

    @staticmethod
    def get_producer_products(producer_id: int) -> list[Product]:
        """Busca todos os produtos cadastrados por um produtor específico."""
        return Product.query.filter_by(producer_id=producer_id).all()

    @staticmethod
    def list_products(user_lat: float = None, user_lng: float = None) -> list[dict]:
        """
        Busca todos os produtos e calcula a distância entre o consumidor (user_lat/user_lng)
        e o produtor de cada produto, opcionalmente ordenando pelo mais próximo.

        Parâmetros:
        - user_lat (float, opcional): Latitude do consumidor.
        - user_lng (float, opcional): Longitude do consumidor.

        Retorno:
        - list[dict]: Lista com dicionários representando cada produto, anexado à 
          distância percorrida e dados básicos do produtor.
        """
        products = Product.query.all()
        results = []
        
        for product in products:
            prod_data = product.to_dict()
            prod_data['created_at'] = product.created_at
            producer = User.query.get(product.producer_id)
            
            prod_data['producer_name'] = producer.name
            prod_data['producer_phone'] = producer.phone
            
            # Se a lat/lng do consumidor for fornecida, calcula a distância
            distance = None
            if user_lat is not None and user_lng is not None and producer.latitude and producer.longitude:
                distance = calculate_distance(user_lat, user_lng, producer.latitude, producer.longitude)
                
            prod_data['distance_km'] = distance
            results.append(prod_data)
            
        # Se havia coordenadas, ordena pela menor distância. 
        # (Produtos sem coordenada conhecida ficam no final do array)
        if user_lat is not None and user_lng is not None:
            results.sort(key=lambda x: (x['distance_km'] is None, x['distance_km']))
            
        return results
