# Local development setup for BPA Metadata
node default {
    include ccgcommon
    include ccgcommon::source
    include ccgapache
    include python

    include repo
    include repo::upgrade
    include repo::repo::ius
    include repo::repo::ccgtesting
    include repo::repo::ccgdeps
    class { 'yum::repo::pgdg93':
      stage => 'setup',
    }
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

    # set the swift secrets so the metadata can be downloaded.
    augeas { "swift_creds":
      incl => "/etc/environment",
      lens    => "shellvars.lns",
      changes => [
        "set SWIFT_USER $globals::bpa_swift_user",
        "set SWIFT_PASSWORD $globals::bpa_swift_password",
      ],
    }

    # the rpm also has these dependencies
    case $::osfamily {
        'RedHat', 'Linux': {
            $packages = [
                'libffi-devel',
                'graphviz-devel',
                'gdal',
                'proj-devel',
                'tree']
        }
        'Debian': {
            $packages = [
                'tree']
        }
    }
    package {$packages: ensure => installed}
}
