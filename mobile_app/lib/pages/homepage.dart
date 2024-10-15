import 'package:bottom_bar/bottom_bar.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:flutter_mjpeg/flutter_mjpeg.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:human_detection_app/controller/navbar_controller.dart';
import 'package:human_detection_app/pages/camera.dart';
import 'package:human_detection_app/pages/rekaman.dart';
import 'package:human_detection_app/pages/tangkapan_camera.dart';
import 'package:provider/provider.dart';

class MyHomePage extends HookWidget {
  const MyHomePage({super.key});
  @override
  Widget build(BuildContext context) {
    final isRunning = useState(true);
    final bottomNavProvider = Provider.of<BottomNavProvider>(context);
    return Scaffold(
      appBar: AppBar(
        title: Center(
          child: Text('FinExpo2024', style: GoogleFonts.openSans(fontSize: 30.sp)),
        ),
      ),
      body: SafeArea(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            Center(
              child: Container(
                width: 330.w,
                height: 170.h,
                color: Colors.brown,
                child: Expanded(
                  child: Mjpeg(
                    isLive: isRunning.value,
                    error: (context, error, stack) {
                      return Center(
                        child: Text(
                          error.toString(), 
                          style: GoogleFonts.poppins(
                            fontSize: 14.sp,
                            color: Colors.red,
                            fontWeight: FontWeight.bold,
                          ),
                          textAlign: TextAlign.center,
                        )
                      );
                    },
                    stream:
                    'http://hkcctv.tunnel.kazuyosan.my.id/jdIXe4mglNxQwv7sr2QNtN2O4nqbfs/mjpeg/0EQBg36nUv/HKCCTV_IM001_AI'
                    // 'http://hkcctv.tunnel.kazuyosan.my.id/jdIXe4mglNxQwv7sr2QNtN2O4nqbfs/mjpeg/0EQBg36nUv/HKCCTV_IM001_AI', //'http://192.168.1.37:8081',
                  ),
                ),
              ),
            ),
            Padding(
              padding: EdgeInsets.symmetric(horizontal: 20.w, vertical: 20.h),
              child: Row(
                children: [
                  Padding(
                    padding: EdgeInsets.only(right: 20.w),
                    child: IconButton(
                      onPressed: (){}, 
                      icon: Icon(
                          Icons.photo_camera,
                          size: 30.sp,
                        )
                      ),
                  ),
                  Padding(
                    padding: EdgeInsets.only(right: 146.w),
                    child: IconButton(
                      onPressed: (){}, 
                      icon: Icon(
                          Icons.movie_creation,
                          size: 30.sp,
                        )
                      ),
                  ),
                  IconButton(
                    onPressed: (){}, 
                    icon: Icon(
                        Icons.zoom_out_map,
                        size: 30.sp,
                      )
                    ),
                ],
              ),
            ),
            Expanded(
              child: PageView(
                controller: bottomNavProvider.pageController,
                onPageChanged: (index){
                  bottomNavProvider.updateIndex(index);
                },
                children: [
                  MyCamera(),
                  MyRekaman(),
                  MyCapture(),
                ],
              ),
            )
          ],
        ),
      ),
      bottomNavigationBar: BottomBar(
        selectedIndex: bottomNavProvider.selectedIndex,         
        onTap: (index){
          bottomNavProvider.updateIndex(index);
        },
        items: [
          BottomBarItem(
            icon: Icon(Icons.camera),
            title: Text('Camera', style: GoogleFonts.poppins()),
            activeColor: Colors.brown.shade400
          ),
          BottomBarItem(
            icon: Icon(Icons.video_camera_front),
            title: Text('Rekaman', style: GoogleFonts.poppins()),
            activeColor: Colors.brown.shade400
          ),
          BottomBarItem(
            icon: Icon(Icons.screenshot),
            title: Text('Tangkapan Camera', style: GoogleFonts.poppins()),
            activeColor: Colors.brown.shade400
          ),
        ],
      ),
    );
  }
}
