import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../models/order.dart';
import '../utils/currency_format.dart';
import '../utils/app_theme.dart';

class OrderCard extends StatelessWidget {
  final Order order;
  final bool isProducer;
  final Function(Order, String) onUpdateStatus;

  const OrderCard({
    super.key,
    required this.order,
    required this.isProducer,
    required this.onUpdateStatus,
  });

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'pendente':
        return AppTheme.warningColor;
      case 'pronto para retirada':
        return AppTheme.infoColor;
      case 'concluído':
        return AppTheme.primaryColor;
      case 'cancelado':
        return AppTheme.errorColor;
      default:
        return Colors.grey;
    }
  }

  Future<void> _launchMapsUrl(
    BuildContext context,
    double lat,
    double lng,
  ) async {
    final Uri url = Uri.parse(
      'https://www.google.com/maps/search/?api=1&query=$lat,$lng',
    );
    if (!await launchUrl(url, mode: LaunchMode.externalApplication)) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Não foi possível abrir o mapa.'),
            backgroundColor: AppTheme.errorColor,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      elevation: 4,
      shadowColor: Colors.black12,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      child: ExpansionTile(
        shape: const Border(),
        leading: CircleAvatar(
          backgroundColor: AppTheme.primaryColor.withOpacity(0.1),
          child: Icon(
            isProducer ? Icons.local_shipping : Icons.shopping_bag,
            color: AppTheme.primaryColor,
          ),
        ),
        title: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              'Pedido #${order.id}',
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
            if (!isProducer)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: _getStatusColor(order.status).withOpacity(0.1),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: _getStatusColor(order.status)),
                ),
                child: Text(
                  order.status,
                  style: TextStyle(
                    color: _getStatusColor(order.status),
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
          ],
        ),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 4.0),
          child: Text(
            'Total: ${CurrencyFormat.format(order.totalPrice)}\n'
            '${isProducer ? "Comprador: ${order.consumerName}" : "Produtor: ${order.producerName}"}',
            style: TextStyle(color: Colors.grey[700]),
          ),
        ),
        children: [
          Container(
            padding: const EdgeInsets.all(16.0),
            decoration: BoxDecoration(
              color: Colors.grey[50],
              borderRadius: const BorderRadius.vertical(
                bottom: Radius.circular(15),
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (isProducer) ...[
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Status do Pedido:',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      DropdownButton<String>(
                        value:
                            [
                              'Pendente',
                              'Pronto para Retirada',
                              'Concluído',
                              'Cancelado',
                            ].contains(order.status)
                            ? order.status
                            : 'Pendente',
                        items: const [
                          DropdownMenuItem(
                            value: 'Pendente',
                            child: Text(
                              'Pendente',
                              style: TextStyle(color: AppTheme.warningColor),
                            ),
                          ),
                          DropdownMenuItem(
                            value: 'Pronto para Retirada',
                            child: Text(
                              'Pronto para Retirada',
                              style: TextStyle(color: AppTheme.infoColor),
                            ),
                          ),
                          DropdownMenuItem(
                            value: 'Concluído',
                            child: Text(
                              'Concluído',
                              style: TextStyle(color: AppTheme.primaryColor),
                            ),
                          ),
                          DropdownMenuItem(
                            value: 'Cancelado',
                            child: Text(
                              'Cancelado',
                              style: TextStyle(color: AppTheme.errorColor),
                            ),
                          ),
                        ],
                        onChanged: (newStatus) {
                          if (newStatus != null && newStatus != order.status) {
                            onUpdateStatus(order, newStatus);
                          }
                        },
                      ),
                    ],
                  ),
                  const Divider(),
                ],
                if (!isProducer &&
                    order.producerAddress != null &&
                    order.producerAddress!.isNotEmpty) ...[
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(
                        Icons.location_on,
                        color: Colors.grey,
                        size: 20,
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          'Retirar em:\n${order.producerAddress!}',
                          style: const TextStyle(fontSize: 14),
                        ),
                      ),
                    ],
                  ),
                  if (order.producerLatitude != null &&
                      order.producerLongitude != null)
                    Padding(
                      padding: const EdgeInsets.only(top: 4.0, left: 28.0),
                      child: TextButton.icon(
                        onPressed: () => _launchMapsUrl(
                          context,
                          order.producerLatitude!,
                          order.producerLongitude!,
                        ),
                        icon: const Icon(Icons.map, size: 18),
                        label: const Text('Ver Rota no Mapa'),
                        style: TextButton.styleFrom(
                          foregroundColor: AppTheme.infoColor,
                          padding: EdgeInsets.zero,
                          minimumSize: const Size(50, 30),
                          alignment: Alignment.centerLeft,
                        ),
                      ),
                    ),
                  const SizedBox(height: 12),
                ],
                if (!isProducer &&
                    order.producerPhone != null &&
                    order.producerPhone!.isNotEmpty) ...[
                  Row(
                    children: [
                      const Icon(Icons.phone, color: Colors.grey, size: 20),
                      const SizedBox(width: 8),
                      Text(
                        order.producerPhone!,
                        style: const TextStyle(fontSize: 14),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                ],
                if (isProducer &&
                    order.consumerPhone != null &&
                    order.consumerPhone!.isNotEmpty) ...[
                  Row(
                    children: [
                      const Icon(Icons.phone, color: Colors.grey, size: 20),
                      const SizedBox(width: 8),
                      Text(
                        order.consumerPhone!,
                        style: const TextStyle(fontSize: 14),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                ],
                const Text(
                  'Itens do Pedido:',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.black87,
                  ),
                ),
                const SizedBox(height: 8),
                ...order.items.map(
                  (item) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 4.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          '${item.quantity.toStringAsFixed(item.product?.unit == "kg" ? 1 : 0)} ${item.product?.unit ?? ""} de ${item.product?.name ?? 'Indisponível'}',
                        ),
                        Text(
                          CurrencyFormat.format(item.unitPrice),
                          style: const TextStyle(fontWeight: FontWeight.w500),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
