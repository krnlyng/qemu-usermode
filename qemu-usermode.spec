# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.23
# 
# >> macros
# << macros

Name:       qemu-usermode
Summary:    Universal CPU emulator
Version:    1.0.50.2012.03
Release:    1
Group:      System/Emulators/PC
License:    GPLv2
ExclusiveArch:  %{ix86}
URL:        http://qemu.org
Source0:    qemu-linaro-1.0.50-2012.03.tar.gz
Source1:    qemu-binfmt-conf.sh
Source100:  qemu-usermode.yaml
Patch0:     fix-glibc-install-locales.patch
Patch1:     mips-support.patch
BuildRequires:  pkgconfig(ext2fs)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  bison
BuildRequires:  curl-devel
BuildRequires:  zlib-static
BuildRequires:  glibc-static
BuildRequires:  python-devel
BuildRequires:  glib2-static
BuildRoot:  %{_tmppath}/%{name}-%{version}-build


%description
QEMU is an extremely well-performing CPU emulator that allows you to choose between simulating an entire system and running userspace binaries for different architectures under your native operating system. It currently emulates x86, ARM, PowerPC and SPARC CPUs as well as PC and PowerMac systems.



%prep
%setup -q -n qemu-linaro-1.0.50-2012.03

# fix-glibc-install-locales.patch
%patch0 -p1
# mips-support.patch
%patch1 -p1
# >> setup
# << setup

%build
# >> build pre

%if "%{name}" == "qemu-usermode-static"
%define staticflag --static
%else
%define staticflag %{nil}
%endif

CFLAGS=`echo $CFLAGS | sed 's|-fno-omit-frame-pointer||g'` ; export CFLAGS ;
CFLAGS=`echo $CFLAGS | sed 's|-O2|-O|g'` ; export CFLAGS ;


./configure \
--prefix=/usr \
--sysconfdir=%_sysconfdir \
%{staticflag} \
--interp-prefix=/usr/share/qemu/qemu-i386 \
--disable-system \
--enable-linux-user \
--enable-guest-base \
--disable-werror \
--target-list=arm-linux-user,mipsel-linux-user

# << build pre


make %{?jobs:-j%jobs}

# >> build post
# << build post
%install
rm -rf $RPM_BUILD_ROOT
# >> install pre
%if "%{name}" == "qemu-usermode-static"
mkdir -p %{buildroot}/usr/sbin
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/usr/sbin
%endif
# << install pre
%if 0%{?moblin_version}
%make_install
%else
%makeinstall
%endif

# >> install post
rm -f $RPM_BUILD_ROOT/usr/share/qemu/openbios-ppc
rm -f $RPM_BUILD_ROOT/usr/share/qemu/openbios-sparc32
rm -f $RPM_BUILD_ROOT/usr/share/qemu/openbios-sparc64
rm -f $RPM_BUILD_ROOT/usr/libexec/qemu-bridge-helper
rm -rf $RPM_BUILD_ROOT/etc
rm -rf $RPM_BUILD_ROOT/%{_datadir}

%if "%{name}" == "qemu-usermode-static"
mv %{buildroot}%{_bindir}/qemu-arm %{buildroot}%{_bindir}/qemu-arm-static
mv %{buildroot}%{_bindir}/qemu-mipsel %{buildroot}%{_bindir}/qemu-mipsel-static
%endif

%if "%{name}" == "qemu-usermode"
mv %{buildroot}%{_bindir}/qemu-arm %{buildroot}%{_bindir}/qemu-arm-dynamic
mv %{buildroot}%{_bindir}/qemu-mipsel %{buildroot}%{_bindir}/qemu-mipsel-dynamic
%endif



# << install post






%files
%defattr(-,root,root,-)
%{_bindir}/qem*
# >> files
%if "%{name}" == "qemu-usermode-static"
%{_sbindir}/qemu-binfmt-conf.sh
%endif
# << files


