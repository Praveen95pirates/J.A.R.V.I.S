[app]

# (str) Title of your application
title = J.A.R.V.I.S.

# (str) Package name
package.name = jarvis

# (str) Package domain (needed for android/ios packaging)
package.domain = org.ai.jarvis

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,mp3,wav,json,yaml,yml,txt,md

# (list) Application requirements
requirements = python3,kivy,android,pyjnius,requests,speechrecognition,plyer,webview

# (str) Presplash of the application
presplash.filename = %(source.dir)s/android/assets/splash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/android/assets/icon-512.png

# (str) Supported orientation (landscape, portrait, all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,WAKE_LOCK,FOREGROUND_SERVICE,ACCESS_NETWORK_STATE

# (str) The format used to package the app for release mode
# possible values: aab, apk
android.release_artifact = apk

# (int) Minimum API required
android.minapi = 21

# (int) Target API
android.targetapi = 34

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private storage on Android
android.private_storage = True

# (bool) Enable AndroidX support
android.enable_androidx = True

# (bool) Enable Gradle build
android.gradle_build_tools = 8.7.3

# (bool) Enable auto-backup
android.allow_backup = True

# (str) The location of the build directory
build_dir = .buildozer

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (list) The Android app metadata
meta.data = org.ai.jarvis

[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
