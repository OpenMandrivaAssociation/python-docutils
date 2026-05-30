%define module docutils
%bcond emacs 0

Name:		python-docutils
Summary:	Python Documentation Utilities
Version:	0.23
Release:	1
License:	CC-PDDC AND 0BSD AND BSD-3-Clause AND BSD-2-Clause AND GPL-2.0-or-later AND GPL-3.0-or-later
Group:		Development/Python
URL:		https://docutils.sourceforge.net
Source0:	https://files.pythonhosted.org/packages/source/d/%{module}/%{module}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc

BuildSystem:	python
BuildArch:	noarch
%if %{with emacs}
BuildRequires:	emacs
%endif
BuildRequires:	fdupes
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(flit-core)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(wheel)
Suggests:	python%{pyver}dist(imaging)
Suggests:	python%{pyver}dist(pygments)

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

%prep -a
# Remove shebang from library files
sed -i -e '/#! *\/usr\/bin\/.*/{1D}' $(grep -Erl '^#!.+python' docutils)
# Remove executable bits
find . -type f -exec chmod -x {} +

%install -a
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

# Build docs
# For instructions see: https://docutils.sourceforge.io/docs/dev/distributing.html#documentation
export PYTHONPATH="%{buildroot}%{python_sitelib}"
pushd tools
# Copy css to basedir
cp ../docutils/writers/html4css1/html4css1.css ..
# Run builthtml.py with options applied including --no-source-link, which saves
# having to run the build script again after removing the rst files below.
%{__python} buildhtml.py --input-encoding=utf-8 --no-datestamp \
		--stylesheet-path=../html4css1.css .. --no-source-link
popd

# Find and remove all .rst files except cheatsheet.rst, demo.rst and licences/
# path contents.
# We dont need to keep the rest of the .rst souce files in the package after
# the html files have been generated.
# See: https://docutils.sourceforge.io/docs/dev/distributing.html#removing-the-rst-files
find . ! -name 'cheatsheet.rst' ! -name 'demo.rst' ! -path "*/licenses/*" \
	-name '*.rst' -type f -exec rm -f {} +

# We want the licenses but dont need this build file
rm -f licenses/docutils.conf

%fdupes %{buildroot}%{python_sitelib}


%files
%doc *.html docs/ licenses/ html4css1.css tools/editors
%{_bindir}/%{module}
%{_bindir}/rst2{html,html4,html5,latex,man,odt,pseudoxml,s5,xetex,xml}
%{python_sitelib}/%{module}
%{python_sitelib}/%{module}-%{version}.dist-info
%if %{with emacs}
%{_datadir}/emacs/site-lisp/*
%{_sysconfdir}/emacs/site-start.d/*
%endif
