#!/bin/bash

TMPDIR=/tmp/adbpush/pytt

mkdir -p $TMPDIR
cp -L -r * $TMPDIR
cd $TMPDIR
py.cleanup
cd -

adb shell rm -rf /sdcard/kivy/pytabletop
adb push $TMPDIR /sdcard/kivy/pytabletop
adb logcat -c
adb logcat -s python
