class FirebaseErrorMapper {
  static String toMessage(String code) {
    switch (code) {
      case 'invalid-credential':
        throw 'The credential is invalid. Please try again.';
      case 'user-disabled':
        throw 'This user account has been disabled.';
      case 'user-not-found':
        throw 'No user found for this credential.';
      case 'account-exists-with-different-credential':
        throw 'An account already exists with the same email but different sign-in method.';
      case 'operation-not-allowed':
        throw 'This sign-in method is not enabled.';
      case 'invalid-verification-code':
        throw 'The verification code is invalid.';
      case 'invalid-verification-id':
        throw 'The verification ID is invalid.';
      case 'invalid-email':
        throw 'The email address is malformed.';
      case 'wrong-password':
        throw 'The password is wrong.';
      case 'too-many-requests':
        throw 'Too many attempts. Try again later.';
      case 'network-request-failed':
        throw 'Network connection failed. Please check your internet and try again.';
      case 'expired-action-code':
        throw 'The action code or link has expired.';
      case 'missing-email':
        throw 'Please enter an email address.';
      case 'missing-password':
        throw 'Please enter your password.';
      case 'invalid-user-token':
        throw 'Your session has expired. Please sign in again.';
      case 'user-token-expired':
        throw 'Your authentication token has expired. Please log in again.';
      case 'popup-closed-by-user':
        throw 'The sign-in popup was closed before completing.';
      case 'cancelled-popup-request':
        throw 'Only one popup request is allowed at a time. Please try again.';
      default:
        throw 'An unknown error occurred. Please try again later.';
    }
  }
}
