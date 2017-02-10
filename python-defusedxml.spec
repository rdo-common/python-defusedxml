# Enable Python 3 builds for Fedora + EPEL >6
%if 0%{?fedora} || 0%{?rhel} > 6
# If the definition isn't available for python3_pkgversion, define it
%{?!python3_pkgversion:%global python3_pkgversion 3}
%bcond_without  python3
%else
%bcond_with     python3
%endif

%global pypi_name defusedxml
# define the license macro as doc if licensedir is not defined for
# compatibility with EPEL
%{!?_licensedir:%global license %%doc}

Name:           python-%{pypi_name}
Version:        0.5.0
Release:        1%{?dist}
Summary:        XML bomb protection for Python stdlib modules
License:        Python
URL:            https://github.com/tiran/defusedxml
Source0:        https://files.pythonhosted.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
# No python2-setuptools on EL 7
BuildRequires:  python-setuptools

%if 0%{with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%if 0%{?with_python3_other}
BuildRequires:  python%{python3_other_pkgversion}-setuptools
BuildRequires:  python%{python3_other_pkgversion}-devel
%endif # with_python3_other
%endif # with_python3

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
module. This is the Python 2 build.

%if 0%{with_python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        XML bomb protection for Python stdlib modules
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
The defusedxml package contains several Python-only workarounds and fixes for
denial of service and other vulnerabilities in Python's XML libraries. In order
to benefit from the protection you just have to import and use the listed
functions / classes from the right defusedxml module instead of the original
module. This is the python%{python3_pkgversion} build.

%if 0%{?with_python3_other}
%package -n python%{python3_other_pkgversion}-%{pypi_name}
Summary:        XML bomb protection for Python stdlib modules
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_other_pkgversion}-%{pypi_name}
The defusedxml package contains several Python-only workarounds and fixes for
denial of service and other vulnerabilities in Python's XML libraries. In order
to benefit from the protection you just have to import and use the listed
functions / classes from the right defusedxml module instead of the original
module. This is the python%{python3_other_pkgversion} build.
%endif # with_python3_other
%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%py2_build
%if 0%{with_python3}
%py3_build
%if 0%{?with_python3_other}
%py3_other_build
%endif # with_python3_other
%endif # with_python3

%install
%py2_install
%if 0%{with_python3}
%py3_install
%if 0%{?with_python3_other}
%py3_other_install
%endif # with_python3_other
%endif # with_python3

%check
%{__python2} tests.py
%if 0%{with_python3}
%{__python3} tests.py
%endif # with_python3

%files -n python2-%{pypi_name}
%doc README.txt README.html CHANGES.txt
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{with_python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.txt README.html CHANGES.txt
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3_other}
%files -n python%{python3_other_pkgversion}-%{pypi_name}
%doc README.txt README.html CHANGES.txt
%license LICENSE
%{python3_other_sitelib}/%{pypi_name}
%{python3__other_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python3_other
%endif # with_python3

%changelog
* Fri Feb 10 2017 Adam Williamson <awilliam@redhat.com> - 0.5.0-1
- Update to 0.5.0, drop merged/superseded patches
- Enable Python 3 build for EPEL 7, per https://fedoraproject.org/wiki/PackagingDrafts:Python3EPEL
- Drop format-string patch as Python 2.6 is no longer supported anyway
- Update URL to github
- Update source URL for pypi changes

* Thu Dec 22 2016 Adam Williamson <awilliam@redhat.com> - 0.4.1-9
- Fix incompatibility with Python 3.6 (gh#3 / gh#4)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com>
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

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
