import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:google_fonts/google_fonts.dart';

class MyCombinedWidget extends StatelessWidget {
  final String? imageUrl; // URL gambar, bisa null jika tidak ada gambar
  final String fileName; // Nama file untuk ditampilkan

  const MyCombinedWidget({super.key, this.imageUrl, required this.fileName});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(bottom: 15.h),
      child: Container(
        width: 330.w,
        height: 120.h,
        padding: EdgeInsets.symmetric(vertical: 10.h, horizontal: 10.w),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(15),
          boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.2), 
            spreadRadius: 2, 
            blurRadius: 5, 
            offset: Offset(0, 3), 
          ),
        ],
        ),
        child: Row(
          children: [
            Padding(
              padding: EdgeInsets.only(right: 30.w),
              child: Text(
                fileName,
                style: GoogleFonts.poppins(),
              ),
            ),
            Container(
              width: 100.w,
              height: 120.h,
              decoration: BoxDecoration(
                color: Colors.red,
                borderRadius: BorderRadius.circular(15),
              ),
              child: imageUrl != null && imageUrl!.isNotEmpty // Cek jika ada gambar
                  ? ClipRRect(
                      borderRadius: BorderRadius.circular(15), // Membulatkan sudut
                      child: Image.network(
                        imageUrl!,
                        fit: BoxFit.cover, // Gambar akan menutupi seluruh kontainer
                        width: 100.w,
                        height: 120.h,
                      ),
                    )
                  : Center(
                      child: Icon(
                        Icons.image, // Ganti dengan ikon yang Anda inginkan
                        size: 50.sp, // Ukuran ikon
                        color: Colors.white, // Warna ikon
                      ),
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
