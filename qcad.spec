%define	name	qcad
%define	version	2.0.5.0
%define manver	2.0.4.0-1
%define	release	3

Summary: 	A professional CAD system
Name: 		%{name}
Version: 	%{version}
Release: 	%mkrel %{release}
Source0:	http://www.ribbonsoft.com/archives/qcad/qcad-%{version}-1-community.src.tar.bz2
Source1: 	icons-%{name}.tar.bz2
Source2:	http://www.ribbonsoft.com/archives/qcad/qcad-manual-en-%{manver}.html.zip
Patch0:		qcad-2.0.4.0-1-x86_64.patch
Patch1:		qcad-2.0.4.0-1-assistant.patch
Patch2:		qcad-2.0.5.0-1-path.patch
Patch3:		qcad-2.0.4.0-1-manfix.patch
Patch4:		qcad-2.0.5.0-1-nopedantic.patch
Patch5:		qcad-2.0.5.0-1-release_translations.patch
URL: 		http://www.qcad.org
License: 	GPL 
Group: 		Graphics
BuildRequires: 	XFree86-devel
BuildRequires:	jpeg-devel
BuildRequires:  png-devel
BuildRequires:  zlib-devel
BuildRequires:	qt3-devel
BuildRequires:	qt3-static-devel
BuildRequires:	unzip
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root

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
perl -pi -e 's!\@BINDIR\@!%_bindir!;s!\@DATADIR\@!%_datadir!' qcad/src/qc_applicationwindow.cpp
chmod +x scripts/release_translations.sh

%build
# QTDIR is always set to /usr/lib/qt3
export QTDIR=%{_prefix}/lib/qt3
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
rm -rf $RPM_BUILD_ROOT
install -m 755 -d $RPM_BUILD_ROOT%_bindir \
	$RPM_BUILD_ROOT%_libdir/qcad \
	$RPM_BUILD_ROOT%_iconsdir \
        $RPM_BUILD_ROOT%_datadir/%name \
	$RPM_BUILD_ROOT%_datadir/qcad/doc \
	$RPM_BUILD_ROOT%_datadir/qcad/library

pushd $RPM_BUILD_DIR/%{name}-%{version}-1-community.src/qcad
	cp -p qcad $RPM_BUILD_ROOT/%_bindir/
	for i in {data,fonts,library,machines,patterns,qm}; do
		cp -r $i $RPM_BUILD_ROOT/%_datadir/%name
	done
popd
cp -rfp qcad-manual-en-%{manver}.html/* $RPM_BUILD_ROOT/%_datadir/qcad/doc

# icons
tar xjf %SOURCE1 -C $RPM_BUILD_ROOT%{_iconsdir}

# menu
install -m 755 -d $RPM_BUILD_ROOT/%_menudir
cat > $RPM_BUILD_ROOT%_menudir/qcad <<EOF
?package(qcad):\
needs="x11"\
section="Office/Graphs"\
title="Qcad"\
command="%{_bindir}/qcad"\
icon=%{name}.png \
%if %{mdkversion} >= 200610
xdg=true \
%endif
longtitle="A professional CAD system"
EOF

# desktop
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Qcad
Comment=A professional CAD system
Exec=%{_bindir}/qcad %f
Icon=qcad
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Office-Graphs;Office;Chart;
StartupNotify=true
Encoding=UTF-8
EOF

# fix permissions
find $RPM_BUILD_ROOT%_bindir/ -type d -print0 | xargs -0 chmod 755
find $RPM_BUILD_ROOT%_libdir/ -type d -print0 | xargs -0 chmod 755
find $RPM_BUILD_ROOT%_datadir/ -type d -print0 | xargs -0 chmod 755
find $RPM_BUILD_ROOT%_menudir/ -type f  -print0 | xargs -0 chmod 644
find $RPM_BUILD_ROOT%_datadir/ -type f  -print0 | xargs -0 chmod 644

# remove not packaged files
rm $RPM_BUILD_ROOT%_includedir -rf

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc qcad/README 
%attr(755,root,root) %{_bindir}/qcad
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png
%{_menudir}/qcad
%{_datadir}/qcad/*
%{_datadir}/applications/*.desktop


