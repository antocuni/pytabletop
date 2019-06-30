#!/bin/bash

# usage: deploy.sh [--all]

TMPDIR=/tmp/adbpush/pytt
FILES=(
    android.txt
    main.py
    pytt
    )

if [ x$1 = "x--all" ]
then
    FILES+=(libs)
    adb shell rm -rf /sdcard/kivy/pytabletop
fi

rm -rf $TMPDIR
mkdir -p $TMPDIR
cp -L -r "${FILES[@]}" $TMPDIR
cd $TMPDIR
py.cleanup
cd -

adb push $TMPDIR /sdcard/kivy/pytabletop
adb logcat -c
adb logcat -s python
