#!/usr/bin/env python3
"""
Fabric script to deploy web static archives
"""
from fabric import Connection
from fabric import task
import os

@task
def do_deploy(c, archive_path):
    """
    Distributes an archive to web servers
    
    Args:
        c (Connection): Fabric connection
        archive_path (str): Path to archive file
    
    Returns:
        bool: True if deployment successful, False otherwise
    """
    # Check if archive exists
    if not os.path.exists(archive_path):
        return False
    
    try:
        # Get archive filename
        filename = os.path.basename(archive_path)
        no_ext = os.path.splitext(filename)[0]
        
        # Remote paths
        remote_tmp_path = f'/tmp/{filename}'
        remote_release_path = f'/data/web_static/releases/{no_ext}'
        
        # Upload archive
        c.put(archive_path, remote_tmp_path)
        
        # Create release directory
        c.run(f'mkdir -p {remote_release_path}')
        
        # Uncompress archive
        c.run(f'tar -xzf {remote_tmp_path} -C {remote_release_path}')
        
        # Remove uploaded archive
        c.run(f'rm {remote_tmp_path}')
        
        # Move contents
        c.run(f'mv {remote_release_path}/web_static/* {remote_release_path}/')
        c.run(f'rm -rf {remote_release_path}/web_static')
        
        # Update symbolic link
        c.run('rm -rf /data/web_static/current')
        c.run(f'ln -s {remote_release_path} /data/web_static/current')
        
        return True
    except Exception:
        return False

# Hosts configuration
env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = 'path/to/private_key'
