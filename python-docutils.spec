%define name	python-docutils
%define version 0.4

Name: 	 	%{name}
Summary: 	Python Documentation Utilities
Version: 	%{version}
Release: 	%mkrel 2

Source:		docutils-%{version}.tar.bz2
URL:		http://docutils.sourceforge.net/
License:	BSD
Group:		Development/Python
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	python-devel
BuildArch:     noarch
%description
The purpose of the Docutils project is to create a set of tools for processing
plaintext documentation into useful formats, such as HTML, XML, and TeX.
Several sources will be supported:
    * Standalone files (implemented).
    * Inline documentation from Python modules and packages, extracted with
      namespace context.
    * PEPs (Python Enhancement Proposals) (implemented).
    * And others as discovered.

%prep
%setup -q -n docutils-%version

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc *.txt docs tools
%py_puresitedir/docutils
%py_puresitedir/roman*
%py_puresitedir/*.egg-info
%_bindir/*


