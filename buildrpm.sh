#! /bin/bash
OCCI_PATH=`dirname $0`
cd $OCCI_PATH
mkdir dist/SOURCES/OCCI
cp -rf src/* dist/SOURCES/OCCI
tar -zcvf dist/SOURCES/occi-1.0.0.0.tar.gz -C dist/SOURCES OCCI
rpmbuild -bb dist/SPECS/OCCI.spec
rm -rf dist/SOURCES/*
