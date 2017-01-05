Name:           occi 
Version:        1.0.0.0
Release:        1
Vendor:         AsiaInfo, Inc.
URL:            http://www.asiainfo.com
Packager:       AsiaInfo, Inc.<For more information, please contact your sales representative>
Summary:        OCCI service installation package. 
Group:          Applications/System
License:        Copyright AsiaInfo, Inc. 2016
Source0:        %{name}-%{version}.tar.gz
BuildArch:      x86_64 
Requires:       ambari-server = 2.4.0.1
%define         userpath  /var/lib/ambari-server/resources/stacks/HDP/2.5/services
Prefix:         %{userpath}
%define         _topdir %(echo $PWD)/dist
%description 
OCCI service installation package.

%prep
%setup -c
%install
install -d $RPM_BUILD_ROOT%{userpath}
cp -a * $RPM_BUILD_ROOT%{userpath}
exit 0
%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}
%files
%defattr(-,root,root)
%{userpath}

%changelog
