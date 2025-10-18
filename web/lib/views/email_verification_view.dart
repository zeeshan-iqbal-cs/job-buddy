import 'dart:async';
import 'package:flutter/material.dart';
import 'package:job_buddy/global/app_routes.dart';
import 'package:job_buddy/services/auth_service.dart';

class EmailVerificationView extends StatefulWidget {
  const EmailVerificationView({super.key});

  @override
  State<EmailVerificationView> createState() => _EmailVerificationViewState();
}

class _EmailVerificationViewState extends State<EmailVerificationView> {
  final auth = AuthService();
  Timer? timer;
  bool isVerified = false;
  bool isResending = false;

  @override
  void initState() {
    super.initState();
    _checkVerification();
    timer = Timer.periodic(
      const Duration(seconds: 3),
      (_) => _checkVerification(),
    );
  }

  Future<void> _checkVerification() async {
    await auth.reloadUser();
    final user = auth.currentUser;
    if (user != null && user.emailVerified) {
      timer?.cancel();
      if (mounted) {
        setState(() => isVerified = true);
        Navigator.pushNamedAndRemoveUntil(
          context,
          AppRoute.home.path,
          (route) => false,
        );
      }
    }
  }

  Future<void> _resendEmail(BuildContext context) async {
    setState(() => isResending = true);

    await auth.sendEmailVerification();

    if (!context.mounted) return;

    setState(() => isResending = false);

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Verification email sent again!')),
    );
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      body: Center(
        child: Container(
          width: 400,
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            boxShadow: const [
              BoxShadow(
                color: Colors.black12,
                blurRadius: 16,
                offset: Offset(0, 6),
              ),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(
                Icons.email_outlined,
                size: 64,
                color: Colors.blueAccent,
              ),
              const SizedBox(height: 16),
              const Text(
                'Verify your email',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              const Text(
                'A verification link has been sent to your email. Please verify your account to continue.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.black54),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () => isResending ? null : _resendEmail(context),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blueAccent,
                  padding: const EdgeInsets.symmetric(
                    vertical: 12,
                    horizontal: 24,
                  ),
                ),
                child: isResending
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: Colors.white,
                        ),
                      )
                    : const Text(
                        'Resend Email',
                        style: TextStyle(
                          color: Colors.white,
                        ),
                      ),
              ),
              const SizedBox(height: 16),
              TextButton(
                onPressed: () async {
                  await auth.signOut();

                  if (!context.mounted) return;

                  Navigator.pushNamedAndRemoveUntil(
                    context,
                    AppRoute.login.path,
                    (route) => false,
                  );
                },
                child: const Text('Back to Login'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
