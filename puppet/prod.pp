# BPA Metadata production
node default {
    include ccgcommon
    include ccgcommon::source
    include ccgapache
    include python

    include repo
    include repo::repo::ius
    include repo::repo::ccgtesting
    include yum::repo::pgdg93

    include monit
    include globals

    $django_config = {
      release     => '1.3.0',
      deployment  => 'production',
      dbdriver    => 'django.db.backends.postgresql_psycopg2',
      dbserver    => $globals::dbhost_rds_syd_postgresql_prod,
      dbhost      => $globals::dbhost_rds_syd_postgresql_prod,
      dbname      => 'bpam_prod',
      dbuser      => $globals::dbuser_syd_prod,
      dbpass      => $globals::dbpass_syd_prod,
      memcache    => $globals::memcache_syd,
      secret_key   => $globals::secretkey_aws_bpa_metadata,
      admin_email => $globals::system_email,
      allowed_hosts => 'localhost www.ccgapps.com.au ccgapps.com.au',
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
