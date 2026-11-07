# Please be aware that the the two additional archives are required to build qcad for QT6 
# as some functionality (qtscript) was removed one of the archives replaces that.
# Both are required for the build and they must be in separate directories at the root of the build 
# as there are cross references in the cmake files which will break if this is not done. 

#define _empty_manifest_terminate_build 0
%define _build_id_links none
%global _QCAD_DIR %{_libdir}/%{name}

#%%global qt_current_version %%(qtpaths --qt-version)

Summary:	A professional CAD system
Name:		qcad
Version:	3.33.1.0
Release:	1
Group:		Graphics
License:	GPLv3 with exceptions, CC-BY, GPLv2+, LGPLv2.1, BSD
URL:		https://www.qcad.org
Source0:	https://github.com/qcad/qcad/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	https://github.com/qcad/qcadjsapi/archive/refs/tags/qtjsapi-%{version}.tar.gz
Source2:	https://github.com/qcad/qtjsapi/archive/refs/tags/qcadjsapi-%{version}.tar.gz
# (tpg) https://bugreports.qt.io/browse/QTBUG-73834
# dropped (no longer applies): Patch0:		qcad-fix-lto.patch
Patch1:		qcad-3.27.8.7-fix-link-stage.patch
Patch2:		fix-X11-linking.patch
Patch4:		fix-qcadjsapi-linking.patch
Patch3:		fix-cmake-versions.patch
BuildRequires:	gnutar
BuildRequires:	ninja
BuildRequires:	fontpackages-devel
BuildRequires:	qt6-qtimageformats
BuildRequires:	qt6-qttools
BuildRequires:	pkgconfig(appstream)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libtsm)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(Qt6Concurrent)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Designer)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Help)
BuildRequires:	pkgconfig(Qt6Network)
BuildRequires:	pkgconfig(Qt6OpenGL)
BuildRequires:	pkgconfig(Qt6PrintSupport)
BuildRequires:	pkgconfig(Qt6Qml)
BuildRequires:	pkgconfig(Qt6Quick)
BuildRequires:	pkgconfig(Qt6Sql)
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:	cmake(Qt6UiTools)
BuildRequires:	pkgconfig(Qt6WebChannel)
BuildRequires:	pkgconfig(Qt6WebEngineCore)
BuildRequires:	pkgconfig(Qt6WebEngineWidgets)
#BuildRequires:	pkgconfig(Qt6WebKitWidgets)
BuildRequires:	pkgconfig(Qt6Xml)
#BuildRequires:	pkgconfig(Qt6XmlPatterns)
BuildRequires:	pkgconfig(Qt6Help)
BuildRequires:	cmake(Core5Compat)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(zlib)
# (unpackaged)
BuildRequires:  spatialindex-devel

