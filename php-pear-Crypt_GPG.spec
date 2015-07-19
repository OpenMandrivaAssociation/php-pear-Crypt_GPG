%define  upstream_name Crypt_GPG
%define peardir %(pear config-get php_dir 2> /dev/null || echo %{_datadir}/pear)
%define xmldir  /var/lib/pear


Name:		php-pear-%{upstream_name}
Version: 	1.3.2
Release:	2
Summary: 	GNU Privacy Guard (GnuPG)
License: 	LGPL
Group: 		Development/PHP
Source0:	http://pear.phpunit.de/get/%upstream_name-%{version}.tgz
URL: 		http://pear.php.net/package/Crypt_GPG
BuildRequires: 	php-pear >= 1.4.7
Requires(pre):	php-pear
BuildArch: noarch

%description
This package provides an object oriented interface to GNU Privacy Guard
(GnuPG). It requires the GnuPG executable to be on the system.

Though GnuPG can support symmetric-key cryptography, this package is
intended only to facilitate public-key cryptography.

This package requires PHP version 5.2.1 or greater.

%prep
%setup -c -T
pear -v -c pearrc \
        -d php_dir=%{peardir} \
        -d doc_dir=/docs \
        -d bin_dir=%{_bindir} \
        -d data_dir=%{peardir}/data \
        -d test_dir=%{peardir}/tests \
        -d ext_dir=%{_libdir} \
        -s

%build

%install
pear -c pearrc install --nodeps --packagingroot %{buildroot} %{SOURCE0}
        
# Clean up unnecessary files
rm pearrc
rm %{buildroot}/%{peardir}/.filemap
rm %{buildroot}/%{peardir}/.lock
rm -rf %{buildroot}/%{peardir}/.registry
rm -rf %{buildroot}%{peardir}/.channels
rm %{buildroot}%{peardir}/.depdb
rm %{buildroot}%{peardir}/.depdblock

mv %{buildroot}/docs .


# Install XML package description
mkdir -p %{buildroot}%{xmldir}
tar -xzf %{SOURCE0} package.xml
cp -p package.xml %{buildroot}%{xmldir}/Crypt_GPG.xml


%post
pear install --nodeps --soft --force --register-only %{xmldir}/Crypt_GPG.xml

%postun
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only pear.php.net/Crypt_GPG
fi

%files
%doc docs/Crypt_GPG/*
%{peardir}/*
%{xmldir}/Crypt_GPG.xml


%changelog
* Wed Oct 15 2014 umeabot <umeabot> 1.3.2-4.mga5
+ Revision: 742242
- Second Mageia 5 Mass Rebuild

* Wed Oct 01 2014 tv <tv> 1.3.2-3.mga5
+ Revision: 734036
- rebuild for pear deps

* Tue Sep 16 2014 umeabot <umeabot> 1.3.2-2.mga5
+ Revision: 687198
- Mageia 5 Mass Rebuild

* Wed Apr 09 2014 spuhler <spuhler> 1.3.2-1.mga5
+ Revision: 613067
- imported package php-pear-Crypt_GPG

