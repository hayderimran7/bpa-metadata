# A centos instance for building RPM packages
node default {
  include role::rpmbuild

  $packages = [ 
     'graphviz',
     'gdal-devel.x86_64',
     'libxml2-devel', 
     'libxslt-devel',
     'proj-devel',
     'tree',
     'tmux',
  ]
  package {$packages: ensure => installed}
}
