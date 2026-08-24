from app.models import db, User

class UserService:
    """
    Serviço para gerenciar os dados de perfil dos usuários.
    """

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """
        Busca um usuário pelo seu ID.

        Parâmetros:
        - user_id (int): ID do usuário a buscar.

        Retorno:
        - User: Instância do usuário, caso exista. Retorna None caso contrário.
        """
        return User.query.get(user_id)

    @staticmethod
    def update_user(user_id: int, data: dict) -> User:
        """
        Atualiza as informações de perfil do usuário.

        Parâmetros:
        - user_id (int): ID do usuário a atualizar.
        - data (dict): Dicionário contendo os campos a serem atualizados.

        Retorno:
        - User: O usuário atualizado.
        """
        user = User.query.get(user_id)
        if not user:
            return None
        
        # Atualiza campos base
        if 'name' in data: user.name = data['name']
        if 'email' in data: user.email = data['email']
        if 'phone' in data: user.phone = data['phone']
        if 'address' in data: user.address = data['address']
        if 'latitude' in data: user.latitude = data['latitude']
        if 'longitude' in data: user.longitude = data['longitude']
        
        # Atualiza campos específicos do produtor
        if user.role == 'producer' and user.producer_info:
            if 'farm_name' in data: user.producer_info.farm_name = data['farm_name']
            if 'cpf_cnpj' in data: user.producer_info.cpf_cnpj = data['cpf_cnpj']
            if 'pix_key' in data: user.producer_info.pix_key = data['pix_key']
            if 'cultivation_methods' in data: user.producer_info.cultivation_methods = data['cultivation_methods']
            
        db.session.commit()
        return user

    @staticmethod
    def get_all_producers() -> list[User]:
        """
        Busca todos os usuários com o perfil 'producer'.

        Retorno:
        - list: Uma lista de objetos User que são produtores.
        """
        return User.query.filter_by(role='producer').all()
