# cb - 20181202 - lto causes rcc error 'no data signature found'
%define _disable_lto 1
#define _empty_manifest_terminate_build 0

%global qt_version %(qtpaths --qt-version)

Summary:	A professional CAD system
Name:		qcad
Version:	3.27.1.6
Release:	2
Group:		Graphics
License:	GPLv3 with exceptions, CC-BY, GPLv2+, LGPLv2.1, BSD
URL:		http://www.qcad.org
Source0:	https://github.com/qcad/qcad/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	fontpackages-devel
BuildRequires:	qt5-devel
BuildRequires:	qt5-qtimageformats
BuildRequires:	qt5-qttools
BuildRequires:	pkgconfig(appstream-glib)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libtsm)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Designer)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Help)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5Qml)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5Script)
BuildRequires:	pkgconfig(Qt5ScriptTools)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5UiTools)
BuildRequires:	pkgconfig(Qt5WebChannel)
BuildRequires:	pkgconfig(Qt5WebEngine)
BuildRequires:	pkgconfig(Qt5WebEngineWidgets)
BuildRequires:	pkgconfig(Qt5WebKitWidgets)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(Qt5XmlPatterns)
BuildRequires:	pkgconfig(Qt5ScriptTools)
BuildRequires:	pkgconfig(Qt5Help)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(zlib)
# (unpackaged)
#BuildRequires: spatialindex-devel

Requires:	fonts-ttf-dejavu
Requires:	qt5-qtimageformats
Requires:	qt5-qttranslations
#Requires:	vlgothic-fonts
Requires:	wise
 
%description
QCad is a professional CAD System. With QCad you can easily construct
and change drawings with ISO-text and many other features and save
them as DXF-files. These DXF-files are the interface to many
CAD-systems such as AutoCAD(TM) and many others.

%files
%doc readme.txt LICENSE.txt README.md gpl-3.0.txt cc-by-3.0.txt gpl-3.0-exceptions.txt
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/qcad.svg
%{_datadir}/icons/qcad.png
#%{_datadir}/pixmaps/qcad.png
%{_mandir}/man1/qcad.1*

#---------------------------------------------------------------------------

%prep
%autosetup -p1
find . -name ".gitignore" -delete

# use system libs
#  quazip (unused)
#rm -rf src/3rdparty/quazip/src
#  spatialindex (unpackaged)
#rm -rf src/3rdparty/spatialindexnavel/include/spatialindex

# adapt qtscriptgenerator to current Qt
mkdir -p src/3rdparty/qt-labs-qtscriptgenerator-%{qt_version}
#sed -e "s|5.5.0|%{qt_version}|g" src/3rdparty/qt-labs-qtscriptgenerator-5.15.2/qt-labs-qtscriptgenerator-5.15.2.pro > src/3rdparty/qt-labs-qtscriptgenerator-%{qt_version}/qt-labs-qtscriptgenerator-%{qt_version}.pro
cp -fa src/3rdparty/qt-labs-qtscriptgenerator-5.15.2/qt-labs-qtscriptgenerator-5.15.2.pro \
	src/3rdparty/qt-labs-qtscriptgenerator-%{qt_version}/qt-labs-qtscriptgenerator-%{qt_version}.pro

%build
#export CC=gcc
#export CXX=g++

%qmake_qt5
#-makefile CONFIG+=release %{name}.pro \
# QMAKE_CFLAGS_RELEASE="%{optflags} %(pkg-config --cflags Qt5UiTools) -I$PWD/src/3rdparty/spatialindexnavel/include" \
# QMAKE_CXXFLAGS_RELEASE="%{optflags} %(pkg-config --cflags Qt5UiTools) -I$PWD/src/3rdparty/spatialindexnavel/include" \
# QMAKE_LFLAGS="%{optflags} -Wl,-rpath -Wl,%{_libdir}/%{name}" \
# LFLAGS="%{optflags} -Wl,-rpath -Wl,%{_libdir}/%{name}"

%make_build

%install
# libs
install -dm 0755 %{buildroot}%{_libdir}/%{name}
install -pm 0755 release/%{name}-bin %{buildroot}%{_libdir}/%{name}
install -pm 0755 release/*.so %{buildroot}%{_libdir}/%{name}

# link plugins from system qt
install -dm 0755 %{buildroot}%{_libdir}/%{name}/
cp -r plugins %{buildroot}%{_libdir}/%{name}/
for qtplugin in imageformats sqldrivers printsupport
do
	for sofiles in %{_qt5_plugindir}/${qtplugin}/*.so
	do
		ln -sf ${sofiles} %{buildroot}%{_libdir}/%{name}/plugins/${qtplugin}/${sofiles##/*/}
	done
done

# fix perms
pushd %{buildroot}%{_libdir}/%{name}
for i in `find . -type f \( -name "*.so*" -o -name "%{name}-bin" \)`; do
	chmod -c 0755 $i
	#chrpath -r %{_libdir}/%{name} $i
done
popd

# data
install -dm 0755 %{buildroot}%{_datadir}/%{name}
for d in examples fonts libraries linetypes patterns scripts themes ts
do
	cp -r $d %{buildroot}%{_datadir}/%{name}/
done

# unbundle fonts
#   vlgothic-fonts (unpackagd)
#ln -sf %{_fontbasedir}/vlgothic/VL-Gothic-Regular.ttf %{buildroot}%{_libdir}/%{name}/fonts/VL-Gothic-Regular.ttf
#   dejavu-sans-fonts
for f in `ls %{buildroot}%{_datadir}/%{name}/fonts/qt | grep DejaVuSans`
do
	ln -sf %{_fontbasedir}/dejavu/$f %{buildroot}%{_datadir}/%{name}/fonts/qt/$f
done

# launcher
install -dm 0755 %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/sh
export LD_LIBRARY_PATH=%{_libdir}/%{name}:%{_libdir}/%{name}/plugins/script:\$LD_LIBRARY_PATH
export QTLIB=%{_libdir}
export QTDIR=%{_libdir}/qt5
export QTINC=%{_includedir}/qt5
export WISECONFIGDIR=%{_datadir}/wise
export QT_QPA_PLATFORM=xcb
export PATH=%{_libdir}:%{_libdir}/%{name}:%{_datadir}/%{name}:\$PATH
%{_libdir}/%{name}/%{name}-bin "\$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

# icon
install -Dm 0644 scripts/%{name}_icon.png %{buildroot}%{_iconsdir}/%{name}.png
install -Dm 0644 scripts/%{name}_icon.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
 
# desktop
install -m 755 -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=Qcad
Name[ru]=Qcad
Comment=A professional CAD system
Comment[ru]=Профессиональная CAD система
Exec=%{name}
Icon=qcad
Terminal=false
Type=Application
Categories=Office;Chart;Qt;
StartupNotify=true
EOF

# man page
install -Dm644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

# documentation for help system
install -Dm 0644 readme.txt %{buildroot}%{_datadir}/%{name}/readme.txt

# clean
find %{buildroot}%{_datadir}/%{name} \( -name '*.pri' -or -name '*.pro' -or -name '*.ts' \) -delete
find %{buildroot}%{_datadir}/%{name} \( -name 'Makefile*' -or -name '.gitignore' \) -delete

