# A centos instance for building RPM packages
node default {
  $custom_hostname = 'aws-rpmbuild-centos6.ec2.ccgapps.com.au'
  include role::rpmbuild::sydney

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
