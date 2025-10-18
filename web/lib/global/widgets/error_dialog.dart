import 'package:flutter/material.dart';

enum DialogType { error, success, info }

class AppDialog {
  static Future<void> show(
    BuildContext context, {
    required String message,
    String? title,
    DialogType type = DialogType.error,
  }) async {
    final colors = {
      DialogType.error: Colors.redAccent,
      DialogType.success: Colors.green,
      DialogType.info: Colors.blueAccent,
    };

    final icons = {
      DialogType.error: Icons.error_outline,
      DialogType.success: Icons.check_circle_outline,
      DialogType.info: Icons.info_outline,
    };

    await showDialog(
      context: context,
      barrierDismissible: true,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: Row(
          children: [
            Icon(icons[type], color: colors[type]),
            const SizedBox(width: 10),
            Text(
              title ?? _defaultTitle(type),
              style: TextStyle(
                color: colors[type],
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
        content: Text(
          message,
          style: const TextStyle(fontSize: 15),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }

  static String _defaultTitle(DialogType type) {
    switch (type) {
      case DialogType.success:
        return 'Success';
      case DialogType.info:
        return 'Info';
      default:
        return 'Error';
    }
  }
}
