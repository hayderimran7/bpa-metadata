Installation with CentOS and MySQL
==================================

Install the desired database and driver::

    yum install mysql-server mysql MySQL-python

Add the CCG yum repo::

    fixme

Install the package::

    yum install bpa-metadata


Set up the database, as in the django docs::

    sudo mysql
    CREATE DATABASE bpam CHARACTER SET utf8;
    GRANT ALL ON bpam.* TO bpam@localhost IDENTIFIED BY 'bpam';
    \q

    sudo bpam syncdb
    sudo bpam migrate
    sudo bpam collectstatic


Visit your installation at http://my-web-host/bpa-metadata/admin/

Logs will be in ``/var/log/httpd/bpa-metadata.error_log`` and
``/var/log/bpa-metadata``.

