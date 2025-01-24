# Puppet manifest for web static setup

# Ensure nginx is installed
package { 'nginx':
  ensure => installed,
}

# Create directory structure
file { [
  '/data',
  '/data/web_static',
  '/data/web_static/releases',
  '/data/web_static/shared',
  '/data/web_static/releases/test'
]:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create test index.html
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => "<html>\n  <head>\n  </head>\n  <body>\n    ALX\n  </body>\n</html>",
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Configure nginx
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => template('nginx/default.erb'),
  notify  => Service['nginx'],
}

# Ensure nginx is running
service { 'nginx':
  ensure => running,
  enable => true,
}
