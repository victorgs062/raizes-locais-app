import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave_secreta_padrao'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'chave_jwt_super_secreta'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@localhost:3306/raizes_locais'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAPI / Swagger config
    API_TITLE = "Raízes Locais API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
