%define module	docutils
%bcond_with emacs

Summary:	Python Documentation Utilities
Name:		python-%{module}
Version:	0.18.1
Release:	1
License:	BSD
Group:		Development/Python
Url:		http://docutils.sourceforge.net/
Source0:	https://files.pythonhosted.org/packages/57/b1/b880503681ea1b64df05106fc7e3c4e3801736cf63deffc6fa7fc5404cf5/docutils-0.18.1.tar.gz
BuildArch:	noarch
%if %{with emacs}
BuildRequires:	emacs
%endif
BuildRequires:	pkgconfig(python3)
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

%prep
%autosetup -p1 -n %{module}-%{version}

%install
python setup.py install --root=%{buildroot}
for file in %{buildroot}%{_bindir}/*.py; do
	mv $file %{buildroot}%{_bindir}/`basename $file .py`
done

%if %{with emacs}
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
%endif

%files
%doc *.txt docs tools
%{py_puresitedir}/docutils
%{py_puresitedir}/*.egg-info
%{_bindir}/*
%if %{with emacs}
%{_datadir}/emacs/site-lisp/*
%{_sysconfdir}/emacs/site-start.d/*
%endif
