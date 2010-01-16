%define	name	vavoom
%define	version	1.30
%define	release %mkrel 1
%define	Summary	Open source port of the DOOM game engine

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://dl.sourceforge.net/vavoom/%{name}-%{version}.tar.bz2
Patch0:		vavoom-1.30-linkage.patch
Patch1:		vavoom-1.30-fix-str-fmt.patch
Patch2:		vavoom-1.30-cmake28-fix.patch
URL:		http://vavoom-engine.com/
Group:		Games/Arcade
License:	GPLv2+
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	SDL-devel SDL_mixer-devel SDL_net-devel libpng-devel allegro-devel
BuildRequires:	oggvorbis-devel libmad-devel openal-devel libmikmod-devel
BuildRequires:	cmake desktop-file-utils mesagl-devel libjpeg-devel wxGTK-devel
Enhances:	vavoom-vmdl TiMidity++

%description
Vavoom is an open-source port of Doom, the classic 3D first-person shooter
game.  It adds some extra features to Doom such as translucency
and freelook support.

%prep 
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1
# This one line sed command is easier than trying to muck with the Makefile
# to add the proper -D definition.
%{__sed} -i "s|#define FL_BASEDIR.*|#define FL_BASEDIR \"%{_gamesdatadir}/%{name}\"|" source/files.h

%build
%cmake -DCMAKE_INSTALL_PREFIX=%{_gamesbindir} \
      -DDATADIR=%{_gamesdatadir} \
      -DWITH_SDL=Y \
      -DWITH_OPENGL=Y \
      -DWITH_OPENAL=Y \
      -DWITH_ALLEGRO=N

# The Makefile doesn't do parallel builds correctly.
make

%install
rm -rf %{buildroot}
%makeinstall_std -C build

cat << EOF > %{name}.desktop
[Desktop Entry]
Name=Freedoom
Comment=Freedoom with the Vavoom engine
Exec=vavoom
Icon=arcade_section
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

desktop-file-install --vendor="" \
        --dir %{buildroot}%{_datadir}/applications \
        --add-category="X-MandrivaLinux-MoreApplications-Games-Arcade;" \
        %{name}.desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_gamesbindir}/*
%{_gamesdatadir}/*
%{_datadir}/applications/*.desktop
%doc docs/*.log docs/gnu.txt docs/vavoom.txt
