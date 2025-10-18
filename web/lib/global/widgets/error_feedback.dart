import 'package:flutter/material.dart';

enum FeedbackType { error, success, info }

class ErrorFeedback extends StatelessWidget {
  final String message;
  final FeedbackType type;
  final bool visible;

  const ErrorFeedback({
    super.key,
    required this.message,
    this.type = FeedbackType.error,
    this.visible = true,
  });

  Color _backgroundColor(BuildContext context) {
    switch (type) {
      case FeedbackType.success:
        return Colors.green.shade50;
      case FeedbackType.info:
        return Colors.blue.shade50;
      case FeedbackType.error:
        return Colors.red.shade50;
    }
  }

  IconData _icon() {
    switch (type) {
      case FeedbackType.success:
        return Icons.check_circle_outline;
      case FeedbackType.info:
        return Icons.info_outline;
      case FeedbackType.error:
        return Icons.error_outline;
    }
  }

  Color _iconColor() {
    switch (type) {
      case FeedbackType.success:
        return Colors.green.shade700;
      case FeedbackType.info:
        return Colors.blue.shade700;
      case FeedbackType.error:
        return Colors.red.shade700;
    }
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedSwitcher(
      duration: const Duration(milliseconds: 300),
      switchInCurve: Curves.easeOut,
      switchOutCurve: Curves.easeIn,
      child: visible
          ? Container(
              key: ValueKey(message),
              margin: const EdgeInsets.only(bottom: 12),
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: _backgroundColor(context),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: _iconColor().withValues(alpha: 0.3)),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(_icon(), color: _iconColor()),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      message,
                      style: TextStyle(
                        color: _iconColor(),
                        fontSize: 14,
                        height: 1.4,
                      ),
                    ),
                  ),
                ],
              ),
            )
          : const SizedBox.shrink(),
    );
  }
}
