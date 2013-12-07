%define module	docutils

Summary:	Python Documentation Utilities
Name:		python-%{module}
Version:	0.11
Release:	2
License:	BSD
Group:		Development/Python
Url:		http://docutils.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/docutils/docutils/0.11/docutils-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	emacs
BuildRequires:	pkgconfig(python)
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
%setup -qn %{module}-%{version}

%install
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

