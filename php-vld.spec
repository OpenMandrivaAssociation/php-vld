%define modname vld
%define soname %{modname}.so
%define inifile 98_%{modname}.ini

Summary:	Provides functionality to dump the internal representation of PHP scripts
Name:		php-%{modname}
Version:	0.11.2
Release:	1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/vld
Source0:	http://pecl.php.net/get/vld-%{version}.tgz
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
rm -rf %{buildroot}

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
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Wed May 02 2012 Oden Eriksson <oeriksson@mandriva.com> 0.11.1-2mdv2012.0
+ Revision: 794922
- rebuild for php-5.4.x

* Tue Apr 10 2012 Oden Eriksson <oeriksson@mandriva.com> 0.11.1-1
+ Revision: 790124
- 0.11.1

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-10
+ Revision: 761126
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-9
+ Revision: 696378
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-8
+ Revision: 695323
- rebuilt for php-5.3.7

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-7
+ Revision: 667760
- mass rebuild

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-6
+ Revision: 646562
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-5mdv2011.0
+ Revision: 629753
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-4mdv2011.0
+ Revision: 628056
- ensure it's built without automake1.7

* Tue Nov 23 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-3mdv2011.0
+ Revision: 600188
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-2mdv2011.0
+ Revision: 588727
- rebuild

* Wed Apr 14 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-1mdv2010.1
+ Revision: 534660
- 0.10.1

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-15mdv2010.1
+ Revision: 514712
- rebuilt for php-5.3.2

* Sun Feb 21 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-14mdv2010.1
+ Revision: 509096
- rebuild

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-13mdv2010.1
+ Revision: 485269
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-12mdv2010.1
+ Revision: 468096
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-11mdv2010.0
+ Revision: 451226
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.9.1-10mdv2010.0
+ Revision: 397301
- Rebuild

* Wed May 13 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-9mdv2010.0
+ Revision: 375367
- rebuilt against php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-8mdv2009.1
+ Revision: 346687
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-7mdv2009.1
+ Revision: 341517
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-6mdv2009.1
+ Revision: 321962
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-5mdv2009.1
+ Revision: 310227
- rebuilt against php-5.2.7

* Thu Aug 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-4mdv2009.0
+ Revision: 266240
- has to be loaded before apc

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-3mdv2009.0
+ Revision: 238472
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-2mdv2009.0
+ Revision: 200303
- rebuilt for php-5.2.6

* Wed Apr 09 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-1mdv2009.0
+ Revision: 192505
- 0.9.1

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-2mdv2008.1
+ Revision: 162106
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Nov 30 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-1mdv2008.1
+ Revision: 114115
- import php-vld


* Fri Nov 30 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-1mdv2008.1
- initial Mandriva package

