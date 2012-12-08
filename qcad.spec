%define manver	2.0.4.0-1

Summary:	A professional CAD system
Name:		qcad
Version:	2.0.5.0
Release:	11
License: 	GPL
Group: 		Graphics
URL: 		http://www.qcad.org
Source0:	http://www.ribbonsoft.com/archives/qcad/qcad-%{version}-1-community.src.tar.bz2
Source1:	icons-%{name}.tar.bz2
Source2:	http://www.ribbonsoft.com/archives/qcad/qcad-manual-en-%{manver}.html.zip
Patch0:		qcad-2.0.4.0-1-x86_64.patch
Patch1:		qcad-2.0.4.0-1-assistant.patch
Patch2:		qcad-2.0.5.0-1-path.patch
Patch3:		qcad-2.0.4.0-1-manfix.patch
Patch4:		qcad-2.0.5.0-1-nopedantic.patch
Patch5:		qcad-2.0.5.0-1-release_translations.patch
Patch6:		qcad-2.0.5.0-1-gcc43.patch
BuildRequires:	qt3-devel
BuildRequires:	unzip

%description
QCad is a professional CAD System. With QCad you can easily construct
and change drawings with ISO-text and many other features and save
them as DXF-files. These DXF-files are the interface to many
CAD-systems such as AutoCAD(TM) and many others.

%prep
%setup -q -n %{name}-%{version}-1-community.src
%setup -q -T -D -a 2 -n %{name}-%{version}-1-community.src
%patch0 -p1 -b .x86_64
%patch1 -p1 -b .assistant
%patch2 -p1 -b .path
%patch3 -p1 -b .manfix
%patch4 -p1 -b .nopedantic
%patch5 -p1 -b .rtsh
%patch6 -p1 -b .gcc43
perl -pi -e 's!\@BINDIR\@!%{_bindir}!;s!\@DATADIR\@!%{_datadir}!' qcad/src/qc_applicationwindow.cpp
chmod +x scripts/release_translations.sh

%build
# QTDIR is always set to /usr/lib/qt3
export QTDIR=%{qt3dir}
export PATH=$PATH:$QTDIR/bin
%ifarch x86_64
export QMAKESPEC=$QTDIR/mkspecs/linux-g++-64
%else
export QMAKESPEC=$QTDIR/mkspecs/linux-g++
%endif

pushd scripts
CFLAGS="%{optflags}" \
CXXFLAGS="%{optflags}" \
./build_qcad.sh
popd

%install
install -m 755 -d %{buildroot}%{_bindir} \
	%{buildroot}%{_libdir}/qcad \
	%{buildroot}%{_iconsdir} \
        %{buildroot}%{_datadir}/%{name} \
	%{buildroot}%{_datadir}/qcad/doc \
	%{buildroot}%{_datadir}/qcad/library

pushd qcad
	cp -p qcad %{buildroot}%{_bindir}/
	for i in {data,fonts,library,machines,patterns,qm}; do
		cp -r $i %{buildroot}%{_datadir}/%{name}
	done
popd
cp -rfp qcad-manual-en-%{manver}.html/* %{buildroot}%{_datadir}/qcad/doc

# icons
tar xjf %{SOURCE1} -C %{buildroot}%{_iconsdir}

# desktop
install -m 755 -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Qcad
Comment=A professional CAD system
Exec=%{_bindir}/qcad %f
Icon=qcad
Terminal=false
Type=Application
Categories=Office;Chart;Qt;
StartupNotify=true
EOF

# fix permissions
find %{buildroot}%{_bindir}/ -type d -print0 | xargs -0 chmod 755
find %{buildroot}%{_libdir}/ -type d -print0 | xargs -0 chmod 755
find %{buildroot}%{_datadir}/ -type d -print0 | xargs -0 chmod 755
find %{buildroot}%{_datadir}/ -type f  -print0 | xargs -0 chmod 644

# remove not packaged files
rm -rf %{buildroot}%{_includedir}

%files
%doc qcad/README
%attr(755,root,root) %{_bindir}/qcad
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png
%{_datadir}/qcad/*
%{_datadir}/applications/*.desktop




%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0.5.0-10mdv2011.0
+ Revision: 669368
- mass rebuild

* Thu Feb 03 2011 Funda Wang <fwang@mandriva.org> 2.0.5.0-9
+ Revision: 635602
- only qt3 is required
- tighten BR

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.5.0-8mdv2011.0
+ Revision: 607260
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.5.0-6mdv2010.1
+ Revision: 523881
- rebuilt for 2010.1

* Tue Aug 05 2008 Funda Wang <fwang@mandriva.org> 2.0.5.0-5mdv2009.0
+ Revision: 263977
- add gcc 4.3 patch from fedora
- use xdg-open rather than gnome-open

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.5.0-5mdv2008.1
+ Revision: 179396
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Sun Sep 16 2007 Emmanuel Andry <eandry@mandriva.org> 2.0.5.0-4mdv2008.0
+ Revision: 88607
- drop old menu

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'
    - buildrequires obsoletes buildprereq


* Thu Mar 15 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 2.0.5.0-3mdv2007.1
+ Revision: 144419
- Added fix for bug 26993.
- Unbzip2 patches.

* Mon Feb 19 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 2.0.5.0-2mdv2007.1
+ Revision: 122914
- Import qcad

* Sat Feb 17 2007 Giuseppe Ghibò <ghibo@mandriva.com> 2.0.5.0-2mdv2007.1
- xdg menu.

* Sun May 07 2006 Giuseppe Ghibò <ghibo@mandriva.com> 2.0.5.0-1mdk
- qcad-2.0.5.0-1-nopedantic.patch.bz2.
- Provide CFLAGS|CXXFLAGS to build_cad.sh.
- Added Patch5 for providing .qm files.

* Sun May 07 2006 Giuseppe Ghibò <ghibo@mandriva.com> 2.0.4.0-4mdk
- Removed MDK920 conditional flags.
- Merged Patch1 from FC5 (fix call of QT assistant).
- Added Patch2 to fix doc and assistant path.
- Merged Patch3 from FC5 (fix manual).
- Added HTML Manual.
- Added Patch4 to allow 'long long' type.

* Sun May 07 2006 Giuseppe Ghibò <ghibo@mandriva.coM> 2.0.4.0-3mdk
- Added fix for x86-64 (Patch2).
- Cleaned SPEC file of unused things.

* Sun Jul 10 2005 Giuseppe Ghibò <ghibo@mandriva.com> 2.0.4.0-2mdk
- Rebuilt.

* Thu Oct 28 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 2.0.4.0-1mdk
- 2.0.4.0

* Mon Jul 19 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.0.3.3-1mdk
- build with gcc 3.4 (patch1)
- 2.0.3.3

* Sat May 08 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 2.0.3.1-1mdk
- 2.0.3.1

* Fri Apr 16 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.1.3-6mdk
- really use mdkversion, other fixlets

* Thu Apr 01 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 2.0.1.3-5mdk
- Use mdkversion

