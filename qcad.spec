%define manver	2.0.4.0-1

Summary:	A professional CAD system
Name:		qcad
Version:	2.0.5.0
Release:	14
License:	GPLv2
Group:		Graphics
Url:		http://www.qcad.org
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
%setup -qn %{name}-%{version}-1-community.src
%setup -q -T -D -a 2 -n %{name}-%{version}-1-community.src
%apply_patches

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

