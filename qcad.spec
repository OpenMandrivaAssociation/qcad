# cb - 20181202 - lto causes rcc error 'no data signature found'
%define _disable_lto 1

Summary:	A professional CAD system
Name:		qcad
Version:	3.25.2.12
Release:	1
Group:		Graphics
License:	GPLv3 with exceptions, CC-BY, GPLv2+, LGPLv2.1, BSD
URL:		http://www.qcad.org
Source0:	https://github.com/qcad/qcad/archive/v%{version}.tar.gz

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
%setup -q
%autopatch -p1
find . -name ".gitignore" -delete
sed -e 's|$${QT_VERSION}|5.5.0|g' \
      -i src/3rdparty/3rdparty.pro # Don't require specific Qt version
rm -rf src/3rdparty/quazip/src

mkdir -p src/3rdparty/qt-labs-qtscriptgenerator-5.13.1/
cat <<EOF > qt-labs-qtscriptgenerator-5.13.1.pro
include( ../../../shared.pri )

SUBDIRS = ../qt-labs-qtscriptgenerator-5.5.0/qtbindings
TEMPLATE = subdirs
EOF

mv qt-labs-qtscriptgenerator-5.13.1.pro src/3rdparty/qt-labs-qtscriptgenerator-5.13.1/

%build
%qmake_qt5
%make

%install

# remove project files
find . \( -name '*.pri' -or -name '.pro' -or -name '*.ts' \) -delete
find . \( -name 'Makefile*' -name '.gitignore' \) -delete

install -dm755 %{buildroot}%{_datadir}/%{name}
cp -r examples fonts libraries patterns plugins scripts ts %{buildroot}%{_datadir}/%{name}
cp release/* %{buildroot}%{_datadir}/%{name}

# qt
for sofiles in %{_qt5_plugindir}/imageformats/*.so
do
    ln -sf ${sofiles} %{buildroot}%{_datadir}/%{name}/plugins/imageformats/${sofiles##/*/}
done

for sofiles in %{_qt5_plugindir}/sqldrivers/*.so
do
    ln -sf ${sofiles} %{buildroot}%{_datadir}/%{name}/plugins/sqldrivers/${sofiles##/*/}
done

install -Dm644 scripts/qcad_icon.png %{buildroot}%{_iconsdir}/qcad_icon.png

install -dm0755 %{buildroot}%{_bindir}
echo -e '#!/bin/sh\ncd %{_datadir}/%{name}\nLD_LIBRARY_PATH=`pwd`:$LD_LIBRARY_PATH exec ./qcad-bin' > %{buildroot}%{_bindir}/%{name}
chmod 0755 %{buildroot}%{_bindir}/%{name}

rm -f %{buildroot}%{_datadir}/%{name}/*.a

install -dm0755 %{buildroot}%{_libdir}
mv %{buildroot}%{_datadir}/%{name}/*.so %{buildroot}%{_libdir}

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
%{_libdir}/*.so
%{_iconsdir}/*.png
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_datadir}/applications/*.desktop
