# BPA Metadata production
node default {
    include ccgcommon
    include ccgcommon::source
    include ccgapache
    include python
    include repo::epel
    include include::ius
    include repo::pgrpms
    include repo::ccgtesting
    include monit
    include globals

    $django_config = {
      deployment  => 'production',
      dbdriver    => 'django.db.backends.postgresql_psycopg2',
      dbhost      => '',
      dbname      => 'bpam_prod',
      dbuser      => 'bpam',
      dbpass      => 'bpam',
      memcache    => $globals::memcache_syd,
      secretkey   => 'asdfj*&^*&^hhqwertyLAHLAHLAH424242',
      admin_email => $globals::system_email,
      allowed_hosts => 'localhost',
    }

    ccgdatabase::postgresql::db { $django_config['dbname']:
      user     => $django_config['dbuser'],
      password => $django_config['dbpass'],
    }

  package {'bpa_metadata':
    ensure => $ensure,
    provider => 'yum_nogpgcheck'
  } ->
  django::config { 'bpa_metadata':
    config_hash => $django_config,
  } ->
  django::syncdbmigrate{'bpa_metadta':
    dbsync  => true,
    notify  => Service[$ccgapache::params::service_name],
    require => [
      Ccgdatabase::Postgresql::Db[$django_config['dbname']],
      Package['bpa_metadata'],
      Django::Config['bpa_metadata'] ]
  }

  $dbdriver = 'django.db.backends.postgresql_psycopg2'

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
