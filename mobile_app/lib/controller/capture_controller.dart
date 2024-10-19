import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class CaptureProvider with ChangeNotifier {
  bool _isCapturing = false;

  bool get isCapturing => _isCapturing;

  Future<void> captureImage() async {
    _isCapturing = true;
    notifyListeners();
    
    final response = await http.get(Uri.parse('http://YOUR_FLASK_SERVER_IP:5000/capture'));

    if (response.statusCode == 200) {
      print('Image captured successfully');
    } else {
      print('Failed to capture image');
    }

    _isCapturing = false;
    notifyListeners();
  }
}
