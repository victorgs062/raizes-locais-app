import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'providers/auth_provider.dart';
import 'screens/login_screen.dart';
import 'screens/consumer_main_screen.dart';
import 'screens/producer_main_screen.dart';
import 'providers/cart_provider.dart';
import 'utils/app_theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final authProvider = AuthProvider();
  await authProvider.init();

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: authProvider),
        ChangeNotifierProvider(create: (_) => CartProvider()),
      ],
      child: const RaizesLocaisApp(),
    ),
  );
}

class RaizesLocaisApp extends StatelessWidget {
  const RaizesLocaisApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Raízes Locais',
      theme: AppTheme.themeData,
      home: Consumer<AuthProvider>(
        builder: (context, auth, _) {
          if (auth.isAuthenticated) {
            if (auth.currentUser?.role == 'producer') {
              return const ProducerMainScreen();
            } else {
              return const ConsumerMainScreen();
            }
          }
          return const LoginScreen();
        },
      ),
    );
  }
}
