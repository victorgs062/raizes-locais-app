from flask.views import MethodView
from flask_smorest import Blueprint
from app.schemas import CarbonFootprintRequestSchema, CarbonFootprintResponseSchema
from app.utils import calculate_co2_savings

sustainability_blp = Blueprint(
    'sustainability', 'sustainability', url_prefix='/api',
    description='Operações de métricas de sustentabilidade'
)

@sustainability_blp.route('/carbon-footprint')
class CarbonFootprint(MethodView):
    @sustainability_blp.arguments(CarbonFootprintRequestSchema)
    @sustainability_blp.response(200, CarbonFootprintResponseSchema)
    def post(self, data):
        """Calcular a economia de pegada de carbono para uma compra simulada"""
        distance_km = data.get('distance_km')
        weight_kg = data.get('weight_kg', 1.0)
        
        savings = calculate_co2_savings(distance_km, weight_kg)
        
        return {
            'co2_saved_kg': savings,
            'message': f'Você economizou {savings} kg de CO2!'
        }
