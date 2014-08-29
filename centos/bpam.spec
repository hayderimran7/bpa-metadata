%define __python /usr/bin/python%{pybasever}
# sitelib for noarch packages
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define pyver 27
%define pybasever 2.7

%define app bpa-metadata
%define name %{app}
%define nickname bpam 
%define version 1.3.0
%define unmangled_version %{version}
%define release 1
%define webapps /usr/local/webapps
%define installdir %{webapps}/%{name}
%define buildinstalldir %{buildroot}/%{installdir}
%define settingsdir %{buildinstalldir}/defaultsettings
%define logdir %{buildroot}/var/log/%{nickname}
%define mediadir %{buildroot}/var/lib/%{nickname}/media
%define scratchdir %{buildroot}/var/lib/%{nickname}/scratch
%define sharedir %{buildroot}/usr/share/%{nickname}/
%define staticdir %{buildinstalldir}/static

Summary: bpa-metadata
Name: %{app}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GNU GPL v3
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{app}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: x86_64
Vendor: Centre for Comparative Genomics <web@ccg.murdoch.edu.au>
BuildRequires: python%{pyver}-virtualenv python%{pyver}-devel libffi-devel graphviz-devel proj-devel gdal-devel libxml2-devel libxslt-devel git
Requires: python%{pyver}-psycopg2 python%{pyver}-mod_wsgi httpd libffi-devel graphviz-devel gdal proj-devel postgis2_93 python%{pyver}-lxml python%{pyver}-mod_wsgi httpd

%description
BPA Metadata Management

%prep

if [ -d ${RPM_BUILD_ROOT}%{installdir} ]; then
    echo "Cleaning out stale build directory" 1>&2
    rm -rf ${RPM_BUILD_ROOT}%{installdir}
fi

# Turn off brp-python-bytecompile because it compiles the settings file.
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%install
NAME=%{name}

# Build from source dir
cd $CCGSOURCEDIR

# Make sure the standard target directories exist
# These two contain files owned by the RPM
mkdir -p %{settingsdir}
mkdir -p %{staticdir}
# The rest are for persistent data files created by the app
mkdir -p %{logdir}
mkdir -p %{mediadir}
mkdir -p %{scratchdir}
mkdir -p %{sharedir}

# Create a python prefix with app requirements
mkdir -p %{buildinstalldir}

# Make a virtualenv and install the app's dependencies
virtualenv-%{pybasever} %{buildinstalldir}
. %{buildinstalldir}/bin/activate

# Use specific version of pip -- avoids surprises with deprecated
# options, etc.
pip install --force-reinstall --upgrade 'pip>=1.5,<1.6'

# Install package into the prefix
pip install --allow-unverified --allow-all-external --process-dependency-links .


# Fix up paths in virtualenv, enable use of global site-packages
virtualenv-%{pybasever} --relocatable %{buildinstalldir}
find %{buildinstalldir} -name \*py[co] -exec rm {} \;
find %{buildinstalldir} -name no-global-site-packages.txt -exec rm {} \;
sed -i "s|$(readlink -f ${RPM_BUILD_ROOT})||g" %{buildinstalldir}/bin/*

# Strip out mention of rpm buildroot from the pip install record
find %{buildinstalldir} -name RECORD -exec sed -i -e "s|${RPM_BUILD_ROOT}||" {} \;

# Strip debug syms out of the compiled python modules which are in the
# build root.
find %{buildinstalldir} -name \*.so -exec strip -g {} \;

# don't need a copy of python interpreter in the virtualenv
# rm %{buildinstalldir}/bin/python*

# tools are ne`eded to popalte the database from the excell spreadsheets
cp -r ./tools* %{buildinstalldir}/

# Create settings symlink so we can run collectstatic with the default settings
# touch %{settingsdir}/__init__.py
# ln -sf .. $(find %{buildinstalldir} -path "*/%{name}/settings.py" | sed s:^%{buildinstalldir}::) %{settingsdir}/%{name}.py

# Create symlinks under install directory to real persistent data directories
APP_SETTINGS_FILE=`find %{buildinstalldir} -path "*/%{nickname}/settings.py" | sed s:^%{buildinstalldir}/::`
APP_PACKAGE_DIR=`dirname ${APP_SETTINGS_FILE}`
VENV_LIB_DIR=`dirname ${APP_PACKAGE_DIR}`

# Create static files symlink within module directory
ln -fsT %{installdir}/static %{buildinstalldir}/${VENV_LIB_DIR}/static
ln -fsT %{installdir}/static %{buildinstalldir}/${VENV_LIB_DIR}/static

# Install prodsettings conf file to /etc, and replace with symlink
install --mode=0640 -D centos/%{nickname}.conf.example %{buildroot}/etc/%{nickname}/%{nickname}.conf
install --mode=0640 -D %{nickname}/prodsettings.py %{buildroot}/etc/%{nickname}/settings.py
ln -sfT /etc/${nickname}/settings.py %{buildinstalldir}/${APP_PACKAGE_DIR}/prodsettings.py

# Create symlinks under install directory to real persistent data directories
ln -fsT /var/log/%{nickname} %{buildinstalldir}/${VENV_LIB_DIR}/log
ln -fsT /var/lib/%{nickname}/scratch %{buildinstalldir}/${VENV_LIB_DIR}/scratch
ln -fsT /var/lib/%{nickname}/media %{buildinstalldir}/${VENV_LIB_DIR}/media

# temp fix to make defaultsettings importable
ln -sfT %{installdir}/defaultsettings %{buildinstalldir}/${APP_PACKAGE_DIR}/../defaultsettings

# Install WSGI configuration into httpd/conf.d
install -D centos/%{nickname}.ccg %{buildroot}/etc/httpd/conf.d/%{nickname}.ccg
ln -sfT ${APP_PACKAGE_DIR}/wsgi.py %{buildinstalldir}/django.wsgi

# Create symlinks to scripts in the virtualenv
mkdir -p %{buildroot}/%{_bindir}
ln -sfT %{installdir}/bin/%{nickname}-manage.py %{buildroot}/%{_bindir}/%{nickname}

%post
# Clear out staticfiles data and regenerate
rm -rf %{installdir}/static/*
%{app} collectstatic --noinput  > /dev/null
# Remove root-owned logged files just created by collectstatic
rm -rf /var/log/%{nickname}/*
# Touch the wsgi file to get the app reloaded by mod_wsgi
touch %{installdir}/django.wsgi

%pre
if [ "$1" -gt "1" ]; then
  # Nuke any staticfiles before upgrading to this version
  rm -rf %{installdir}/static
fi

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
%attr(-,apache,,apache) /var/log/%{nickname}
%attr(-,apache,,apache) /var/lib/%{nickname}
%attr(-,apache,,apache) /usr/share/%{nickname}
%attr(710,root,apache) /etc/%{nickname}
%attr(640,root,apache) /etc/%{nickname}/settings.py
%attr(640,root,apache) /etc/%{nickname}/%{nickname}.conf
%config(noreplace) /etc/%{nickname}/settings.py
%config(noreplace) /etc/%{nickname}/%{nickname}.conf

%config /etc/httpd/conf.d/%{nickname}.ccg
