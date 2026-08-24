from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'producer' or 'consumer'
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    phone = db.Column(db.String(20), nullable=True) # WhatsApp number
    address = db.Column(db.String(255), nullable=True)
    reset_code = db.Column(db.String(4), nullable=True)
    reset_code_expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    producer_info = db.relationship('ProducerInfo', backref='user', uselist=False, cascade="all, delete-orphan")
    products = db.relationship('Product', backref='producer', lazy=True, cascade="all, delete-orphan")
    orders_as_consumer = db.relationship('Order', foreign_keys='Order.consumer_id', backref='consumer', lazy=True, cascade="all, delete-orphan")
    orders_as_producer = db.relationship('Order', foreign_keys='Order.producer_id', backref='producer', lazy=True, cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        """
        Converte a instância do usuário para um dicionário serializável.
        
        Retorno:
        - dict: Dicionário contendo os dados do usuário.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ProducerInfo(db.Model):
    __tablename__ = 'producers_info'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farm_name = db.Column(db.String(150), nullable=True)
    cpf_cnpj = db.Column(db.String(20), nullable=True)
    pix_key = db.Column(db.String(100), nullable=True)
    cultivation_methods = db.Column(db.String(200), nullable=True) # e.g. "Organico, Agrossilvicultura"

    def to_dict(self) -> dict:
        """
        Converte as informações do produtor para um dicionário.
        
        Retorno:
        - dict: Dicionário contendo os dados da fazenda/produtor.
        """
        return {
            'farm_name': self.farm_name,
            'cpf_cnpj': self.cpf_cnpj,
            'pix_key': self.pix_key,
            'cultivation_methods': self.cultivation_methods
        }

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False) # 'kg', 'unidade', 'maço'
    photo_url = db.Column(db.String(255), nullable=True) # URL to photo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """
        Converte o produto para um dicionário.
        
        Retorno:
        - dict: Dicionário contendo os dados do produto.
        """
        return {
            'id': self.id,
            'producer_id': self.producer_id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'stock_quantity': self.stock_quantity,
            'unit': self.unit,
            'photo_url': self.photo_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    consumer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    producer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='Pendente') # Pendente, Concluído, Cancelado
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        """
        Converte a instância do pedido para um dicionário.
        
        Retorno:
        - dict: Dicionário contendo os dados do pedido.
        """
        return {
            'id': self.id,
            'consumer_id': self.consumer_id,
            'producer_id': self.producer_id,
            'status': self.status,
            'total_price': self.total_price,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    product = db.relationship('Product')

    def to_dict(self) -> dict:
        """
        Converte o item do pedido para um dicionário.
        
        Retorno:
        - dict: Dicionário contendo os dados do item.
        """
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'unit_price': self.unit_price
        }
