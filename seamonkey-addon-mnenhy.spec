
%define		_realname	mnenhy

Summary:	MailNews-Enhancements
Summary(pl.UTF-8):	Rozszerzenia MailNews
Name:		seamonkey-addon-%{_realname}
Version:	0.7.6
Release:	0.1
License:	MPL 1.1/GPL 2.0/LGPL 2.1
Group:		X11/Applications/Networking
Source0:	http://downloads.mozdev.org/mnenhy/%{_realname}-%{version}.xpi
# Source0-md5:	6fdda0ca6a830bb9167b7474924c8341
Source1:	gen-installed-chrome.sh
URL:		http://mnenhy.mozdev.org/
BuildRequires:	unzip
BuildRequires:	zip
Requires(post,postun):	seamonkey >= 1.0
Requires:	seamonkey >= 1.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_chromedir	%{_datadir}/seamonkey/chrome

%description
The primary goal of the Mnenhy project is to make some enhancements to
SeaMonkey/Mozilla MailNews.

%description -l pl.UTF-8
Głównym celem projektu Mnenhy jest tworzenie rozszerzeń do klienta
SeaMonkey/Mozilla MailNews.

%prep
%setup -qc
install %{SOURCE1} .

unzip -qq chrome/%{_realname}.jar
find content -mindepth 1 -type d \
	| sed 's#^#content,install,url,jar:resource:/chrome/%{_realname}.jar!/#; s#$#/#' \
	> %{_realname}-installed-chrome.txt

# en should be the first language
./gen-installed-chrome.sh locale chrome/%{_realname}.{en,[!e]*}-*.jar \
	>> %{_realname}-installed-chrome.txt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_chromedir}

install chrome/%{_realname}*.jar $RPM_BUILD_ROOT%{_chromedir}
install %{_realname}-installed-chrome.txt $RPM_BUILD_ROOT%{_chromedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/seamonkey-chrome+xpcom-generate

%postun
%{_sbindir}/seamonkey-chrome+xpcom-generate

%files
%defattr(644,root,root,755)
%{_chromedir}/%{_realname}.jar
%{_chromedir}/%{_realname}.*-*.jar
%{_chromedir}/%{_realname}-installed-chrome.txt
