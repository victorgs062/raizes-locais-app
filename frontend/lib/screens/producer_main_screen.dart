import 'package:flutter/material.dart';

import 'producer_dashboard_screen.dart';
import 'orders_screen.dart';
import 'profile_screen.dart';

class ProducerMainScreen extends StatefulWidget {
  const ProducerMainScreen({super.key});

  @override
  State<ProducerMainScreen> createState() => _ProducerMainScreenState();
}

class _ProducerMainScreenState extends State<ProducerMainScreen> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    const ProducerDashboardScreen(),
    const OrdersScreen(),
    const ProfileScreen(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.store),
            label: 'Meus Produtos',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.receipt_long),
            label: 'Vendas',
          ),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Perfil'),
        ],
      ),
    );
  }
}
