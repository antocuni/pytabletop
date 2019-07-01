#!/bin/bash

# usage: deploy.sh [--all]

TMPDIR=/tmp/adbpush/pytabletop-master
FILES=(android.txt
       main.py
       libs
       pytt
      )

rm -rf $TMPDIR
mkdir -p $TMPDIR

if [ x$1 = "x--all" ]
then
    # deploy everything -- slowish
    adb shell rm -rf /sdcard/kivy/pytabletop-master
    cp -L -r "${FILES[@]}" $TMPDIR
    cd $TMPDIR
    py.cleanup
    cd -
    adb push $TMPDIR /sdcard/kivy/pytabletop-master
else
    # deploy only pytt -- faster
    cp -L -r pytt $TMPDIR
    cd $TMPDIR
    py.cleanup
    cd -
    adb shell rm -rf /sdcard/kivy/pytabletop-master/pytt
    adb push $TMPDIR/pytt /sdcard/kivy/pytabletop-master
fi

adb logcat -c
adb logcat -s python
