import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:human_detection_app/widget/custom_list_view.dart';

class MyCamera extends StatelessWidget {
  const MyCamera({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: Padding(
        padding: EdgeInsets.symmetric(vertical: 10.w),
        child: ListView(
          children: [
            Center(
              child: MyCombinedWidget(
                fileName: "20241005-144235.160.jpg",
                imageUrl: "",
              ),
            ),
            Center(
              child: MyCombinedWidget(
                fileName: "20241005-144235.160.jpg",
                imageUrl: "",
              ),
            ),
            Center(
              child: MyCombinedWidget(
                fileName: "20241005-144235.160.jpg",
                imageUrl: "",
              ),
            ),
            Center(
              child: MyCombinedWidget(
                fileName: "20241005-144235.160.jpg",
                imageUrl: "",
              ),
            ),
            Center(
              child: MyCombinedWidget(
                fileName: "20241005-144235.160.jpg",
                imageUrl: "",
              ),
            ),
            Center(
              child: MyCombinedWidget(
                fileName: "20241005-144235.160.jpg",
                imageUrl: "",
              ),
            ),
            Center(
              child: MyCombinedWidget(
                fileName: "20241005-144235.160.jpg",
                imageUrl: "",
              ),
            ),
            Center(
              child: MyCombinedWidget(
                fileName: "20241005-144235.160.jpg",
                imageUrl: "",
              ),
            ),
            Center(
              child: MyCombinedWidget(
                fileName: "20241005-144235.160.jpg",
                imageUrl: "",
              ),
            ),
          ],
        ),
      ),
    );
  }
}