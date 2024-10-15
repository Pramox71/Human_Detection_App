import 'package:flutter/material.dart';

class BottomNavProvider with ChangeNotifier {
  int _selectedIndex = 0;
  final PageController _pageController = PageController();
  int get selectedIndex => _selectedIndex;
  PageController get pageController => _pageController;
  void updateIndex(int index) {
    _selectedIndex = index;
    _pageController.jumpToPage(index); // Navigasi ke halaman yang sesuai
    notifyListeners();
  }
  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }
}