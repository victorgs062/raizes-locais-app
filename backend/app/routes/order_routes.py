from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import OrderSchema, OrderCreateSchema, OrderStatusUpdateSchema
from app.services.order_service import OrderService

order_blp = Blueprint(
    'orders', 'orders', url_prefix='/api',
    description='Operações de pedidos e checkout'
)

@order_blp.route('/orders')
class OrderResource(MethodView):
    @order_blp.arguments(OrderCreateSchema)
    @order_blp.response(201, OrderSchema(many=True))
    @jwt_required()
    def post(self, data):
        """Finalizar carrinho e criar pedidos (um por produtor)"""
        consumer_id = data['consumer_id']
        current_user_id = int(get_jwt_identity())
        
        if current_user_id != consumer_id:
            abort(403, message="Não autorizado a criar pedido para este usuário.")
            
        try:
            return OrderService.create_checkout(consumer_id, data['items'])
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message="Erro interno ao processar o pedido.")

@order_blp.route('/orders/user/<int:user_id>')
class UserOrdersResource(MethodView):
    @order_blp.response(200, OrderSchema(many=True))
    @jwt_required()
    def get(self, user_id):
        """Obter todos os pedidos onde o usuário é consumidor ou produtor"""
        current_user_id = int(get_jwt_identity())
        if current_user_id != user_id:
            abort(403, message="Não autorizado a ver os pedidos deste usuário.")
            
        return OrderService.get_user_orders(user_id)

@order_blp.route('/orders/<int:order_id>/status')
class OrderStatusResource(MethodView):
    @order_blp.arguments(OrderStatusUpdateSchema)
    @order_blp.response(200, OrderSchema)
    @jwt_required()
    def put(self, data, order_id):
        """Atualizar o status de um pedido"""
        current_user_id = int(get_jwt_identity())
        
        try:
            return OrderService.update_order_status(order_id, data['status'], current_user_id)
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message="Erro ao atualizar status.")
