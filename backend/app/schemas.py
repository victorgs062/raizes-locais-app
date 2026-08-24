from marshmallow import Schema, fields, validate

class ProducerInfoSchema(Schema):
    farm_name = fields.Str()
    cpf_cnpj = fields.Str()
    pix_key = fields.Str()
    cultivation_methods = fields.Str()

class UserRegisterSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(required=True) # 'producer' or 'consumer'
    latitude = fields.Float(allow_none=True)
    longitude = fields.Float(allow_none=True)
    phone = fields.Str(allow_none=True)
    address = fields.Str(allow_none=True)
    farm_name = fields.Str(allow_none=True)
    cpf_cnpj = fields.Str(allow_none=True)
    pix_key = fields.Str(allow_none=True)
    cultivation_methods = fields.Str(allow_none=True)

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class UserResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Email()
    role = fields.Str()
    latitude = fields.Float(allow_none=True)
    longitude = fields.Float(allow_none=True)
    phone = fields.Str(allow_none=True)
    address = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    producer_info = fields.Nested(ProducerInfoSchema, dump_only=True)

class UserUpdateSchema(Schema):
    name = fields.Str(allow_none=True)
    email = fields.Email(allow_none=True)
    phone = fields.Str(allow_none=True)
    address = fields.Str(allow_none=True)
    latitude = fields.Float(allow_none=True)
    longitude = fields.Float(allow_none=True)
    farm_name = fields.Str(allow_none=True)
    cpf_cnpj = fields.Str(allow_none=True)
    pix_key = fields.Str(allow_none=True)
    cultivation_methods = fields.Str(allow_none=True)

class UserLoginResponseSchema(Schema):
    message = fields.Str()
    user = fields.Nested(UserResponseSchema)
    access_token = fields.Str()

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    producer_id = fields.Int(required=True)
    name = fields.Str(required=True)
    category = fields.Str(load_default="Outros")
    price = fields.Float(required=True)
    stock_quantity = fields.Float(load_default=0.0)
    unit = fields.Str(load_default="un")
    photo_url = fields.Str(dump_only=True)
    photo_base64 = fields.Str(load_only=True)
    created_at = fields.DateTime(dump_only=True)

class ProductUpdateSchema(Schema):
    name = fields.Str()
    category = fields.Str()
    price = fields.Float()
    stock_quantity = fields.Float()
    unit = fields.Str()
    photo_base64 = fields.Str(load_only=True)

class ProductListResponseSchema(ProductSchema):
    producer_name = fields.Str(dump_only=True, allow_none=True)
    producer_phone = fields.Str(dump_only=True, allow_none=True)
    distance_km = fields.Float(dump_only=True, allow_none=True)

class ProductQueryArgsSchema(Schema):
    lat = fields.Float()
    lng = fields.Float()

class CarbonFootprintRequestSchema(Schema):
    distance_km = fields.Float(required=True)
    weight_kg = fields.Float(load_default=1.0)

class CarbonFootprintResponseSchema(Schema):
    co2_saved_kg = fields.Float()
    message = fields.Str()

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity = fields.Float(required=True)
    unit_price = fields.Float(dump_only=True)
    product = fields.Nested(ProductSchema, dump_only=True)

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    consumer_id = fields.Int(dump_only=True)
    producer_id = fields.Int(dump_only=True)
    status = fields.Str(dump_only=True)
    total_price = fields.Float(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    items = fields.List(fields.Nested(OrderItemSchema), dump_only=True)
    
    # Extra fields for ease of display
    producer_name = fields.Str(dump_only=True, allow_none=True)
    producer_phone = fields.Str(dump_only=True, allow_none=True)
    producer_address = fields.Str(dump_only=True, allow_none=True)
    producer_latitude = fields.Float(dump_only=True, allow_none=True)
    producer_longitude = fields.Float(dump_only=True, allow_none=True)
    consumer_name = fields.Str(dump_only=True, allow_none=True)
    consumer_phone = fields.Str(dump_only=True, allow_none=True)

class CartItemSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Float(required=True)

class OrderCreateSchema(Schema):
    consumer_id = fields.Int(required=True)
    items = fields.List(fields.Nested(CartItemSchema), required=True)

class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True)

class VerifyCodeSchema(Schema):
    email = fields.Email(required=True)
    code = fields.Str(required=True)

class ResetPasswordSchema(Schema):
    email = fields.Email(required=True)
    code = fields.Str(required=True)
    new_password = fields.Str(required=True)

class OrderStatusUpdateSchema(Schema):
    status = fields.Str(required=True, validate=validate.OneOf(['Pendente', 'Pronto para Retirada', 'Concluído', 'Cancelado']))
