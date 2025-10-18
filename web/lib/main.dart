import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:job_buddy/global/app_routes.dart';
import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(const WebApp());
}

class WebApp extends StatelessWidget {
  const WebApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Job Buddy',
      debugShowCheckedModeBanner: false,
      initialRoute: AppRoute.auth.path,
      routes: appRoutes,
    );
  }
}
