%define module	docutils
%bcond_without python2

Summary:	Python Documentation Utilities
Name:		python-%{module}
Version:	0.15.1
Release:	1
License:	BSD
Group:		Development/Python
Url:		http://docutils.sourceforge.net/
Source0:	https://files.pythonhosted.org/packages/d4/12/6c3fd74a590c7327c98cae008c11d536029fa9cd7924de477e8cb8804186/docutils-0.15.1-post1.tar.gz
BuildArch:	noarch
BuildRequires:	emacs
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(python2)
BuildRequires:	python-setuptools
Requires:	python
Suggests:	python-imaging

%description
The purpose of the Docutils project is to create a set of tools for
processing plaintext documentation into useful formats, such as HTML,
XML, and LaTeX.  Support for the following sources has been implemented:

* Standalone files.
* PEPs (Python Enhancement Proposals)

Support for the following sources is planned:

* Inline documentation from Python modules and packages, extracted
  with namespace context.
* Email (RFC-822 headers, quoted excerpts, signatures, MIME parts).
* Wikis, with global reference lookups of "wiki links".
* Compound documents, such as multiple chapter files merged into a
  book.
* And others as discovered.

%package -n python2-docutils
Summary: Documentation utilities for Python 2.x
Requires: python2
BuildRequires: pkgconfig(python2)
Group:		Development/Python

%description -n python2-docutils
Documentation utilities for Python 2.x

%prep
%setup -qn %{module}-%{version}

mkdir python2
cp -a `ls |grep -v python2` python2

%install
cd python2
python2 setup.py install --root=%{buildroot}
# We only want the module -- the binaries come from python3
rm -f %{buildroot}%{_bindir}/*.py

cd ..
%__python setup.py install --root=%{buildroot}
for file in %{buildroot}%{_bindir}/*.py; do
  mv $file %{buildroot}%{_bindir}/`basename $file .py`
done

# Make emacs mode available:
emacs -batch -f batch-byte-compile tools/editors/emacs/rst.el
install -d -m 755 %{buildroot}%{_datadir}/emacs/site-lisp
install -D -m 644 tools/editors/emacs/rst.el* %{buildroot}%{_datadir}/emacs/site-lisp
rm -rf tools/editors/emacs

cat > ./rst.el << EOF
(autoload 'rst-mode "rst" "reStructuredText mode" t)
(add-to-list 'auto-mode-alist '("\\.rst$" . rst-mode))
EOF
emacs -batch -f batch-byte-compile rst.el
install -d -m 755 %{buildroot}%{_sysconfdir}/emacs/site-start.d
install -m 644 rst.el* %{buildroot}%{_sysconfdir}/emacs/site-start.d/

%files
%doc *.txt docs tools
%{py_puresitedir}/docutils
%{py_puresitedir}/*.egg-info
%{_bindir}/*
%{_datadir}/emacs/site-lisp/*
%{_sysconfdir}/emacs/site-start.d/*

%files -n python2-docutils
%{py2_puresitedir}/docutils
%{py2_puresitedir}/*.egg-info
