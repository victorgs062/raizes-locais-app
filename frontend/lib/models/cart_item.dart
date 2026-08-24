import 'product.dart';

class CartItem {
  final Product product;
  double quantity;

  CartItem({required this.product, required this.quantity});

  Map<String, dynamic> toJson() {
    return {'product_id': product.id, 'quantity': quantity};
  }
}
