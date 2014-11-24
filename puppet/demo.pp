# BPA Metadata production
node default {
  include ccgcommon
  include ccgcommon::source
  include ccgapache
  include python
  include repo::repo::ius
  include repo::repo::ccgtesting
  include yum::repo::pgdg93
  include monit
  include globals

  $django_config = {
    deployment  => 'staging',
    dbdriver    => 'django.db.backends.postgresql_psycopg2',
    dbhost      => '',
    dbname      => 'bpam',
    dbuser      => 'bpam',
    dbpass      => 'bpam',
    memcache    => $globals::memcache_syd,
    secretkey   => 'm0th3rl0ad0ffailf0ry0urighth3r3m0f0',
    admin_email => $globals::system_email,
    allowed_hosts => 'localhost',
  }

  ccgdatabase::postgresql::db { $django_config['dbname']:
    user     => $django_config['dbuser'],
    password => $django_config['dbpass'],
  }

  package {'bpa-metadata':
    ensure => $ensure,
    provider => 'yum_nogpgcheck'
  }

  django::config { 'bpam':
    config_hash => $django_config,
  }
  ->
  django::syncdbmigrate{'bpa-metadata':
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
