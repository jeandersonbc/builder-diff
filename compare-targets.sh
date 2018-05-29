#!/bin/bash
JPF_HOME=/Users/jeandersonbc/projects/jpf/jpf-core

OLD_TARGET=ant-build
NEW_TARGET=gradle-build
BASEDIR=`pwd`

pushd $JPF_HOME
rm -rf $OLD_TARGET $NEW_TARGET

echo "Running ant build"
time ant clean build &>$BASEDIR/ant-build.log
mv build $OLD_TARGET

echo "Running gradle build"
time ./gradlew clean buildJars --info &>$BASEDIR/gradle-build.log
mv build $NEW_TARGET

diff -r $OLD_TARGET $NEW_TARGET

# TODO: must compare jar files

rm -rf $OLD_TARGET $NEW_TARGET
popd
