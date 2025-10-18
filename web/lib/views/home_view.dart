import 'package:flutter/material.dart';
import 'package:job_buddy/global/app_routes.dart';
import 'package:job_buddy/services/auth_service.dart';

class HomeView extends StatefulWidget {
  const HomeView({super.key});

  @override
  State<HomeView> createState() => _HomeViewState();
}

class _HomeViewState extends State<HomeView> {
  final authService = AuthService();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Job Buddy'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Welcome to Job Buddy!'),
            ElevatedButton(
              onPressed: () async {
                await authService.signOut().then((_) {
                  if (!context.mounted) return;
                  Navigator.pushNamedAndRemoveUntil(
                    context,
                    AppRoute.login.path,
                    (route) => false,
                  );
                });
              },
              child: const Text('Logout'),
            ),
          ],
        ),
      ),
    );
  }
}
