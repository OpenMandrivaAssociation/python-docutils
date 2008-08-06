%define name	python-docutils
%define version 0.5

Name: 	 	%{name}
Summary: 	Python Documentation Utilities
Version: 	%{version}
Release: 	%mkrel 1

Source:		docutils-%{version}.tar.lzma
URL:		http://docutils.sourceforge.net/
License:	BSD
Group:		Development/Python
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	python-devel, emacs
BuildArch:	noarch
Requires:	python      

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
%setup -q -n docutils-%version

%install
%__rm -rf %{buildroot}
%__python setup.py install --root=%{buildroot}
for file in %{buildroot}%_bindir/*.py; do
  mv $file %{buildroot}%_bindir/`basename $file .py`
done

# force installation of roman.py:
%__install -D -m 0644 extras/roman.py %{buildroot}/%py_puresitedir/roman.py

# make emacs mode available:
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

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc *.txt docs tools
%py_puresitedir/docutils
%py_puresitedir/roman*
%py_puresitedir/*.egg-info
%_bindir/*
%_datadir/emacs/site-lisp/*
%_sysconfdir/emacs/site-start.d/*
