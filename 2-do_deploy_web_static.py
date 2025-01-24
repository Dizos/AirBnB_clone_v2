#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""
from fabric import task
from fabric.api import env, put, run
import os

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'

@task
def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    
    Args:
        archive_path (str): Path to the archive to be deployed
    
    Returns:
        bool: True if deployment successful, False otherwise
    """
    # Check if archive file exists
    if not os.path.exists(archive_path):
        return False

    try:
        # Get filename without path
        filename = os.path.basename(archive_path)
        no_ext = os.path.splitext(filename)[0]
        
        # Remote paths
        remote_tmp_path = f'/tmp/{filename}'
        remote_release_path = f'/data/web_static/releases/{no_ext}'
        
        # Upload archive to remote tmp directory
        put(archive_path, remote_tmp_path)
        
        # Create release directory
        run(f'mkdir -p {remote_release_path}')
        
        # Extract archive
        run(f'tar -xzf {remote_tmp_path} -C {remote_release_path}')
        
        # Remove uploaded archive
        run(f'rm {remote_tmp_path}')
        
        # Move web_static contents 
        run(f'mv {remote_release_path}/web_static/* {remote_release_path}/')
        run(f'rm -rf {remote_release_path}/web_static')
        
        # Update symbolic link
        run('rm -rf /data/web_static/current')
        run(f'ln -s {remote_release_path} /data/web_static/current')
        
        return True
    except Exception:
        return False
