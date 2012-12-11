Name:		vavoom
Version:	1.33
Release:	%mkrel 1
Summary:	Open source port of the DOOM game engine
Source0:	http://dl.sourceforge.net/vavoom/%{name}-%{version}.tar.bz2
Patch0:		vavoom-1.30-linkage.patch
Patch1:		vavoom-1.30-fix-str-fmt.patch
Patch2:		vavoom-1.33-sfmt.patch
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
%patch2 -p1
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


%changelog
* Thu Jan 12 2012 Andrey Bondrov <abondrov@mandriva.org> 1.33-1mdv2012.0
+ Revision: 760443
- Rebuild against utf8 wxGTK2.8, build with FLAC support

  + Zombie Ryushu <ryushu@mandriva.org>
    - Upgrade to 1.33

* Wed Jul 14 2010 Zombie Ryushu <ryushu@mandriva.org> 1.32-1.2mdv2011.0
+ Revision: 553334
- fix datadir location

* Wed Jul 14 2010 Zombie Ryushu <ryushu@mandriva.org> 1.32-1.1mdv2011.0
+ Revision: 553332
- fix bindir location
- fix bindir location

* Tue Jul 13 2010 Zombie Ryushu <ryushu@mandriva.org> 1.32-1mdv2011.0
+ Revision: 551960
- Upgrade to 1.32 Fix cmake
- Upgrade to 1.32 Fix cmake
- Upgrade to 1.32
- Upgrade to 1.32

* Sat Jan 16 2010 Funda Wang <fwang@mandriva.org> 1.30-1mdv2010.1
+ Revision: 492186
- add patch to have it built correctly

* Mon Feb 23 2009 Zombie Ryushu <ryushu@mandriva.org> 1.30-1mdv2009.1
+ Revision: 344256
- New version 1.30

* Tue Nov 11 2008 Zombie Ryushu <ryushu@mandriva.org> 1.29-1mdv2009.1
+ Revision: 302018
- Update to version 1.29, Linkage patches are deprecated.
- Initial Import from Fedora

* Wed Oct 29 2008 Stéphane Téletchéa <steletch@mandriva.org> 1.28-2mdv2009.1
+ Revision: 298117
- add missing buildrequires
- Update to 1.28
- Adapt to the cmake system, and adjut the parameters accordingly

* Thu Aug 14 2008 Götz Waschk <waschk@mandriva.org> 1.22.1-5mdv2009.0
+ Revision: 271881
- patch for new mikmod
- update license

* Sun Aug 03 2008 Thierry Vignaud <tv@mandriva.org> 1.22.1-4mdv2009.0
+ Revision: 261832
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 1.22.1-3mdv2009.0
+ Revision: 255287
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 1.22.1-1mdv2008.1
+ Revision: 128866
- kill re-definition of %%buildroot on Pixel's request
- kill explicit icon extension
- kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'


* Mon Jan 22 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.22.1-1mdv2007.0
+ Revision: 111803
- fix buildrequires
- new release: 1.22.1
  some patches from Zombie
  fix xdg menu
- Import vavoom

* Thu Aug 03 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.21.1-1mdv2007.0
- initial mandriva release based on fedora package

