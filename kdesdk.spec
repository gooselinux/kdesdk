Name: kdesdk
Version: 4.3.4
Release: 4%{?dist}
Summary: The KDE Software Development Kit (SDK)

Group: User Interface/Desktops
License: GPLv2
URL: http://www.kde.org/
Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# bz#587935 - lokalize has two entries in menu (edit)   
Patch0: kdesdk-4.3.4-category.patch

# upstream patches
Patch100: kdesdk-4.3.4-kde#184055.patch.patch
Patch101: kdesdk-4.3.5.patch

BuildRequires: kdepimlibs-devel >= %{version}
BuildRequires: plasma-devel >= %{version}
BuildRequires: strigi-devel
BuildRequires: flex
BuildRequires: apr-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: subversion-devel
BuildRequires: boost-devel
BuildRequires: libical-devel
BuildRequires: binutils-devel

Requires: kdepimlibs >= %{version}
Requires: %{name}-libs = %{version}-%{release}
Requires: kross(python)
Requires(hint): %{name}-utils = %{version}-%{release}

%description
A collection of applications and tools used by developers, including:
* cervisia: a CVS frontend
* kate: advanced text editor
* kbugbuster: a tool to manage the KDE bug report system
* kcachegrind: a browser for data produced by profiling tools (e.g. cachegrind)
* kompare: diff tool
* kuiviewer: displays designer's UI files
* lokalize: computer-aided translation system focusing on productivity and performance
* umbrello: UML modeller and UML diagram tool

%package libs
Summary: Runtime libraries for %{name}
Group:   System Environment/Libraries

%description libs
%{summary}.

%package devel
Summary:  Developer files for %{name}
Group:    Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: kdepimlibs-devel

%description devel
Files for developing applications using %{name}.

%package utils
Summary: Text utilities from %{name}
Group:   Applications/Text

%description utils
%{summary}, including:
po2xml
split2po
swappo
xml2pot


%prep
%setup -q

%patch0 -p1 -b .category

# upstream patches
%patch100 -p4 -b kde#184055
%patch101 -p1 -b .kde4.3.5

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# unpackaged files
rm -f %{buildroot}%{_kde4_libdir}/libantlr.so

# This one fits better into krazy2 (it requires krazy2), and the version in
# kdesdk does not understand lib64.
rm -f %{buildroot}%{_kde4_bindir}/krazy-licensecheck

# move devel symlinks
mkdir -p %{buildroot}%{_kde4_libdir}/kde4/devel
pushd %{buildroot}%{_kde4_libdir}
for i in lib*.so
do
  case "$i" in
    libkateinterfaces.so)
      linktarget=`readlink "$i"`
      rm -f "$i"
      ln -sf "../../$linktarget" "kde4/devel/$i"
      ;;
  esac
done
popd


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
touch --no-create %{_kde4_iconsdir}/locolor &> /dev/null ||:
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
gtk-update-icon-cache %{_kde4_iconsdir}/locolor &> /dev/null ||:
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:


