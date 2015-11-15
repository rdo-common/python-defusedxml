%global with_python3 1
%global pypi_name defusedxml

Name:           python-%{pypi_name}
Version:        0.4.1
Release:        6%{?dist}
Summary:        XML bomb protection for Python stdlib modules
License:        Python
URL:            https://bitbucket.org/tiran/defusedxml
Source0:        http://pypi.python.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

# https://bugzilla.redhat.com/show_bug.cgi?id=927883#c14
Patch0:         %{name}-entity_loop.patch
Patch1:         %{name}-format_strings.patch

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%if 0%{with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
The defusedxml package contains several Python-only workarounds and fixes for
denial of service and other vulnerabilities in Python's XML libraries. In order
to benefit from the protection you just have to import and use the listed
functions / classes from the right defusedxml module instead of the original
module.

%package -n python2-%{pypi_name}
Summary:        XML bomb protection for Python stdlib modules
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
The defusedxml package contains several Python-only workarounds and fixes for
denial of service and other vulnerabilities in Python's XML libraries. In order
to benefit from the protection you just have to import and use the listed
functions / classes from the right defusedxml module instead of the original
module.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        XML bomb protection for Python stdlib modules
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
The defusedxml package contains several Python-only workarounds and fixes for
denial of service and other vulnerabilities in Python's XML libraries. In order
to benefit from the protection you just have to import and use the listed
functions / classes from the right defusedxml module instead of the original
module.
%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}
%if 0%{?rhel}
%patch0 -p1
%endif
%patch1 -p1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/bin/env python|#!%{__python3}|'
%endif # with_python3

%build
%{__python} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%{__python} setup.py install --skip-build --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%check
%{__python} tests.py
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} tests.py
popd
%endif # with_python3

%files -n python2-%{pypi_name}
%doc README.txt README.html CHANGES.txt
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.txt README.html CHANGES.txt
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python3

%changelog
* Sun Nov 15 2015 Ralph Bean <rbean@redhat.com> - 0.4.1-6
- Added explicit python2 subpackage with modern provides statement.
- Only apply the entity_loop patch on enterprisey builds.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Aug 05 2015 Miro Hrončok <mhroncok@redhat.com> - 0.4.1-4
- Add patches by Avram Lubkin
- https://bugzilla.redhat.com/show_bug.cgi?id=927883#c14

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Miro Hrončok <mhroncok@redhat.com> - 0.4.1-1
- Updated to 0.4.1 (#1100730)

* Tue May 13 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Miro Hrončok <mhroncok@redhat.com> - 0.4-1
- Initial package.
