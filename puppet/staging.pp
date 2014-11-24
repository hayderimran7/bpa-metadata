# BPA Metadata production
node default {
    include ccgcommon
    include ccgcommon::source
    include ccgapache
    include python

    include repo::repo::ius
    include repo::repo::pgrpms
    include repo::repo::ccgtesting

    include monit
    include globals

    $django_config = {
      deployment  => 'staging',
      dbdriver    => 'django.db.backends.postgresql_psycopg2',
      dbhost      => $globals::dbhost_rds_syd_postgresql_prod,
      dbserver    => $globals::dbhost_rds_syd_postgresql_prod,
      dbname      => 'bpam_staging',
      dbuser      => $globals::dbuser_syd_staging,
      dbpass      => $globals::dbpass_syd_staging,
      memcache    => $globals::memcache_syd,
      secret_key   => 'asdfj*&^*&^hhqwertyLAHLAHLAH424242',
      admin_email => $globals::system_email,
      allowed_hosts => 'localhost .ccgapps.com.au',
    }

    ccgdatabase::postgresql::db { $django_config['dbname']:
      user     => $django_config['dbuser'],
      password => $django_config['dbpass'],
    }

    django::config { 'bpam':
      config_hash => $django_config,
    } ->
    package {'bpa-metadata':
      ensure => $ensure,
      provider => 'yum_nogpgcheck'
    } ->
    django::syncdbmigrate{'bpam':
      dbsync  => true,
      notify  => Service[$ccgapache::params::service_name],
      require => [
        Ccgdatabase::Postgresql::Db[$django_config['dbname']],
        Package['bpa-metadata'],
        Django::Config['bpam'] ]
    }

    # cronjob to run link checker
    cron { "link-checker":
       ensure  => present,
       command => "cd /usr/local/src/bpam && vpython-bpam manage.py runscript url_checker",
       user    => 'ec2-user',
       minute  => [ 0 ],
       hour  => [ 7 ],
    }

   case $::osfamily {
      'RedHat', 'Linux': {
        $packages = [
          'graphviz',
          'gdal-devel.x86_64',
          'libxml2-devel',
          'libxslt-devel',
          'proj-devel',
          'tree',
          'tmux',
          'cowsay']
      }
      'Debian': {
        $packages = [
          'tree',
          'tmux']
      }
   }

   package {$packages: ensure => installed}

}
