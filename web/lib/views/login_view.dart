import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:job_buddy/global/app_routes.dart';
import 'package:job_buddy/global/widgets/error_dialog.dart';
import 'package:job_buddy/services/auth_service.dart';

class LoginView extends StatefulWidget {
  const LoginView({super.key});

  @override
  State<LoginView> createState() => _LoginViewState();
}

class _LoginViewState extends State<LoginView> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  final AuthService authService = AuthService();

  Future<void> _login(BuildContext context) async {
    try {
      final user = await authService.signIn(
        emailController.text.trim(),
        passwordController.text,
      );

      if (!context.mounted) return;

      if (user == null) {
        await AppDialog.show(
          context,
          message: 'User not found or credentials invalid.',
          type: DialogType.error,
        );
        return;
      }

      if (!user.emailVerified) {
        await AppDialog.show(
          context,
          message: 'Please verify your email before logging in.',
          type: DialogType.info,
        );
        if (!context.mounted) return;
        Navigator.pushNamedAndRemoveUntil(
          context,
          AppRoute.emailVerification.path,
          (route) => false,
        );
      } else {
        Navigator.pushNamedAndRemoveUntil(
          context,
          AppRoute.home.path,
          (route) => false,
        );
      }
    } catch (e) {
      if (!context.mounted) return;
      await AppDialog.show(
        context,
        message: e.toString(),
        type: DialogType.error,
      );
    }
  }

  Future<void> _loginWithGoogle(BuildContext context) async {
    try {
      final user = await authService.signInWithGoogle();
      if (!context.mounted) return;

      if (user != null) {
        await AppDialog.show(
          context,
          message: 'Logged in successfully with Google!',
          type: DialogType.success,
        );
        if (!context.mounted) return;
        Navigator.pushNamedAndRemoveUntil(
          context,
          AppRoute.home.path,
          (route) => false,
        );
      }
    } catch (e) {
      if (!context.mounted) return;
      await AppDialog.show(
        context,
        message: 'Google sign-in failed: $e',
        type: DialogType.error,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final isWide = width > 600;

    return Scaffold(
      backgroundColor: Colors.grey[100],
      body: Center(
        child: Container(
          width: isWide ? 400 : width * 0.9,
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
              const Text(
                'Welcome 👋',
                style: TextStyle(
                  fontSize: 26,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'Please log in to continue',
                style: TextStyle(color: Colors.grey[600]),
              ),
              const SizedBox(height: 24),

              TextField(
                controller: emailController,
                decoration: InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
              const SizedBox(height: 16),

              // Password field
              TextField(
                controller: passwordController,
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
              const SizedBox(height: 24),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => _login(context),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    backgroundColor: Colors.blueAccent,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text(
                    'Login',
                    style: TextStyle(fontSize: 16, color: Colors.white),
                  ),
                ),
              ),
              const SizedBox(height: 16),

              TextButton(
                onPressed: () {
                  Navigator.pushNamed(
                    context,
                    AppRoute.forgotPassword.path,
                  );
                },
                style: TextButton.styleFrom(alignment: Alignment.centerRight),
                child: Text(
                  'Forgot your Password?',
                ),
              ),

              const SizedBox(height: 16),

              Row(
                children: [
                  Expanded(child: Divider(color: Colors.grey[300])),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 8.0),
                    child: Text(
                      'OR',
                      style: TextStyle(color: Colors.grey[600]),
                    ),
                  ),
                  Expanded(child: Divider(color: Colors.grey[300])),
                ],
              ),

              const SizedBox(height: 16),

              SizedBox(
                width: double.infinity,
                child: OutlinedButton(
                  onPressed: () => _loginWithGoogle(context),
                  style: OutlinedButton.styleFrom(
                    backgroundColor: const Color(0xFFFFFFFF), // Fill
                    side: const BorderSide(
                      color: Color(0xFF747775), // Stroke color
                      width: 1, // Stroke width
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(
                        24,
                      ), // Rounded corners
                    ),
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 14,
                    ),
                    foregroundColor: const Color(0xFF1F1F1F), // Text color
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      SvgPicture.asset(
                        'assets/Google Icon/light/web_light_rd_na.svg',
                        height: 24,
                        width: 24,
                      ),
                      const SizedBox(width: 12),
                      Text(
                        'Sign in with Google',
                        style: GoogleFonts.roboto(
                          fontWeight: FontWeight.w500,
                          fontSize: 14,
                          height: 20 / 14, // line height = 20
                          color: const Color(0xFF1F1F1F),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 16),

              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    "Don't have an account?",
                    style: TextStyle(color: Colors.grey[700]),
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.pushNamed(
                        context,
                        AppRoute.signup.path,
                      );
                    },
                    child: const Text('Sign Up'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
