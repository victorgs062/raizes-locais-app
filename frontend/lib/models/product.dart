class Product {
  final int id;
  final int producerId;
  final String name;
  final String category;
  final double price;
  final double stockQuantity;
  final String unit;
  final String? photoUrl;
  final String? createdAt;
  final String? producerName;
  final String? producerPhone;
  final double? distanceKm;

  Product({
    required this.id,
    required this.producerId,
    required this.name,
    required this.category,
    required this.price,
    required this.stockQuantity,
    required this.unit,
    this.photoUrl,
    this.createdAt,
    this.producerName,
    this.producerPhone,
    this.distanceKm,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      producerId: json['producer_id'],
      name: json['name'],
      category: json['category'],
      price: (json['price'] as num).toDouble(),
      stockQuantity: (json['stock_quantity'] as num).toDouble(),
      unit: json['unit'],
      photoUrl: json['photo_url'],
      createdAt: json['created_at'],
      producerName: json['producer_name'],
      producerPhone: json['producer_phone'],
      distanceKm: json['distance_km'] != null
          ? (json['distance_km'] as num).toDouble()
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'producer_id': producerId,
      'name': name,
      'category': category,
      'price': price,
      'stock_quantity': stockQuantity,
      'unit': unit,
      'photo_url': photoUrl,
    };
  }
}
