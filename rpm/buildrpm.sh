#! /bin/bash
RPM_PATH=`dirname $0`
SOURCE_PATH=${RPM_PATH}"/.."
echo OCCI SOURCE PATH is $SOURCE_PATH
cd $SOURCE_PATH
yum install -y rpm-build
rm -rf ~/rpmbuild
mkdir -pv ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
mkdir ~/rpmbuild/SOURCES/OCCI
cp -rf * ~/rpmbuild/SOURCES/OCCI
cp -f rpm/OCCI-0.1.spec ~/rpmbuild/SPECS
tar -zcvf ~/rpmbuild/SOURCES/occi-1.0.0.0.tar.gz -C ~/rpmbuild/SOURCES OCCI --exclude .git
rpmbuild -bb ~/rpmbuild/SPECS/OCCI-0.1.spec
mv ~/rpmbuild/RPMS/x86_64/occi-1.0.0.0-1.x86_64.rpm ./rpm 
rm -rf ~/rpmbuild
