%define __python /usr/bin/python%{pybasever}
# sitelib for noarch packages
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define pyver 27
%define pybasever 2.7

%define app bpa-metadata
%define name %{app}
%define nickname bpam 
%define version 1.4.0
%define unmangled_version %{version}
%define release 1
%define webapps /usr/local/webapps
%define installdir %{webapps}/%{nickname}
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
NAME=%{nickname}

# Build from source dir
cd $CCGSOURCEDIR

# Make sure the standard target directories exist
# These two contain files owned by the RPM
mkdir -p %{settingsdir}
#mkdir -p %{staticdir}
# The rest are for persistent data files created by the app
mkdir -p %{logdir}
mkdir -p %{mediadir}
mkdir -p %{scratchdir}
mkdir -p %{sharedir}

# Create a python prefix with app requirements
mkdir -p %{buildinstalldir}

# Virtualenv
# Make a virtualenv and install the app's dependencies
virtualenv-%{pybasever} %{buildinstalldir}
. %{buildinstalldir}/bin/activate
# Use specific version of pip -- avoids surprises with deprecated options, etc.
pip install --force-reinstall --upgrade 'pip>=1.5,<1.6'
# Install package into the prefix
pip install --allow-unverified --allow-all-external --process-dependency-links ./%{nickname}
# Fix up paths in virtualenv, enable use of global site-packages
virtualenv-%{pybasever} --relocatable %{buildinstalldir}
find %{buildinstalldir} -name \*py[co] -exec rm {} \;
find %{buildinstalldir} -name no-global-site-packages.txt -exec rm {} \;
sed -i "s|`readlink -f ${RPM_BUILD_ROOT}`||g" %{buildinstalldir}/bin/*

# Strip out mention of rpm buildroot from the pip install record
find %{buildinstalldir} -name RECORD -exec sed -i -e "s|${RPM_BUILD_ROOT}||" {} \;

# Strip debug syms out of the compiled python modules which are in the
# build root.
find %{buildinstalldir} -name \*.so -exec strip -g {} \;

# tools are needed to populate the database from the excell spreadsheets
cp -r ./tools* %{buildinstalldir}/
cp deploy.sh %{buildinstalldir}/


# Create symlinks under install directory to real persistent data directories
APP_SETTINGS_FILE=`find %{buildinstalldir} -path "*/$NAME/settings.py" | sed s:^%{buildinstalldir}/::`
APP_PACKAGE_DIR=`dirname ${APP_SETTINGS_FILE}`
ln -sfT /var/log/%{nickname} %{buildinstalldir}/${APP_PACKAGE_DIR}/log
ln -sfT /var/lib/%{nickname}/scratch %{buildinstalldir}/${APP_PACKAGE_DIR}/scratch
ln -sfT /var/lib/%{nickname}/media %{buildinstalldir}/${APP_PACKAGE_DIR}/media

# Install settings conf file to /etc, and replace with symlink
install --mode=0640 -D centos/%{nickname}.conf.example %{buildroot}/etc/%{nickname}/%{nickname}.conf.example
install --mode=0640 -D %{nickname}/%{nickname}/prodsettings.py %{buildroot}/etc/%{nickname}/settings.py
ln -sfT /etc/%{nickname}/settings.py %{buildinstalldir}/${APP_PACKAGE_DIR}/prodsettings.py

mkdir -p %{staticdir}
ln -sfT %{installdir}/static %{buildinstalldir}/${APP_PACKAGE_DIR}/static

# temp fix to make defaultsettings importable
ln -sfT %{installdir}/defaultsettings %{buildinstalldir}/${APP_PACKAGE_DIR}/../defaultsettings

# Install WSGI configuration into httpd/conf.d
install -D centos/%{nickname}.ccg %{buildroot}/etc/httpd/conf.d/%{nickname}.ccg
ln -sfT ${APP_PACKAGE_DIR}/wsgi.py %{buildinstalldir}/django.wsgi

# Create symlinks to scripts in the virtualenv
mkdir -p %{buildroot}/%{_bindir}
ln -sfT %{installdir}/bin/manage.py %{buildroot}/%{_bindir}/%{nickname}
ln -sfT %{installdir}/deploy.sh %{buildroot}/%{_bindir}/%{nickname}-deploy.sh

%post
# Clear out staticfiles data and regenerate
rm -rf %{installdir}/static/*
%{nickname} collectstatic --noinput  > /dev/null
# Remove root-owned logged files just created by collectstatic
rm -rf /var/log/%{nickname}/*

# populate the db
# %{nickname}-deploy.sh ingest

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
%{_bindir}/%{nickname}-deploy.sh
%attr(-,apache,,apache) %{webapps}/%{nickname}
%attr(-,apache,,apache) /var/log/%{nickname}
%attr(-,apache,,apache) /var/lib/%{nickname}
# directory for metadata
%attr(-,apache,,apache) /var/www/metadata

%config /etc/httpd/conf.d/%{nickname}.ccg
%config(noreplace) /etc/%{nickname}/settings.py
/etc/%{nickname}/%{nickname}.conf.example



