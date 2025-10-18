import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:job_buddy/services/auth_service.dart';
import 'package:job_buddy/views/email_verification_view.dart';
import 'package:job_buddy/views/home_view.dart';
import 'package:job_buddy/views/login_view.dart';

class AuthGate extends StatelessWidget {
  AuthGate({super.key});

  final AuthService _authService = AuthService();

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<User?>(
      stream: _authService.authStateChanges,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return const Center(child: Text('Something went wrong!'));
        } else if (snapshot.hasData) {
          final user = snapshot.data!;
          if (user.emailVerified) {
            return const HomeView();
          } else {
            return const EmailVerificationView();
          }
        } else {
          return const LoginView();
        }
      },
    );
  }
}
