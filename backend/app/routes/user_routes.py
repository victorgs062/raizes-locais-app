from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import UserResponseSchema, UserUpdateSchema
from app.services.user_service import UserService

user_blp = Blueprint(
    'users', 'users', url_prefix='/api',
    description='Operações de perfil e busca de usuários'
)

@user_blp.route('/users/<int:user_id>')
class UserResource(MethodView):
    @user_blp.response(200, UserResponseSchema)
    def get(self, user_id):
        """Obter detalhes do usuário por ID"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            abort(404, message="Usuário não encontrado.")
        return user
        
    @user_blp.arguments(UserUpdateSchema)
    @user_blp.response(200, UserResponseSchema)
    @jwt_required()
    def put(self, data, user_id):
        """Atualizar perfil do usuário"""
        current_user_id = int(get_jwt_identity())
        if current_user_id != user_id:
            abort(403, message="Não autorizado a atualizar este usuário.")
            
        user = UserService.update_user(user_id, data)
        if not user:
            abort(404, message="Usuário não encontrado.")
            
        return user

@user_blp.route('/producers')
class ProducersResource(MethodView):
    @user_blp.response(200, UserResponseSchema(many=True))
    def get(self):
        """Obter todos os produtores (útil para listagens no app)"""
        return UserService.get_all_producers()
