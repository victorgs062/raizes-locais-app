import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

import '../models/user.dart';
import '../models/product.dart';
import '../models/order.dart';
import '../models/cart_item.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  static const String hostUrl = kIsWeb
      ? 'http://localhost:5000'
      : 'http://10.1.1.125:5000';
  static const String baseUrl = '$hostUrl/api';
  String? token;

  Map<String, String> get _headers {
    final headers = {'Content-Type': 'application/json'};
    if (token != null) {
      headers['Authorization'] = 'Bearer $token';
    }
    return headers;
  }

  /// Realiza o login do usuário na API.
  ///
  /// Parâmetros:
  /// - [email]: E-mail do usuário.
  /// - [password]: Senha do usuário.
  ///
  /// Retorna: Um objeto [User] se o login for bem-sucedido, caso contrário `null`.
  Future<User?> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'password': password}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        token = data['access_token'];
        return User.fromJson(data['user']);
      }
    } catch (e) {
      debugPrint('Erro no login: $e');
    }
    return null;
  }

  /// Registra um novo usuário (consumidor ou produtor).
  ///
  /// Parâmetros:
  /// - [userData]: Um mapa contendo os dados de registro (nome, email, senha, role, etc).
  ///
  /// Retorna: Um objeto [User] criado se o registro for bem-sucedido, `null` caso contrário.
  Future<User?> register(Map<String, dynamic> userData) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(userData),
      );

      if (response.statusCode == 201) {
        final data = jsonDecode(response.body);
        token = data['access_token'];
        return User.fromJson(data['user']);
      }
    } catch (e) {
      debugPrint('Erro no registro: $e');
    }
    return null;
  }

  /// Busca os detalhes de um usuário específico pelo ID.
  Future<User?> getUser(int id) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/users/$id'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        return User.fromJson(jsonDecode(response.body));
      }
    } catch (e) {
      debugPrint('Erro ao buscar usuário: $e');
    }
    return null;
  }

  /// Busca todos os usuários com o perfil de produtor.
  Future<List<User>> getProducers() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/producers'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => User.fromJson(json)).toList();
      }
    } catch (e) {
      debugPrint('Erro ao buscar produtores: $e');
    }
    return [];
  }

  /// Busca o catálogo completo de produtos.
  ///
  /// Parâmetros opcionais:
  /// - [lat], [lng]: Coordenadas do usuário para ordenar os resultados por distância.
  Future<List<Product>> getProducts({double? lat, double? lng}) async {
    String url = '$baseUrl/products';
    if (lat != null && lng != null) {
      url += '?lat=$lat&lng=$lng';
    }

    try {
      final response = await http.get(Uri.parse(url), headers: _headers);
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Product.fromJson(json)).toList();
      }
    } catch (e) {
      debugPrint('Erro ao buscar produtos: $e');
    }
    return [];
  }

  /// Busca os produtos vinculados a um produtor específico.
  Future<List<Product>> getProducerProducts(int producerId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/products/producer/$producerId'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Product.fromJson(json)).toList();
      }
    } catch (e) {
      debugPrint('Erro ao buscar produtos do produtor: $e');
    }
    return [];
  }

  /// Cria um novo produto (apenas para usuários com role 'producer').
  Future<Product?> addProduct(Map<String, dynamic> productData) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/products'),
        headers: _headers,
        body: jsonEncode(productData),
      );
      if (response.statusCode == 201) {
        return Product.fromJson(jsonDecode(response.body));
      }
    } catch (e) {
      debugPrint('Erro ao adicionar produto: $e');
    }
    return null;
  }

  /// Atualiza os dados de um produto existente.
  Future<Product?> updateProduct(
    int productId,
    Map<String, dynamic> productData,
  ) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/products/$productId'),
        headers: _headers,
        body: jsonEncode(productData),
      );
      if (response.statusCode == 200) {
        return Product.fromJson(jsonDecode(response.body));
      }
    } catch (e) {
      debugPrint('Erro ao atualizar produto: $e');
    }
    return null;
  }

  /// Exclui um produto do banco de dados.
  Future<bool> deleteProduct(int productId) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/products/$productId'),
        headers: _headers,
      );
      return response.statusCode == 200;
    } catch (e) {
      debugPrint('Erro ao excluir produto: $e');
      return false;
    }
  }

  /// Calcula a economia de pegada de carbono baseada na distância até o produtor.
  Future<Map<String, dynamic>?> calculateCarbonFootprint(
    double distanceKm,
    double weightKg,
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/carbon-footprint'),
        headers: _headers,
        body: jsonEncode({'distance_km': distanceKm, 'weight_kg': weightKg}),
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (e) {
      debugPrint('Erro ao calcular pegada de carbono: $e');
    }
    return null;
  }

  /// Atualiza o perfil de um usuário logado.
  Future<User?> updateUser(int id, Map<String, dynamic> data) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/users/$id'),
        headers: _headers,
        body: jsonEncode(data),
      );
      if (response.statusCode == 200) {
        return User.fromJson(jsonDecode(response.body));
      }
    } catch (e) {
      debugPrint('Erro ao atualizar perfil do usuário: $e');
    }
    return null;
  }

  /// Busca o histórico de pedidos vinculados a um usuário (consumidor ou produtor).
  Future<List<Order>> getUserOrders(int userId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/orders/user/$userId'),
        headers: _headers,
      );
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Order.fromJson(json)).toList();
      }
    } catch (e) {
      debugPrint('Erro ao buscar pedidos do usuário: $e');
    }
    return [];
  }

  /// Atualiza o status de um pedido (apenas produtor).
  Future<bool> updateOrderStatus(int orderId, String status) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/orders/$orderId/status'),
        headers: _headers,
        body: jsonEncode({'status': status}),
      );
      return response.statusCode == 200;
    } catch (e) {
      debugPrint('Erro ao atualizar status do pedido: $e');
      return false;
    }
  }

  /// Envia um carrinho de compras para criar os pedidos correspondentes.
  Future<List<Order>?> checkout(int consumerId, List<CartItem> items) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/orders'),
        headers: _headers,
        body: jsonEncode({
          'consumer_id': consumerId,
          'items': items.map((i) => i.toJson()).toList(),
        }),
      );
      if (response.statusCode == 201) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Order.fromJson(json)).toList();
      }
    } catch (e) {
      debugPrint('Erro durante checkout: $e');
    }
    return null;
  }

  /// Solicita o envio de um e-mail de recuperação de senha.
  Future<Map<String, dynamic>?> forgotPassword(String email) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/password/forgot'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email}),
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (e) {
      debugPrint('Erro ao solicitar reset de senha: $e');
    }
    return null;
  }

  /// Verifica se o código de 4 dígitos enviado por e-mail é válido.
  Future<bool> verifyResetCode(String email, String code) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/password/verify'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'code': code}),
      );
      return response.statusCode == 200;
    } catch (e) {
      debugPrint('Erro ao verificar código: $e');
      return false;
    }
  }

  /// Confirma a troca de senha usando o código verificado.
  Future<bool> resetPassword(
    String email,
    String code,
    String newPassword,
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/password/reset'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': email,
          'code': code,
          'new_password': newPassword,
        }),
      );
      return response.statusCode == 200;
    } catch (e) {
      debugPrint('Erro ao redefinir senha: $e');
      return false;
    }
  }
}
