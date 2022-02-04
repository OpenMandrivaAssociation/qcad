# cb - 20181202 - lto causes rcc error 'no data signature found'
%define _disable_lto 1
%define _empty_manifest_terminate_build 0

Summary:	A professional CAD system
Name:		qcad
Version:	3.27.1.6
Release:	1
Group:		Graphics
License:	GPLv3 with exceptions, CC-BY, GPLv2+, LGPLv2.1, BSD
URL:		http://www.qcad.org
Source0:	https://github.com/qcad/qcad/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	qt5-devel
BuildRequires:	pkgconfig(Qt5WebKitWidgets)
BuildRequires:	pkgconfig(Qt5Script)
BuildRequires:  pkgconfig(Qt5ScriptTools)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5XmlPatterns)
BuildRequires:	pkgconfig(Qt5Help)
BuildRequires:	pkgconfig(Qt5UiTools)
BuildRequires:	pkgconfig(Qt5Designer)
BuildRequires:	cmake(Qt5WebEngineWidgets)
BuildRequires:	cmake(Qt5ScriptTools)

BuildRequires:	quazip-devel
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(zlib)

BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Designer)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5OpenGL)
BuildRequires:  pkgconfig(Qt5PrintSupport)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5Script)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5WebChannel)
BuildRequires:  pkgconfig(Qt5WebEngine)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(Qt5XmlPatterns)
BuildRequires:  pkgconfig(Qt5ScriptTools)
BuildRequires:  pkgconfig(Qt5Help)
BuildRequires:  pkgconfig(glu)

%description
QCad is a professional CAD System. With QCad you can easily construct
and change drawings with ISO-text and many other features and save
them as DXF-files. These DXF-files are the interface to many
CAD-systems such as AutoCAD(TM) and many others.

%prep
%autosetup -p1
find . -name ".gitignore" -delete
# Use system quazip
rm -rf src/3rdparty/quazip/src
# Adapt qtscriptgenerator to current Qt
mkdir src/3rdparty/qt-labs-qtscriptgenerator-5.15.3
sed -e 's,5.15.2,5.15.3,g' src/3rdparty/qt-labs-qtscriptgenerator-5.15.2/qt-labs-qtscriptgenerator-5.15.2.pro >src/3rdparty/qt-labs-qtscriptgenerator-5.15.3/qt-labs-qtscriptgenerator-5.15.3.pro

qmake-qt5 -makefile CONFIG+=release %{name}.pro \
 QMAKE_CFLAGS_RELEASE="%{optflags} %(pkg-config --cflags Qt5UiTools) -I$PWD/src/3rdparty/spatialindexnavel/include" \
 QMAKE_CXXFLAGS_RELEASE="%{optflags} %(pkg-config --cflags Qt5UiTools) -I$PWD/src/3rdparty/spatialindexnavel/include" \
 QMAKE_LFLAGS="%{optflags} -Wl,-rpath -Wl,%{_libdir}/%{name}" \
 LFLAGS="%{optflags} -Wl,-rpath -Wl,%{_libdir}/%{name}"

%build
%make_build

%install
mkdir -p %{buildroot}%{_libdir}/%{name}/ts
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
mkdir -p %{buildroot}%{_libdir}/qt5/plugins/codecs
mkdir -p %{buildroot}%{_libdir}/qt5/plugins/script
mkdir -p %{buildroot}%{_libdir}/qt5/plugins/designer
mkdir -p %{buildroot}%{_libdir}/qt5/plugins/imageformats
mkdir -p %{buildroot}%{_libdir}/qt5/plugins/sqldrivers
mkdir -p %{buildroot}%{_libdir}/%{name}/plugins/codecs
mkdir -p %{buildroot}%{_libdir}/%{name}/plugins/designer
mkdir -p %{buildroot}%{_libdir}/%{name}/plugins/imageformats
mkdir -p %{buildroot}%{_libdir}/%{name}/plugins/sqldrivers
mkdir -p %{buildroot}%{_libdir}/%{name}/plugins/script
mkdir -p %{buildroot}%{_libdir}/%{name}/plugins/printsupport
 
## Install fonts
cp -a fonts %{buildroot}%{_libdir}/%{name}
 
# Unbundle vlgothic-fonts
ln -sf %{_fontbasedir}/vlgothic/VL-Gothic-Regular.ttf %{buildroot}%{_libdir}/%{name}/fonts/VL-Gothic-Regular.ttf
 
# Unbundle dejavu-sans-fonts
for i in `ls %{buildroot}%{_libdir}/%{name}/fonts/qt | grep DejaVuSans`; do
 ln -sf %{_fontbasedir}/dejavu/$i %{buildroot}%{_libdir}/%{name}/fonts/qt/$i
done
##
 
