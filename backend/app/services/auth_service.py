import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import db, User, ProducerInfo
from app.services.email_service import EmailService

class AuthService:
    """
    Serviço para gerenciar lógica de autenticação, registro e recuperação de senha.
    """

    @staticmethod
    def register_user(data: dict) -> dict:
        """
        Registra um novo usuário (consumidor ou produtor) e cria o token de acesso.

        Parâmetros:
        - data (dict): Dados do usuário validados.

        Retorno:
        - dict: Retorna o usuário criado e o token JWT.
        
        Exceções:
        - ValueError: Se o usuário já existir.
        """
        if User.query.filter_by(email=data['email']).first():
            raise ValueError('User already exists.')
            
        hashed_password = generate_password_hash(data['password'])
        
        new_user = User(
            name=data['name'],
            email=data['email'],
            password_hash=hashed_password,
            role=data['role'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            phone=data.get('phone'),
            address=data.get('address')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Se for produtor, precisamos criar também as informações adicionais
        if data['role'] == 'producer':
            producer_info = ProducerInfo(
                user_id=new_user.id,
                farm_name=data.get('farm_name'),
                cpf_cnpj=data.get('cpf_cnpj'),
                pix_key=data.get('pix_key'),
                cultivation_methods=data.get('cultivation_methods')
            )
            db.session.add(producer_info)
            db.session.commit()
            
        access_token = create_access_token(identity=str(new_user.id))
        return {'user': new_user, 'access_token': access_token}

    @staticmethod
    def login_user(data: dict) -> dict:
        """
        Autentica um usuário usando email e senha.

        Parâmetros:
        - data (dict): Contém 'email' e 'password'.

        Retorno:
        - dict: Retorna o usuário logado e o token JWT.
        
        Exceções:
        - ValueError: Se as credenciais forem inválidas.
        """
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            raise ValueError('Invalid credentials.')
            
        access_token = create_access_token(identity=str(user.id))
        return {'user': user, 'access_token': access_token}

    @staticmethod
    def request_password_reset(email: str) -> None:
        """
        Gera um código de recuperação e envia por e-mail para o usuário.

        Parâmetros:
        - email (str): E-mail do usuário.
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            # Não lança erro para não permitir enumeração de e-mails na API
            return
            
        code = str(random.randint(1000, 9999))
        user.reset_code = code
        user.reset_code_expires_at = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()
        
        EmailService.send_password_reset_email(user.email, code)

    @staticmethod
    def verify_reset_code(email: str, code: str) -> bool:
        """
        Verifica se o código de recuperação enviado é válido.

        Parâmetros:
        - email (str): E-mail do usuário.
        - code (str): Código de 4 dígitos.

        Retorno:
        - bool: True se válido, False caso contrário.
        """
        user = User.query.filter_by(email=email).first()
        if not user or user.reset_code != code or user.reset_code_expires_at < datetime.utcnow():
            return False
        return True

    @staticmethod
    def reset_password(email: str, code: str, new_password: str) -> bool:
        """
        Redefine a senha do usuário, se o código for válido.

        Parâmetros:
        - email (str): E-mail do usuário.
        - code (str): Código de 4 dígitos.
        - new_password (str): A nova senha escolhida pelo usuário.

        Retorno:
        - bool: True se o reset for bem sucedido, False caso o código seja inválido.
        """
        user = User.query.filter_by(email=email).first()
        if not user or user.reset_code != code or user.reset_code_expires_at < datetime.utcnow():
            return False
            
        user.password_hash = generate_password_hash(new_password)
        user.reset_code = None
        user.reset_code_expires_at = None
        db.session.commit()
        
        return True
