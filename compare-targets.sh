#!/bin/bash
JPF_HOME=/Users/jeandersonbc/projects/jpf/jpf-core
OLD_TARGET=ant-build
NEW_TARGET=gradle-build
BASEDIR=`pwd`

extract_jars() {
    for jar_path in $(find build -name "*.jar"); do
        jar_dir=$(echo $jar_path | sed "s/\.jar/-jar/g")
        mkdir -p $jar_dir
        cp $jar_path $jar_dir

        pushd $jar_dir
        jar_name=$(echo $jar_path | sed "s/.*\///g")
        tar xf $jar_name
        rm $jar_name
        popd;

    done;
}

pushd $JPF_HOME
rm -rf $OLD_TARGET $NEW_TARGET

echo "Running ant build"
time ant clean build &>$BASEDIR/ant-build.log
extract_jars
mv build $OLD_TARGET

echo "Running gradle build"
time ./gradlew clean buildJars --info &>$BASEDIR/gradle-build.log
extract_jars
mv build $NEW_TARGET

diff -r $OLD_TARGET $NEW_TARGET
popd
