#!/bin/bash

TMPDIR=/tmp/adbpush/viewer

mkdir -p $TMPDIR
cp -L -r * $TMPDIR
cd $TMPDIR
py.cleanup
cd -

adb shell rm -rf /sdcard/kivy/pytabletop
adb push $TMPDIR /sdcard/kivy/pytabletop
adb logcat -c
adb logcat -s python
