Name:		vavoom
Version:	1.33
Release:	%mkrel 1
Summary:	Open source port of the DOOM game engine
Source0:	http://dl.sourceforge.net/vavoom/%{name}-%{version}.tar.bz2
Patch0:		vavoom-1.30-linkage.patch
Patch1:		vavoom-1.30-fix-str-fmt.patch
URL:		http://vavoom-engine.com/
Group:		Games/Arcade
License:	GPLv2+
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_net-devel
BuildRequires:	libpng-devel
BuildRequires:	allegro-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	pkgconfig(flac++)
BuildRequires:	libmad-devel
BuildRequires:	openal-devel
BuildRequires:	libmikmod-devel
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	mesagl-devel
BuildRequires:	libjpeg-devel
BuildRequires:	wxgtku-devel
Suggests:	vavoom-vmdl
Suggests:	TiMidity++

%description
Vavoom is an open-source port of Doom, the classic 3D first-person shooter
game.  It adds some extra features to Doom such as translucency
and freelook support.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
# This one line sed command is easier than trying to muck with the Makefile
# to add the proper -D definition.
%__sed -i "s|#define FL_BASEDIR.*|#define FL_BASEDIR \"%{_gamesdatadir}/%{name}\"|" source/files.h

%build
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DBINDIR=%{_gamesbindir} \
	-DDATADIR=%{_gamesdatadir}/%{name} \
	-DWITH_SDL=Y \
	-DWITH_OPENGL=Y \
	-DWITH_OPENAL=Y \
	-DWITH_FLAC=Y \
	-DWITH_ALLEGRO=N

# The Makefile doesn't do parallel builds correctly.
make

%install
%__rm -rf %{buildroot}
%makeinstall_std -C build

%__cat << EOF > %{name}.desktop
[Desktop Entry]
Name=Freedoom
Comment=Freedoom with the Vavoom engine
Exec=vavoom
Icon=arcade_section
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

desktop-file-install --vendor="" \
	--dir %{buildroot}%{_datadir}/applications \
	%{name}.desktop

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc docs/*.log docs/gnu.txt docs/vavoom.txt
%{_gamesbindir}/*
%{_gamesdatadir}/*
%{_datadir}/applications/*.desktop