cp -a patterns %{buildroot}%{_libdir}/%{name}
cp -a themes %{buildroot}%{_libdir}/%{name}
cp -a libraries %{buildroot}%{_libdir}/%{name}
cp -a scripts %{buildroot}%{_libdir}/%{name}
cp -a plugins %{buildroot}%{_libdir}/%{name}
cp -a linetypes %{buildroot}%{_libdir}/%{name}
 
# This file is required for Help's "Show Readme" menu choice
cp -p readme.txt %{buildroot}%{_libdir}/%{name}
 
install -pm 644 ts/qcad*.qm %{buildroot}%{_libdir}/%{name}/ts
ln -sf %{_libdir}/qt5/plugins/codecs/libqcncodecs.so %{buildroot}%{_libdir}/%{name}/plugins/codecs/libqcncodecs.so
ln -sf %{_libdir}/qt5/plugins/codecs/libqjpcodecs.so %{buildroot}%{_libdir}/%{name}/plugins/codecs/libqjpcodecs.so
ln -sf %{_libdir}/qt5/plugins/codecs/libqkrcodecs.so %{buildroot}%{_libdir}/%{name}/plugins/codecs/libqkrcodecs.so
ln -sf %{_libdir}/qt5/plugins/codecs/libqtwcodecs.so %{buildroot}%{_libdir}/%{name}/plugins/codecs/libqtwcodecs.so
 
ln -sf %{_libdir}/qt5/plugins/designer/libqwebview.so %{buildroot}%{_libdir}/%{name}/plugins/designer/libqwebview.so
 
ln -sf %{_libdir}/qt5/plugins/imageformats/libqgif.so %{buildroot}%{_libdir}/%{name}/plugins/imageformats/libqgif.so
ln -sf %{_libdir}/qt5/plugins/imageformats/libqico.so %{buildroot}%{_libdir}/%{name}/plugins/imageformats/libqico.so
ln -sf %{_libdir}/qt5/plugins/imageformats/libqjpeg.so %{buildroot}%{_libdir}/%{name}/plugins/imageformats/libqjpeg.so
ln -sf %{_libdir}/qt5/plugins/imageformats/libqsvg.so %{buildroot}%{_libdir}/%{name}/plugins/imageformats/libqsvg.so
ln -sf %{_libdir}/qt5/plugins/imageformats/libqtga.so %{buildroot}%{_libdir}/%{name}/plugins/imageformats/libqtga.so
ln -sf %{_libdir}/qt5/plugins/imageformats/libqtiff.so %{buildroot}%{_libdir}/%{name}/plugins/imageformats/libqtiff.so
 
ln -sf %{_libdir}/qt5/plugins/sqldrivers/libqsqlite.so %{buildroot}%{_libdir}/%{name}/plugins/sqldrivers/libqsqlite.so
ln -sf %{_libdir}/qt5/plugins/printsupport/libcupsprintersupport.so %{buildroot}%{_libdir}/%{name}/plugins/printsupport/libcupsprintersupport.so
 
install -pm 644 scripts/qcad_icon.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -pm 755 release/*.so %{buildroot}%{_libdir}/%{name}
install -pm 755 release/%{name}-bin %{buildroot}%{_libdir}/%{name}
install -pm 644 readme.txt %{buildroot}%{_libdir}/%{name}
 
install -pm 644 qcad.1 %{buildroot}%{_mandir}/man1
install -pm 644 scripts/%{name}_icon.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
 
find %{buildroot}%{_libdir}/%{name} -name ".gitignore" -delete
find %{buildroot}%{_libdir}/%{name} -name "readme.txt" -delete
find %{buildroot}%{_libdir}/%{name} -name "Makefile" -delete
 
pushd %{buildroot}%{_libdir}/%{name}
for i in `find . -type f \( -name "*.so*" -o -name "qcad-bin" \)`; do
  chmod -c 755 $i
  chrpath -r %{_libdir}/%{name} $i
done
popd
 
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/sh
export \
LD_LIBRARY_PATH=%{_libdir}/%{name}:%{_libdir}/%{name}/plugins/script \
QTLIB=%{_libdir} \
QTDIR=%{_libdir}/qt5 \
QTINC=%{_includedir}/qt5 \
WISECONFIGDIR=%{_datadir}/wise2 \
QT_QPA_PLATFORM=xcb \
PATH=%{_libdir}:%{_libdir}/%{name}
%{_libdir}/%{name}/%{name}-bin "\$@"
EOF
chmod a+x %{buildroot}%{_bindir}/%{name}
 
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
Icon=qcad_icon
Terminal=false
Type=Application
Categories=Office;Chart;Qt;
StartupNotify=true
EOF

%files
%doc readme.txt LICENSE.txt README.md gpl-3.0.txt cc-by-3.0.txt gpl-3.0-exceptions.txt
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/qcad.svg
%{_mandir}/man1/qcad.1*
%{_datadir}/pixmaps/qcad.png
