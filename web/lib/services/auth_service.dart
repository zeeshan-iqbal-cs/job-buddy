import 'package:firebase_auth/firebase_auth.dart';
import 'package:job_buddy/utils/firebase_error_mapper.dart';

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final GoogleAuthProvider _googleProvider = GoogleAuthProvider();

  Stream<User?> get authStateChanges => _auth.authStateChanges();
  User? get currentUser => _auth.currentUser;

  // --- Email/Password Signup ---
  Future<User?> signUp(String email, String password) async {
    try {
      final cred = await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );
      await cred.user?.sendEmailVerification();
      return cred.user;
    } on FirebaseAuthException catch (e) {
      throw FirebaseErrorMapper.toMessage(e.code);
    } catch (_) {
      throw 'Something went wrong while signing up. Please try again.';
    }
  }

  Future<User?> signIn(String email, String password) async {
    try {
      final cred = await _auth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
      return cred.user;
    } on FirebaseAuthException catch (e) {
      throw FirebaseErrorMapper.toMessage(e.code);
    } catch (_) {
      throw 'An unknown error occurred while signing in.';
    }
  }

  Future<UserCredential?> signInWithGoogle() async {
    try {
      _googleProvider.addScope(
        'https://www.googleapis.com/auth/contacts.readonly',
      );
      _googleProvider.setCustomParameters({
        'login_hint': 'user@example.com',
      });

      final cred = await _auth.signInWithPopup(_googleProvider);

      return cred;
    } on FirebaseAuthException catch (e) {
      throw FirebaseErrorMapper.toMessage(e.code);
    } catch (_) {
      throw 'Google sign-in failed. Please try again.';
    }
  }

  // --- Sign Out ---
  Future<void> signOut() async {
    try {
      await _auth.signOut();
    } catch (_) {
      throw 'Error while signing out. Please try again.';
    }
  }

  // --- Send Email Verification ---
  Future<void> sendEmailVerification() async {
    try {
      final user = _auth.currentUser;
      if (user != null && !user.emailVerified) {
        await user.sendEmailVerification();
      }
    } on FirebaseAuthException catch (e) {
      throw FirebaseErrorMapper.toMessage(e.code);
    } catch (_) {
      throw 'Could not send verification email. Please try again.';
    }
  }

  // --- Password Reset ---
  Future<void> sendPasswordReset(String email) async {
    try {
      await _auth.sendPasswordResetEmail(email: email);
    } on FirebaseAuthException catch (e) {
      throw FirebaseErrorMapper.toMessage(e.code);
    } catch (_) {
      throw 'Unable to send password reset link. Try again later.';
    }
  }

  // --- Reload User State ---
  Future<void> reloadUser() async {
    try {
      await _auth.currentUser?.reload();
    } catch (_) {
      throw 'Failed to refresh user data. Please reload the app.';
    }
  }
}
