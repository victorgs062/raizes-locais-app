import 'product.dart';

class OrderItem {
  final int id;
  final int productId;
  final double quantity;
  final double unitPrice;
  final Product? product;

  OrderItem({
    required this.id,
    required this.productId,
    required this.quantity,
    required this.unitPrice,
    this.product,
  });

  factory OrderItem.fromJson(Map<String, dynamic> json) {
    return OrderItem(
      id: json['id'] ?? 0,
      productId: json['product_id'],
      quantity: (json['quantity'] as num).toDouble(),
      unitPrice: (json['unit_price'] as num).toDouble(),
      product: json['product'] != null
          ? Product.fromJson(json['product'])
          : null,
    );
  }
}

class Order {
  final int id;
  final int consumerId;
  final int producerId;
  final String status;
  final double totalPrice;
  final String? createdAt;
  final List<OrderItem> items;

  final String? producerName;
  final String? producerPhone;
  final String? producerAddress;
  final double? producerLatitude;
  final double? producerLongitude;
  final String? consumerName;
  final String? consumerPhone;

  Order({
    required this.id,
    required this.consumerId,
    required this.producerId,
    required this.status,
    required this.totalPrice,
    this.createdAt,
    this.items = const [],
    this.producerName,
    this.producerPhone,
    this.producerAddress,
    this.producerLatitude,
    this.producerLongitude,
    this.consumerName,
    this.consumerPhone,
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
      id: json['id'] ?? 0,
      consumerId: json['consumer_id'] ?? 0,
      producerId: json['producer_id'] ?? 0,
      status: json['status'] ?? '',
      totalPrice: (json['total_price'] as num).toDouble(),
      createdAt: json['created_at'],
      items: json['items'] != null
          ? (json['items'] as List).map((i) => OrderItem.fromJson(i)).toList()
          : [],
      producerName: json['producer_name'],
      producerPhone: json['producer_phone'],
      producerAddress: json['producer_address'],
      producerLatitude: json['producer_latitude'] != null
          ? (json['producer_latitude'] as num).toDouble()
          : null,
      producerLongitude: json['producer_longitude'] != null
          ? (json['producer_longitude'] as num).toDouble()
          : null,
      consumerName: json['consumer_name'],
      consumerPhone: json['consumer_phone'],
    );
  }
}
