Name:           apksideloader
Version:        0.1
Release:        1%{?dist}
Summary:        Tool to sideload Android packages onto Chromebooks

%if "%{_vendor}" == "debbuild"
# Maps to debian/control required Maintainer field
Packager:       Stephen Gallagher <Stephen@gallagherhome.com>
License:        GPL-3.0+
%else
License:        GPLv3+
%endif
URL:            https://github.com/sgallagher/apksideloader
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%if "%{_vendor}" == "debbuild"
BuildRequires:  python3-dev >= 3.7
BuildRequires:  python3-setuptools
BuildRequires:  python3-deb-macros
Requires:       python3-adb-shell
Requires:       python3-click >= 7.0.0
Requires:       python3-gi >= 3.30.4
Requires:       python3-setuptools
Requires(post): python3-minimal >= 3.7
Requires(preun): python3-minimal >= 3.7
%else
BuildRequires:  python3-devel >= 3.7
BuildRequires:  python3-setuptools

# Enable Python dependency generation
%{?python_enable_dependency_generator}

%if %{undefined python_enable_dependency_generator}
Requires:       python3dist(adb-shell)
Requires:       python3dist(click) >= 7
Requires:       python3dist(pygobject) >= 3.30.4
Requires:       python3dist(setuptools)
%endif
%endif

%description
%{name} is a tool to sideload Android packages (APKs) onto
devices running Google Chrome OS.

%prep
%autosetup -p1


%build
%py3_build


%install
%py3_install

mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/192x192

# Install desktop file
sed -e "s|@PREFIX@/@BINDIR@|%{_bindir}|g" \
    data/com.gallagherhome.apksideloader.desktop.in \
    > %{buildroot}%{_datadir}/applications/com.gallagherhome.apksideloader.desktop

# Install icon
install -pm 0644 ./data/icons/hicolor/192x192/android_icon.png \
    %{buildroot}%{_datadir}/icons/hicolor/192x192/android_icon.png


%files
%if "%{_vendor}" == "debbuild"
%license packaging/copyright
%endif
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{python3_sitelib}/%{name}*
%{_datadir}/applications/com.gallagherhome.apksideloader.desktop
%{_datadir}/icons/hicolor/192x192/android_icon.png


%if "%{_vendor}" == "debbuild"
# Debian does install-time byte-compilation
%post
%{py3_bytecompile_post %{name}}

%preun
%{py3_bytecompile_preun %{name}}
%endif


%changelog
* Thu Jun  4 2020 Neal Gompa <ngompa13@gmail.com>
- Initial packaging
