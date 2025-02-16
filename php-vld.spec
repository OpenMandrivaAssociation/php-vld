%define modname vld
%define soname %{modname}.so
%define inifile 98_%{modname}.ini

Summary:	Provides functionality to dump the internal representation of PHP scripts
Name:		php-%{modname}
Version:	0.13.0
Release:	3
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/vld
Source0:	http://pecl.php.net/get/vld-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file
Requires(pre,postun): rpm-helper

%description
The Vulcan Logic Disassembler hooks into the Zend Engine and dumps all the
opcodes (execution units) of a script.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make

%install

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}/var/log/httpd

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}

[vld]
vld.active = 0
vld.execute = 1
vld.skip_append = 0
vld.skip_prepend = 0
vld.verbosity = 1
EOF

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files
%doc package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
