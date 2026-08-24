from app.routes.auth_routes import auth_blp
from app.routes.user_routes import user_blp
from app.routes.product_routes import product_blp
from app.routes.order_routes import order_blp
from app.routes.sustainability_routes import sustainability_blp

def register_blueprints(api):
    """
    Registra todos os blueprints da aplicação no objeto Api do flask_smorest.
    
    Parâmetros:
    - api (flask_smorest.Api): A instância da API do Flask-Smorest.
    """
    api.register_blueprint(auth_blp)
    api.register_blueprint(user_blp)
    api.register_blueprint(product_blp)
    api.register_blueprint(order_blp)
    api.register_blueprint(sustainability_blp)
