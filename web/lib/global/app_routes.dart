import 'package:flutter/material.dart';
import 'package:job_buddy/views/auth_wrapper.dart';
import 'package:job_buddy/views/email_verification_view.dart';
import 'package:job_buddy/views/forgot_password_view.dart';
import 'package:job_buddy/views/home_view.dart';
import 'package:job_buddy/views/login_view.dart';
import 'package:job_buddy/views/signup_view.dart';

enum AppRoute {
  auth,
  login,
  signup,
  home,
  emailVerification,
  forgotPassword,
}

extension AppRouteExtension on AppRoute {
  String get path {
    switch (this) {
      case AppRoute.auth:
        return '/';
      case AppRoute.login:
        return '/login';
      case AppRoute.signup:
        return '/signup';
      case AppRoute.home:
        return '/home';
      case AppRoute.emailVerification:
        return '/emailVerification';
      case AppRoute.forgotPassword:
        return '/forgotPassword';
    }
  }

  WidgetBuilder get builder {
    switch (this) {
      case AppRoute.auth:
        return (context) => AuthGate();
      case AppRoute.login:
        return (context) => const LoginView();
      case AppRoute.signup:
        return (context) => const SignUpView();
      case AppRoute.home:
        return (context) => const HomeView();
      case AppRoute.emailVerification:
        return (context) => const EmailVerificationView();
      case AppRoute.forgotPassword:
        return (context) => const ForgotPasswordView();
    }
  }
}

Map<String, WidgetBuilder> get appRoutes => {
  for (final r in AppRoute.values) r.path: r.builder,
};
