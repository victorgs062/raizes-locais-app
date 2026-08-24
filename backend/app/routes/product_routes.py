from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import (
    ProductSchema, ProductListResponseSchema, 
    ProductQueryArgsSchema, ProductUpdateSchema
)
from app.services.product_service import ProductService

product_blp = Blueprint(
    'products', 'products', url_prefix='/api',
    description='Operações no catálogo de produtos'
)

@product_blp.route('/products')
class ProductResource(MethodView):
    @product_blp.arguments(ProductSchema)
    @product_blp.response(201, ProductSchema)
    def post(self, data):
        """Criar um novo anúncio de produto"""
        try:
            return ProductService.create_product(data)
        except Exception as e:
            abort(500, message=f"Falha ao criar produto: {str(e)}")

    @product_blp.arguments(ProductQueryArgsSchema, location="query")
    @product_blp.response(200, ProductListResponseSchema(many=True))
    def get(self, query_args):
        """Obter todos os produtos, opcionalmente ordenados por distância se lat/lng forem fornecidos"""
        user_lat = query_args.get('lat')
        user_lng = query_args.get('lng')
        return ProductService.list_products(user_lat, user_lng)

@product_blp.route('/products/<int:product_id>')
class ProductDetailResource(MethodView):
    @product_blp.response(200, ProductSchema)
    def get(self, product_id):
        """Obter detalhes de um produto específico"""
        product = ProductService.get_product(product_id)
        if not product:
            abort(404, message="Produto não encontrado.")
        return product
        
    @product_blp.arguments(ProductUpdateSchema)
    @product_blp.response(200, ProductSchema)
    def put(self, data, product_id):
        """Atualizar um produto"""
        try:
            product = ProductService.update_product(product_id, data)
            if not product:
                abort(404, message="Produto não encontrado.")
            return product
        except Exception as e:
            abort(500, message=f"Falha ao atualizar produto: {str(e)}")
        
    def delete(self, product_id):
        """Excluir um produto"""
        success = ProductService.delete_product(product_id)
        if success:
            return {'message': 'Produto deletado com sucesso.'}
        abort(404, message="Produto não encontrado.")

@product_blp.route('/products/producer/<int:producer_id>')
class ProducerProducts(MethodView):
    @product_blp.response(200, ProductSchema(many=True))
    def get(self, producer_id):
        """Obter todos os produtos criados por um produtor específico"""
        return ProductService.get_producer_products(producer_id)
