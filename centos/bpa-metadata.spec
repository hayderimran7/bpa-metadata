%define __python /usr/bin/python%{pybasever}
# sitelib for noarch packages
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define pyver 27
%define pybasever 2.7

%define name bpa-metadata
%define nickname bpam
%define version 1.0.14
%define unmangled_version 1.0.14
%define release 1
%define webapps /usr/local/webapps
%define installdir %{webapps}/%{name}
%define buildinstalldir %{buildroot}/%{installdir}
%define settingsdir %{buildinstalldir}/defaultsettings
%define logdir %{buildroot}/var/log/%{name}
%define mediadir %{buildroot}/var/lib/%{name}/media
%define staticdir %{buildinstalldir}/static

Summary: bpa-metadata
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GNU GPL v2
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: x86_64
Vendor: Centre for Comparative Genomics <web@ccg.murdoch.edu.au>
BuildRequires: python%{pyver}-virtualenv python%{pyver}-devel
Requires: httpd python%{pyver}-psycopg2 python%{pyver}-mod_wsgi

%description
BPA Metadata Management

%prep

if [ -d ${RPM_BUILD_ROOT}%{installdir} ]; then
    echo "Cleaning out stale build directory" 1>&2
    rm -rf ${RPM_BUILD_ROOT}%{installdir}
fi

%build
# Nothing, all handled by install

# Turn off brp-python-bytecompile because it compiles the settings file.
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%install
NAME=%{name}
NICKNAME=%{nickname}

# Build from source dir
cd $CCGSOURCEDIR

# Make sure the standard target directories exist
# These two contain files owned by the RPM
mkdir -p %{settingsdir}
mkdir -p %{staticdir}

# The rest are for persistent data files created by the app
mkdir -p %{logdir}
mkdir -p %{mediadir}

# Create a python prefix with app requirements
mkdir -p %{buildinstalldir}
virtualenv-%{pybasever} %{buildinstalldir}
. %{buildinstalldir}/bin/activate

# Use specific version of pip -- avoids surprises with deprecated
# options, etc.
pip install --force-reinstall --upgrade 'pip>=1.5,<1.6'

# Install package into the prefix
pip install --allow-all-external --process-dependency-links ./%{nickname}

# Fix up paths in virtualenv, enable use of global site-packages
virtualenv-%{pybasever} --relocatable %{buildinstalldir}
find %{buildinstalldir} -name \*py[co] -exec rm {} \;
find %{buildinstalldir} -name no-global-site-packages.txt -exec rm {} \;
sed -i "s|`readlink -f ${RPM_BUILD_ROOT}`||g" %{buildinstalldir}/bin/*

# Strip out mention of rpm buildroot from the pip install record
find %{buildinstalldir} -name RECORD -exec sed -i -e "s|${RPM_BUILD_ROOT}||" {} \;

cp -r ./data* %{buildinstalldir}/
cp -r ./tools* %{buildinstalldir}/

# don't need a copy of python interpreter in the virtualenv
rm %{buildinstalldir}/bin/python*

# Create settings symlink so we can run collectstatic with the default settings
touch %{settingsdir}/__init__.py
ln -sf ..`find %{buildinstalldir} -path "*/%{nickname}/settings.py" | sed s:^%{buildinstalldir}::` %{settingsdir}/%{nickname}.py

# Create symlinks under install directory to real persistent data directories
APP_SETTINGS_FILE=`find %{buildinstalldir} -path "*/%{nickname}/settings.py" | sed s:^%{buildinstalldir}/::`
APP_PACKAGE_DIR=`dirname ${APP_SETTINGS_FILE}`
VENV_LIB_DIR=`dirname ${APP_PACKAGE_DIR}`
ln -sfT /var/log/%{name} %{buildinstalldir}/${VENV_LIB_DIR}/log
ln -sfT /var/lib/%{name}/media %{buildinstalldir}/${APP_PACKAGE_DIR}/media
ln -sfT %{installdir}/static %{buildinstalldir}/${VENV_LIB_DIR}/static

# make defaultsettings importable
ln -sfT %{installdir}/defaultsettings %{buildinstalldir}/${VENV_LIB_DIR}/defaultsettings

# Install WSGI configuration into httpd/conf.d
install -D centos/%{name}.ccg %{buildroot}/etc/httpd/conf.d/%{name}.ccg
ln -sfT ${APP_PACKAGE_DIR}/wsgi.py %{buildinstalldir}/django.wsgi

# Create manage script symlink
mkdir -p %{buildroot}/%{_bindir}
ln -sfT %{installdir}/bin/%{nickname}-manage.py %{buildroot}/%{_bindir}/%{nickname}


%post
# Clear out staticfiles data and regenerate
# fixme: not sure whether staticfiles app will be used
rm -rf %{installdir}/static/*
echo "collectstatic:" >&2
%{nickname} collectstatic --noinput # > /dev/null
# Remove root-owned logged files just created by collectstatic
rm -rf /var/log/%{name}/*
# Touch the wsgi file to get the app reloaded by mod_wsgi
touch %{installdir}/django.wsgi

%preun
if [ "$1" = "0" ]; then
  # Nuke staticfiles if not upgrading
  rm -rf %{installdir}/static/*
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,apache,apache,-)
/etc/httpd/conf.d/*
%{_bindir}/%{nickname}
%attr(-,apache,,apache) %{webapps}/%{name}
%attr(-,apache,,apache) /var/log/%{name}
%attr(-,apache,,apache) /var/lib/%{name}
