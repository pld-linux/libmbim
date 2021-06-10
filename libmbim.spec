# TODO: --enable-mbim-username=???
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	GLib library for talking to WWAN modems and devices using MBIM protocol
Summary(pl.UTF-8):	Biblioteka GLib do komunikacji z modemami i urządzeniami WWAN z użyciem protokołu MBIM
Name:		libmbim
Version:	1.24.8
Release:	1
License:	LGPL v2
Group:		Libraries
Source0:	https://www.freedesktop.org/software/libmbim/%{name}-%{version}.tar.xz
# Source0-md5:	89f6b740ac60f8b008f6446006bbbb7e
URL:		https://www.freedesktop.org/wiki/Software/libmbim
BuildRequires:	autoconf >= 2.68
BuildRequires:	autoconf-archive >= 2017.03.21
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.48
BuildRequires:	gobject-introspection-devel >= 0.9.6
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	help2man
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	udev-glib-devel >= 1:147
Requires:	glib2 >= 1:2.48
Requires:	udev-glib >= 1:147
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libmbim is a GLib library for talking to WWAN modems and devices which
speak the Mobile Interface Broadband Model (MBIM) protocol.

%description -l pl.UTF-8
libmbim to biblioteka GLib do komunikacji z modemami i urządzeniami
WWAN, obsługującymi protokół MBIM (Mobile Interface Broadband Model).

%package devel
Summary:	Header files for libmbim library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmbim
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.48

%description devel
Header files for libmbim library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libmbim.

%package static
Summary:	Static libmbim library
Summary(pl.UTF-8):	Statyczna biblioteka libmbim
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libmbim library.

%description static -l pl.UTF-8
Statyczna biblioteka libmbim.

%package apidocs
Summary:	libmbim API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libmbim
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
API documentation for libmbim library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libmbim.

%package -n bash-completion-libmbim
Summary:	Bash completion for libmbim commands
Summary(pl.UTF-8):	Bashowe dopełnianie składni poleceń libmbim
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0

%description -n bash-completion-libmbim
Bash completion for libmbim commands (mbimcli).

%description -n bash-completion-libmbim -l pl.UTF-8
Bashowe dopełnianie składni poleceń libmbim (mbimcli).

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable apidocs gtk-doc} \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/mbim-network
%attr(755,root,root) %{_bindir}/mbimcli
%attr(755,root,root) %{_libexecdir}/mbim-proxy
%attr(755,root,root) %{_libdir}/libmbim-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmbim-glib.so.4
%{_libdir}/girepository-1.0/Mbim-1.0.typelib
%{_mandir}/man1/mbim-network.1*
%{_mandir}/man1/mbimcli.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmbim-glib.so
%{_includedir}/libmbim-glib
%{_datadir}/gir-1.0/Mbim-1.0.gir
%{_pkgconfigdir}/mbim-glib.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmbim-glib.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libmbim-glib
%endif

%files -n bash-completion-libmbim
%defattr(644,root,root,755)
%{bash_compdir}/mbimcli
