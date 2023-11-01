%global __python3 /usr/bin/python3.11
%global python3_pkgversion 3.11

%bcond_without tests

Name:           python%{python3_pkgversion}-pycparser
Summary:        C parser and AST generator written in Python
Version:        2.20
Release:        1%{?dist}
License:        BSD
URL:            http://github.com/eliben/pycparser
Source0:        %{url}/archive/release_v%{version}.tar.gz
Source1:        pycparser-0.91.1-remove-relative-sys-path.py

# This is Fedora-specific; I don't think we should request upstream to
# remove embedded libraries from their distribution, when we can remove
# them during packaging.
# It also ensures that pycparser uses the same YACC __tabversion__ as ply
# package to prevent "yacc table file version is out of date" problem.
Patch100:       pycparser-unbundle-ply.patch

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-rpm-macros
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-ply

Requires:       python%{python3_pkgversion}-ply

# for unit tests
%if %{with tests}
BuildRequires:  cpp
%endif

%description
pycparser is a complete parser for the C language, written in pure Python.
It is a module designed to be easily integrated into applications that
need to parse C source code.

%prep
%autosetup -p1 -n pycparser-release_v%{version}

# remove embedded copy of ply
rm -r pycparser/ply

# Remove relative sys.path from the examples
%{python3} %{SOURCE1} examples

%build
%py3_build
pushd build/lib/pycparser
%{__python3} _build_tables.py
popd

%install
%py3_install

%check
%if %{with tests}
%{python3} tests/all_tests.py
%endif
 
%files -n python%{python3_pkgversion}-pycparser
%license LICENSE
%doc examples
%{python3_sitelib}/pycparser/
%{python3_sitelib}/pycparser-*.egg-info/

%changelog
* Tue Nov 29 2022 Charalampos Stratakis <cstratak@redhat.com> - 2.20-1
- Initial package
- Fedora contributions by:
      Charalampos Stratakis <cstratak@redhat.com>
      Christian Heimes <cheimes@redhat.com>
      Dennis Gilmore <dennis@ausil.us>
      Eric Smith <brouhaha@fedoraproject.org>
      Igor Gnatenko <ignatenkobrain@fedoraproject.org>
      Iryna Shcherbina <shcherbina.iryna@gmail.com>
      Lumir Balhar <lbalhar@redhat.com>
      Marcel Plch <mplch@redhat.com>
      Miro Hrončok <miro@hroncok.cz>
      Nathaniel McCallum <nathaniel@themccallums.org>
      Orion Poplawski <orion@cora.nwra.com>
      Robert Kuska <rkuska@redhat.com>
      Slavek Kabrda <bkabrda@redhat.com>
      Stephen Gallagher <sgallagh@redhat.com>
      Tom Callaway <spot@fedoraproject.org>
      Troy Dawson <tdawson@redhat.com>
