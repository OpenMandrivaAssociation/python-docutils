%define module	docutils
%define name	python-%{module}
%define version	0.9.1
%define	rel		1
%if %mdkversion < 201100
%define	release %mkrel %{rel}
%else
%define	release	%{rel}
%endif

Name:		%{name}
Summary:	Python Documentation Utilities
Version:	%{version}
Release:	%{release}
Source:		http://downloads.sourceforge.net/project/docutils/docutils/%{version}/%{module}-%{version}.tar.gz
URL:		http://docutils.sourceforge.net/
License:	BSD
Group:		Development/Python
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildArch:	noarch
BuildRequires:	python-devel, emacs, python-nose
Requires:	python
Suggests:	python-imaging, python-pygments

%description
Docutils is a modular system for processing documentation into useful formats,
such as HTML, XML, and LaTeX. For input Docutils supports reStructuredText, an
easy-to-read, what-you-see-is-what-you-get plaintext markup syntax.

%prep
%setup -q -n %{module}-%{version}

%install
%__rm -rf %{buildroot}

# Rename executable scripts installed in /usr/bin:
%__python setup.py install --root=%{buildroot}
for file in %{buildroot}%_bindir/*.py; do
  mv $file %{buildroot}%_bindir/`basename $file .py`
done

# Make emacs mode available:
emacs -batch -f batch-byte-compile tools/editors/emacs/rst.el
%__install -d -m 755 %{buildroot}%{_datadir}/emacs/site-lisp
%__install -D -m 644 tools/editors/emacs/rst.el* %{buildroot}%{_datadir}/emacs/site-lisp
%__rm -rf tools/editors/emacs

cat > ./rst.el << EOF
(autoload 'rst-mode "rst" "reStructuredText mode" t)
(add-to-list 'auto-mode-alist '("\\.rst$" . rst-mode))
EOF
emacs -batch -f batch-byte-compile rst.el
%__install -d -m 755 %{buildroot}%{_sysconfdir}/emacs/site-start.d
%__install -m 644 rst.el* %{buildroot}%{_sysconfdir}/emacs/site-start.d/

%check
nosetests -q

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc *.txt docs/ licenses/
%_bindir
%py_puresitedir/docutils*
%_datadir/emacs/site-lisp/*
%_sysconfdir/emacs/site-start.d/*
