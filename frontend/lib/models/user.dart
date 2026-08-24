class User {
  final int id;
  final String name;
  final String email;
  final String role;
  final double? latitude;
  final double? longitude;
  final String? phone;
  final String? address;
  final String? createdAt;
  final ProducerInfo? producerInfo;

  User({
    required this.id,
    required this.name,
    required this.email,
    required this.role,
    this.latitude,
    this.longitude,
    this.phone,
    this.address,
    this.createdAt,
    this.producerInfo,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      name: json['name'],
      email: json['email'],
      role: json['role'],
      latitude: json['latitude'] != null
          ? (json['latitude'] as num).toDouble()
          : null,
      longitude: json['longitude'] != null
          ? (json['longitude'] as num).toDouble()
          : null,
      phone: json['phone'],
      address: json['address'],
      createdAt: json['created_at'],
      producerInfo: json['producer_info'] != null
          ? ProducerInfo.fromJson(json['producer_info'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'role': role,
      'latitude': latitude,
      'longitude': longitude,
      'phone': phone,
      'address': address,
      'created_at': createdAt,
      'producer_info': producerInfo?.toJson(),
    };
  }
}

class ProducerInfo {
  final String? farmName;
  final String? cpfCnpj;
  final String? pixKey;
  final String? cultivationMethods;

  ProducerInfo({
    this.farmName,
    this.cpfCnpj,
    this.pixKey,
    this.cultivationMethods,
  });

  factory ProducerInfo.fromJson(Map<String, dynamic> json) {
    return ProducerInfo(
      farmName: json['farm_name'],
      cpfCnpj: json['cpf_cnpj'],
      pixKey: json['pix_key'],
      cultivationMethods: json['cultivation_methods'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'farm_name': farmName,
      'cpf_cnpj': cpfCnpj,
      'pix_key': pixKey,
      'cultivation_methods': cultivationMethods,
    };
  }
}
