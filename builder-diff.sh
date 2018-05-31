#!/bin/bash
#
# A helper script that diffs recursively two build targets.

PROJECT_HOME=/Users/jeandersonbc/projects/jpf/jpf-core
OLD_TARGET=ant-build
NEW_TARGET=gradle-build

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

BASEDIR=`pwd`
pushd $PROJECT_HOME
rm -rf $OLD_TARGET $NEW_TARGET

echo "Running ant build"
time ant clean test &>$BASEDIR/ant-build.log
echo "Extracting jars"
extract_jars
mv build $OLD_TARGET

echo "Running gradle build"
time ./gradlew clean test --info &>$BASEDIR/gradle-build.log
echo "Extracting jars"
extract_jars
mv build $NEW_TARGET

diff -r $OLD_TARGET $NEW_TARGET
popd