Requires:	fonts-ttf-dejavu
Requires:	qt6-qtimageformats
Requires:	qt6-qttranslations
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
#%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/qcad.svg
%{_QCAD_DIR}
%{_datadir}/icons/qcad.png
%{_includedir}/OpenNURBS/*.h
%{_includedir}/opennurbsStatic/*.h
/usr/lib/libandroid_uuid.a
/usr/lib/libopennurbs.so
/usr/lib/libopennurbsStatic.a
/usr/lib/libopennurbs_public_freetype.a
/usr/lib/libzlib.a
#%{_datadir}/pixmaps/qcad.png
%doc %{_mandir}/man1/qcad.1*

#---------------------------------------------------------------------------

%prep

%setup -n qcad
mkdir -p %{_builddir}/qtjsapi
mkdir -p %{_builddir}/qcadjsapi
%patch -p1  1 2 3

cd %{_builddir}/qtjsapi
gtar -xvf  %{_sourcedir}/qtjsapi-%{version}.tar.gz --strip=1
cd %{_builddir}/qcadjsapi
gtar -xvf  %{_sourcedir}/qcadjsapi-%{version}.tar.gz --strip=1
%patch -p1 4

find . -name ".gitignore" -delete
# use system libs
#  quazip (unused)
rm -rf src/3rdparty/quazip/src
#  spatialindex (unpackaged)
rm -rf src/3rdparty/spatialindexnavel/include/spatialindex

%build


export CMAKE_GENERATOR=Ninja
export CC=gcc
export CXX=g++

cd %{builddir}/qcad
%cmake  -DBUILD_QT6:BOOL=ON -DCMAKE_BUILD_TYPE:STRING=Release -Dractivated:BOOL=ON \
       -DCMAKE_CFLAGS_RELEASE="%{build_cflags} %(pkg-config --cflags Qt6UiTools)" \
       -DCMAKE_CXXFLAGS_RELEASE="%{build_cxxflags} %(pkg-config --cflags Qt6UiTools)" \
       -DVulkan_GLSLC_EXECUTABLE:FILEPATH=%{_bindir}/glslang -DVulkan_GLSLANG_VALIDATOR_EXECUTABLE:FILEPATH=%{_bindir}/glslangValidator \
       -DCMAKE_VERBOSE_MAKEFILE:BOOL=TRUE -DBUILD_SHARED_LIBS:BOOL=OFF

%ninja_build


cd %{builddir}/qtjsapi
%cmake  -DBUILD_QT6:BOOL=ON -DCMAKE_BUILD_TYPE:STRING=Release -Dractivated:BOOL=1 \
       -DCMAKE_CFLAGS_RELEASE="%{build_cflags} %(pkg-config --cflags Qt6UiTools)" \
       -DCMAKE_CXXFLAGS_RELEASE="%{build_cxxflags} %(pkg-config --cflags Qt6UiTools)" \
       -DVulkan_GLSLC_EXECUTABLE:FILEPATH=%{_bindir}/glslang -DVulkan_GLSLANG_VALIDATOR_EXECUTABLE:FILEPATH=%{_bindir}/glslangValidator \
       -DCMAKE_VERBOSE_MAKEFILE:BOOL=TRUE -DBUILD_SHARED_LIBS:BOOL=ON

%ninja_build

cd %{builddir}/qcadjsapi

%cmake  -DBUILD_QT6:BOOL=ON -DCMAKE_BUILD_TYPE:STRING=Release -Dractivated:BOOL=1 \
       -DCMAKE_CFLAGS_RELEASE="%{build_cflags} %(pkg-config --cflags Qt6UiTools)" \
       -DCMAKE_CXXFLAGS_RELEASE="%{build_cxxflags} %(pkg-config --cflags Qt6UiTools)" \
       -DVulkan_GLSLC_EXECUTABLE:FILEPATH=%{_bindir}/glslang -DVulkan_GLSLANG_VALIDATOR_EXECUTABLE:FILEPATH=%{_bindir}/glslangValidator \
       -DCMAKE_VERBOSE_MAKEFILE:BOOL=TRUE -DBUILD_SHARED_LIBS:BOOL=ON

%ninja_build



%install
%ninja_install -C %{builddir}/qcad/build
# libs
install -dm 0755 %{buildroot}%{_libdir}/%{name}
install -pm 0755 release/%{name}-bin %{buildroot}%{_libdir}/%{name}
install -pm 0755 release/*.so %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}/usr/lib64/%{name}/plugins/imageformats
mkdir -p %{buildroot}/usr/lib64/%{name}/plugins/sqldrivers
mkdir -p %{buildroot}/usr/lib64/%{name}/plugins/script
mkdir -p %{buildroot}/usr/lib64/%{name}/plugins/printsupport
# link plugins from system qt
install -dm 0755 %{buildroot}%{_libdir}/%{name}/
cp -r plugins %{buildroot}%{_libdir}/%{name}/
for qtplugin in imageformats sqldrivers printsupport; do
    for sofiles in /usr/lib64/qt6/plugins/${qtplugin}/*.so; do
	ln -srf ${sofiles} %{buildroot}%{_libdir}/%{name}/plugins/${qtplugin}/${sofiles##/*/}
    done
done

# link qt modules
for qtmodules in platforminputcontexts platforms xcbglintegrations; do
    ln -srf %{_qt6_plugindir}/${qtmodules} %{buildroot}%{_libdir}/%{name}/plugins/${qtmodules}
done

# link qt wayland modules
for qtwayland in wayland-decoration-client wayland-graphics-integration-client wayland-graphics-integration-server wayland-shell-integration; do
    ln -srf %{_qt6_plugindir}/${qtwayland} %{buildroot}%{_libdir}/%{name}/${qtwayland}
done

# fix perms
pushd %{buildroot}%{_libdir}/%{name}
for i in $(find . -type f \( -name "*.so*" -o -name "%{name}-bin" \)); do
    chmod -c 0755 $i
#	chrpath -r %{_libdir}/%{name} $i
done
popd

# data
install -dm 0755 %{buildroot}%{_datadir}/%{name}
for d in examples fonts libraries linetypes patterns scripts themes ts; do
    cp -r $d %{buildroot}%{_datadir}/%{name}/
done

# unbundle fonts
#   vlgothic-fonts (unpackagd)
#ln -sf %{_fontbasedir}/vlgothic/VL-Gothic-Regular.ttf %{buildroot}%{_libdir}/%{name}/fonts/VL-Gothic-Regular.ttf
#   dejavu-sans-fonts
for f in $(ls %{buildroot}%{_datadir}/%{name}/fonts/qt | grep DejaVuSans); do
    ln -srf %{_fontbasedir}/dejavu/$f %{buildroot}%{_datadir}/%{name}/fonts/qt/$f
done

# launcher
install -dm 0755 %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/sh
export LD_LIBRARY_PATH=%{_libdir}/%{name}:%{_libdir}/%{name}/plugins/script:\$LD_LIBRARY_PATH
export QTLIB=%{_libdir}
export QTDIR=%{_libdir}/qt6
export QTINC=%{_includedir}/qt6
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
install -Dm 644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

# documentation for help system
install -Dm 0644 readme.txt %{buildroot}%{_datadir}/%{name}/readme.txt
#other docs
mkdir -p %{buildroot}/%{_datadir}/doc/%{name}
install -Dm 0644 LICENSE.txt README.md gpl-3.0.txt cc-by-3.0.txt gpl-3.0-exceptions.txt   %{buildroot}/%{_datadir}/doc/%{name}/



# clean
find %{buildroot}%{_datadir}/%{name} \( -name '*.pri' -or -name '*.pro' -or -name '*.ts' \) -delete
find %{buildroot}%{_datadir}/%{name} \( -name 'Makefile*' -or -name '.gitignore' \) -delete
