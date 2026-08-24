import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';

import '../models/product.dart';
import '../providers/cart_provider.dart';
import '../services/api_service.dart';
import '../utils/currency_format.dart';
import '../utils/app_theme.dart';

class ProductDetailsSheet extends StatefulWidget {
  final Product product;

  const ProductDetailsSheet({super.key, required this.product});

  @override
  State<ProductDetailsSheet> createState() => _ProductDetailsSheetState();
}

class _ProductDetailsSheetState extends State<ProductDetailsSheet> {
  late double quantity;
  late double step;

  @override
  void initState() {
    super.initState();
    step = widget.product.unit == "kg" ? 0.5 : 1.0;
    quantity = step;
  }

  Future<void> _launchWhatsApp() async {
    if (widget.product.producerPhone == null ||
        widget.product.producerPhone!.isEmpty)
      return;
    final phone = widget.product.producerPhone!.replaceAll(RegExp(r'\D'), '');
    final url = Uri.parse('https://wa.me/55$phone');
    if (!await launchUrl(url, mode: LaunchMode.externalApplication)) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Não foi possível abrir o WhatsApp.'),
            backgroundColor: AppTheme.errorColor,
          ),
        );
      }
    }
  }

  void _addToCart() {
    Provider.of<CartProvider>(
      context,
      listen: false,
    ).addItem(widget.product, quantity);
    Navigator.pop(context);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          '${quantity.toStringAsFixed(widget.product.unit == "kg" ? 1 : 0)}x ${widget.product.name} adicionado ao carrinho!',
        ),
        backgroundColor: AppTheme.primaryColor,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          if (widget.product.photoUrl != null)
            ClipRRect(
              borderRadius: BorderRadius.circular(15),
              child: Image.network(
                '${ApiService.hostUrl}${widget.product.photoUrl}',
                height: 200,
                fit: BoxFit.cover,
                errorBuilder: (c, e, s) =>
                    const Icon(Icons.broken_image, size: 100),
              ),
            ),
          const SizedBox(height: 16),
          Text(
            widget.product.name,
            style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                '${CurrencyFormat.format(widget.product.price)} / ${widget.product.unit}',
                style: const TextStyle(
                  fontSize: 20,
                  color: AppTheme.primaryColor,
                  fontWeight: FontWeight.bold,
                ),
              ),
              if (widget.product.distanceKm != null)
                Chip(
                  avatar: const Icon(
                    Icons.location_on,
                    size: 16,
                    color: Colors.white,
                  ),
                  label: Text(
                    '${widget.product.distanceKm!.toStringAsFixed(1)} km',
                    style: const TextStyle(color: Colors.white),
                  ),
                  backgroundColor: AppTheme.primaryColor,
                ),
            ],
          ),
          const SizedBox(height: 16),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: const CircleAvatar(
              backgroundColor: AppTheme.primaryColor,
              child: Icon(Icons.person, color: Colors.white),
            ),
            title: const Text('Produtor'),
            subtitle: Text(widget.product.producerName ?? "Desconhecido"),
          ),
          const Divider(),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              IconButton(
                icon: const Icon(
                  Icons.remove_circle_outline,
                  color: AppTheme.primaryColor,
                  size: 32,
                ),
                onPressed: () {
                  if (quantity > step) {
                    setState(() => quantity -= step);
                  }
                },
              ),
              const SizedBox(width: 16),
              Text(
                '${quantity.toStringAsFixed(widget.product.unit == "kg" ? 1 : 0)} ${widget.product.unit}',
                style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(width: 16),
              IconButton(
                icon: Icon(
                  Icons.add_circle_outline,
                  color: quantity < widget.product.stockQuantity
                      ? AppTheme.primaryColor
                      : Colors.grey,
                  size: 32,
                ),
                onPressed: () {
                  if (quantity + step <= widget.product.stockQuantity) {
                    setState(() => quantity += step);
                  } else if (quantity < widget.product.stockQuantity) {
                    setState(() => quantity = widget.product.stockQuantity);
                  }
                },
              ),
            ],
          ),
          const SizedBox(height: 16),
          ElevatedButton.icon(
            icon: const Icon(Icons.shopping_cart),
            label: const Text(
              'Adicionar ao Carrinho',
              style: TextStyle(fontSize: 16),
            ),
            onPressed: quantity <= widget.product.stockQuantity
                ? _addToCart
                : null,
          ),
          const SizedBox(height: 8),
          if (widget.product.producerPhone != null &&
              widget.product.producerPhone!.isNotEmpty)
            OutlinedButton.icon(
              icon: const Icon(Icons.chat),
              label: const Text(
                'Conversar com o vendedor',
                style: TextStyle(fontSize: 16),
              ),
              onPressed: _launchWhatsApp,
            ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }
}