%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  touch --no-create %{_kde4_iconsdir}/locolor &> /dev/null ||:
  touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/locolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null ||:
  update-desktop-database -q &> /dev/null ||:
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LIB COPYING.DOC README
%{_kde4_bindir}/*
# -utils
%exclude %{_kde4_bindir}/po2xml
%exclude %{_kde4_bindir}/split2po
%exclude %{_kde4_bindir}/swappo
%exclude %{_kde4_bindir}/xml2pot
%{_kde4_configdir}/*
%{_kde4_appsdir}/cervisia/
%{_kde4_appsdir}/cervisiapart/*
%{_kde4_appsdir}/kabc/*
%{_kde4_appsdir}/katepart/
%{_kde4_appsdir}/kate/
%{_kde4_appsdir}/kbugbuster/
%{_kde4_appsdir}/kcachegrind/*
%{_kde4_appsdir}/kconf_update/*
%{_kde4_appsdir}/kio_perldoc/
%{_kde4_appsdir}/kdevappwizard/
%{_kde4_appsdir}/kmtrace/
%{_kde4_appsdir}/kompare/
%{_kde4_appsdir}/kpartloader/
%{_kde4_appsdir}/kuiviewer/*
%{_kde4_appsdir}/kuiviewerpart/*
%{_kde4_appsdir}/lokalize/
%{_kde4_appsdir}/umbrello/
%{_kde4_datadir}/applications/kde4/*
%{_kde4_datadir}/config.kcfg/*
%{_kde4_datadir}/dbus-1/interfaces/*
%{_kde4_datadir}/kde4/services/*
%{_kde4_datadir}/kde4/servicetypes/*
%{_kde4_docdir}/HTML/en/cervisia/
%{_kde4_docdir}/HTML/en/kapptemplate/
%{_kde4_docdir}/HTML/en/kate-plugins/
%{_kde4_docdir}/HTML/en/kate/
%{_kde4_docdir}/HTML/en/kbugbuster/
%{_kde4_docdir}/HTML/en/kcachegrind/
%{_kde4_docdir}/HTML/en/kdesvn-build/
%{_kde4_docdir}/HTML/en/kompare/
%{_kde4_docdir}/HTML/en/lokalize/
%{_kde4_docdir}/HTML/en/umbrello/
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_iconsdir}/locolor/*/*/*
%{_kde4_iconsdir}/oxygen/*/*/*
%{_mandir}/man1/*
%{_kde4_libdir}/libkdeinit4*.so
%{_kde4_libdir}/libkomparedialogpages.so
%{_kde4_libdir}/libkomparediff2.so
%{_kde4_libdir}/strigi/*.so
%{_kde4_datadir}/strigi/fieldproperties/
%{_kde4_libdir}/kde4/*.so
# -devel
%exclude %{_kde4_libdir}/kde4/devel/

%files libs
%defattr(-,root,root,-)
%{_kde4_libdir}/lib*.so.*
# -utils
%exclude %{_kde4_libdir}/libantlr.so.*

%files devel
%defattr(-,root,root,-)
%{_kde4_includedir}/*
%{_kde4_libdir}/lib*.so
%exclude %{_kde4_libdir}/libkomparedialogpages.so
%exclude %{_kde4_libdir}/libkomparediff2.so
%{_kde4_libdir}/kde4/devel/lib*.so

%files utils
%defattr(-,root,root,-)
%{_kde4_bindir}/po2xml
%{_kde4_bindir}/split2po
%{_kde4_bindir}/swappo
%{_kde4_bindir}/xml2pot
%{_kde4_libdir}/libantlr.so.*


%changelog
* Fri May 21 2010 Than Ngo <than@redhat.com> - 4.3.4-4
- Resolves: bz#587935, lokalize has two entries in menu

* Wed Mar 31 2010 Than Ngo <than@redhat.com> - 4.3.4-3
- rebuilt against qt 4.6.2

* Thu Jan 21 2010 Than Ngo <than@redhat.com> - 4.3.4-2
- fix kde#184055, Honor file list sorting when opening/creating new file
- update translation

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.3.4-1
- 4.3.4

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Sun Oct 11 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.2-2
- Fix Kompare diff parsing regression (due to a typo in a bugfix)

* Mon Oct 05 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Thu Sep 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-2
- Requires: kross(python) (#523076)

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Wed Jul 22 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Sun Jul 12 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Fri Jun 26 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3rc1

* Thu Jun 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.90-1
- KDE-4.3 beta2 (4.2.90)

* Thu May 14 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.85-1
- KDE 4.3 beta 1

* Wed Apr 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-2
- optimize scriptlets

* Tue Mar 31 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1
- blockquote patch (#487624)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.2.0-2
- fix Kompare crash with Qt 4.5 (kde#182792)
- fix build with GCC 4.4

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Mon Jan 19 2009 Than Ngo <than@redhat.com> - 4.1.96-4
- apply patch to fix  build against Boost 1.37.0 

* Tue Jan 13 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.96-3
- F11+: add workaround to fix build against Boost 1.37.0

* Fri Jan 09 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.96-2
- don't ship krazy-licensecheck, should be in krazy2

* Wed Jan 07 2009 Than Ngo <than@redhat.com> - 4.1.96-1
- 4.2rc1

* Fri Dec 12 2008 Than Ngo <than@redhat.com> 4.1.85-1
- 4.2beta2

* Mon Dec 01 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.80-3
- BR plasma-devel instead of kdebase-workspace-devel
- don't require kdebase-workspace
- rebase Lokalize quit menu patch
- BR libical-devel

* Thu Nov 20 2008 Than Ngo <than@redhat.com> 4.1.80-2
- merged

* Thu Nov 20 2008 Lorenzo Villani <lvillani@binaryhelix.net> 4.1.80-1
- 4.1.80
- BR cmake >= 2.6.2
- make install/fast
- kdesdk-4.1.2-kdecore.patch upstreamed, dropped

* Wed Nov 12 2008 Than Ngo <than@redhat.com> 4.1.3-1
- 4.1.3

* Wed Oct 22 2008 Than Ngo <than@redhat.com> 4.1.2-4
- check if the document has been saved, if not ask the user
  to save the change or close without saving

* Wed Oct 22 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-3
- -utils should not depend on kdelibs etc (#467984)

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-2
- make VERBOSE=1
- respin against new(er) kde-filesystem

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- 4.1.2

* Wed Sep 24 2008 Than Ngo <than@redhat.com> 4.1.1-2
- show quit in the menu

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Wed Jul 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-2
- fix -utils dep issues

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-1
- 4.0.99

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98

* Sun Jul 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-1
- 4.0.85

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Sat Jun 21 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.83-2
- drop upstreamed rh#433399 patch

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.82-1
- 4.0.82

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta1

* Fri May 16 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.72-2
- %%description: +kate

* Tue May 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-1
- update to 4.0.72
- Obsoletes/Provides kaider (now part of kdesdk, renamed to lokalize)
- add lokalize to description and file list
- add BR strigi-devel for lokalize
- add BR boost-devel (now needed by Umbrello)

* Fri Apr 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-5
- Requires: kdesdk-utils

* Fri Apr 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-4
- utils: po2xml, xml2pot (#432443)

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-3
- rebuild (again) for the fixed %%{_kde4_buildtype}

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-2
- rebuild for NDEBUG and _kde4_libexecdir

* Fri Mar 28 2008 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3

* Thu Feb 28 2008 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2

* Wed Feb 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-2
- kate appears in Applications -> Other (#433399)

* Thu Jan 31 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-1
- kde-4.0.1

* Tue Jan 08 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.0-1
- update to 4.0.0
- drop upstreamed fix-kompare patch
- update file list (no more katesessionmenu.desktop)

* Wed Dec 19 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-8
- update Kompare from SVN (rev 750443)

* Sun Dec 16 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-7
- don't look for libkompare*part.so in %%{_kde4_libdir}
- don't list D-Bus interfaces twice in file list
- build Kompare documentation

* Sun Dec 16 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-6
- update Kompare from SVN (rev 748928)
- Kompare now installs unversioned (private) shared libs, package them properly

* Wed Dec 12 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-5
- rebuild for changed _kde4_includedir

* Tue Dec 11 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-4
- build Kompare's static convenience libraries with -fPIC

* Mon Dec 10 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-3
- updated fix-kompare patch (rev 6)

* Mon Dec 10 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-2
- updated fix-kompare patch (rev 5)

* Sat Dec 08 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-1
- update to 3.97.0 (KDE 4.0 RC2)

* Fri Dec 07 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.96.2-3
- separate -libs subpackage
- remove X11 BRs which are now required by kdelibs-devel

* Thu Dec 06 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.96.2-2
- drop kbabel from description (not actually there)
- reenable kompare, fix its build and porting bugs (kde#153463)
- add missing BR subversion-devel, add files for kio_svn to list
- add missing BR binutils-devel (for libiberty), add files for kmtrace to list

* Fri Nov 30 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.2-1
- kde-3.96.2

* Sat Nov 24 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.1-1
- kde-3.96.1

* Mon Nov 19 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.0-2
- (Build)Require: kdebase-workspace(-devel) (for kate)
- re-enable kate
- BR: kde-filesystem >= 4

* Sun Nov 18 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.0-1
- Initial version for Fedora
