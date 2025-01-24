# Puppet manifest to set up web static infrastructure for AirBnB clone project

file { '/data':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { [
  '/data/web_static',
  '/data/web_static/releases',
  '/data/web_static/shared',
  '/data/web_static/releases/test'
]:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => "<html>\n  <head>\n  </head>\n  <body>\n    ALX\n  </body>\n</html>",
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

package { 'nginx':
  ensure => installed,
}

file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "server {
    listen 80 default_server;
    location /hbnb_static/ {
        alias /data/web_static/current/;
    }
  }",
  notify => Service['nginx'],
}

service { 'nginx':
  ensure => running,
  enable => true,
}
