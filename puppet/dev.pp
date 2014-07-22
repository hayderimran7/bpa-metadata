# Local development setup for BPA Metadata
node default {
    include ccgcommon
    include ccgcommon::source
    include ccgapache
    include python
    include repo::ius
    include repo::epel
    include repo::pgrpms
    include repo::ccgtesting
    include ccgdatabase::postgresql::devel
    include monit
    include globals

    $dbname = 'bpam'
    $dbuser = 'bpam'
    $dbpass = 'bpam'

    ccgdatabase::postgresql::db { $dbname :
      user     => $dbuser, 
      password => $dbpass
    } ->
    exec {'CREATE EXTENSION postgis':
        command => "/usr/pgsql-9.3/bin/psql ${dbname} -c 'CREATE EXTENSION postgis'",
        returns => [0, 1],
        logoutput => true,
        user => "postgres"
    } ->
    exec {'CREATE EXTENSION postgis_topology':
        command => "/usr/pgsql-9.3/bin/psql ${dbname} -c 'CREATE EXTENSION postgis_topology'",
        returns => [0, 1],
        logoutput => true,
        user => "postgres"
    }

    # cronjob to run link checker
    cron { "link-checker":
        ensure  => present,
        command => "cd /usr/local/src/bpam && vpython-bpam manage.py runscript url_checker",
        user    => 'ccg-user',
        minute  => [ 0 ],
        hour  => [ 7 ],
    }

    $django_config = {
      bpa_swift_user  => $globals::bpa_swift_user,
      bpa_swift_password  => $globals::bpa_swift_password,
    }

    django::config {"bpa_metadata":
      config_hash => $django_config,
    }


    # the rpm also has these dependencies
    case $::osfamily {
        'RedHat', 'Linux': {
            $packages = [
                'libffi-devel',
                'graphviz-devel',
                'gdal',
                'proj-devel',
                'postgis2_93',
                'tree']
        }
        'Debian': {
            $packages = [
                'tree']
        }
    }
    package {$packages: ensure => installed}
}
