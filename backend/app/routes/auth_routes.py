from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import (
    UserRegisterSchema, UserLoginSchema, UserLoginResponseSchema, 
    ForgotPasswordSchema, VerifyCodeSchema, ResetPasswordSchema
)
from app.services.auth_service import AuthService

auth_blp = Blueprint(
    'auth', 'auth', url_prefix='/api',
    description='Operações de autenticação e registro'
)

@auth_blp.route('/register')
class Register(MethodView):
    @auth_blp.arguments(UserRegisterSchema)
    @auth_blp.response(201, UserLoginResponseSchema)
    def post(self, data):
        """Registrar um novo usuário (produtor ou consumidor)"""
        try:
            return AuthService.register_user(data)
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message="Erro interno ao registrar usuário.")

@auth_blp.route('/login')
class Login(MethodView):
    @auth_blp.arguments(UserLoginSchema)
    @auth_blp.response(200, UserLoginResponseSchema)
    def post(self, data):
        """Autenticar um usuário"""
        try:
            return AuthService.login_user(data)
        except ValueError as e:
            abort(401, message=str(e))

@auth_blp.route('/password/forgot')
class ForgotPassword(MethodView):
    @auth_blp.arguments(ForgotPasswordSchema)
    def post(self, data):
        """Solicitar um código de recuperação de senha enviado para o email"""
        try:
            AuthService.request_password_reset(data['email'])
            # Retorna 200 independente do usuário existir ou não (segurança contra enumeração)
            return {'message': 'Se o email existir, um código foi enviado.'}
        except Exception as e:
            abort(500, message=str(e))

@auth_blp.route('/password/verify')
class VerifyCode(MethodView):
    @auth_blp.arguments(VerifyCodeSchema)
    def post(self, data):
        """Verificar o código de 4 dígitos"""
        if AuthService.verify_reset_code(data['email'], data['code']):
            return {'message': 'Código verificado com sucesso.'}
        abort(400, message='Código inválido ou expirado.')

@auth_blp.route('/password/reset')
class ResetPassword(MethodView):
    @auth_blp.arguments(ResetPasswordSchema)
    def post(self, data):
        """Redefinir a senha usando o código"""
        success = AuthService.reset_password(data['email'], data['code'], data['new_password'])
        if success:
            return {'message': 'Senha alterada com sucesso.'}
        abort(400, message='Código inválido ou expirado.')
