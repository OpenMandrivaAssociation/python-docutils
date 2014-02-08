%define module	docutils
%define name	python-%{module}
%define version	0.10

Name:		%{name}
Summary:	Python Documentation Utilities
Version:	%{version}
Release:	2
Source:		http://downloads.sourceforge.net/project/docutils/docutils/%{version}/%{module}-%{version}.tar.gz
URL:		http://docutils.sourceforge.net/
License:	BSD
Group:		Development/Python
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildArch:	noarch
BuildRequires:	python-devel, emacs
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
%setup -q -n %{module}-%{version}

%install
%__python setup.py install --root=%{buildroot}
for file in %{buildroot}%{_bindir}/*.py; do
  mv $file %{buildroot}%{_bindir}/`basename $file .py`
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

%clean
%__rm -rf %{buildroot}

%files
%doc *.txt docs tools
%py_puresitedir/docutils
%py_puresitedir/*.egg-info
%_bindir/*
%_datadir/emacs/site-lisp/*
%_sysconfdir/emacs/site-start.d/*


%changelog
* Fri Feb  8 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.10-1
- Update to 0.10.

* Fri Jul 08 2011 Lev Givon <lev@mandriva.org> 0.8-1
+ Revision: 689352
- Update to 0.8.

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.7-4
+ Revision: 667930
- mass rebuild

* Tue Jan 25 2011 Lev Givon <lev@mandriva.org> 0.7-3
+ Revision: 632711
- Rebuild to provide pythonegg(docutils).

* Fri Oct 29 2010 Michael Scherer <misc@mandriva.org> 0.7-2mdv2011.0
+ Revision: 590062
- rebuild for python 2.7

* Sat Aug 07 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.7-1mdv2011.0
+ Revision: 567230
- update to 0.7

* Mon Jan 04 2010 Lev Givon <lev@mandriva.org> 0.6-1mdv2010.1
+ Revision: 486092
- Update to 0.6.

* Fri Dec 26 2008 Funda Wang <fwang@mandriva.org> 0.5-2mdv2009.1
+ Revision: 319373
- rebuild for new python

* Thu Aug 07 2008 Lev Givon <lev@mandriva.org> 0.5-1mdv2009.0
+ Revision: 265323
- Update to 0.5.
  Make emacs mode automatically available.

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 0.4-6mdv2009.0
+ Revision: 242390
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun May 27 2007 Bogdano Arendartchuk <bogdano@mandriva.com> 0.4-4mdv2008.0
+ Revision: 31678
- added requires to python, as it uses pprint

* Fri May 25 2007 Bogdano Arendartchuk <bogdano@mandriva.com> 0.4-3mdv2008.0
+ Revision: 31138
- removed .py suffix of files installed in %%_bindir, as it's done
  by other distros
- force the installation of roman.py


* Wed Dec 13 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.4-2mdv2007.0
+ Revision: 96084
- Fix File section
- Rebuild for new python
- Import python-docutils

* Fri Mar 03 2006 Austin Acton <austin@mandriva.org> 0.4-1mdk
- New release 0.4

* Thu Jan 12 2006 Michael Scherer <misc@mandriva.org> 0.3.9-2mdk
- Use new python macro
- use mkrel

* Wed Nov 23 2005 Austin Acton <austin@mandriva.org> 0.3.9-1mdk
- 0.3.9

* Mon Mar 14 2005 Michael Scherer <misc@mandrake.org> 0.3.7-1mdk
- New release 0.3.7
- noarch

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 0.3-2mdk
- Rebuild for new python

