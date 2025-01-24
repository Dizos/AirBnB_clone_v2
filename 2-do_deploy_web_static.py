#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""
from fabric.api import *
import os

# SSH configuration
env.hosts = ['54.157.32.137', '52.55.249.213']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    
    Args:
        archive_path (str): Path to the archive to be deployed
    
    Returns:
        bool: True if deployment successful, False otherwise
    """
    # Validate archive existence
    if not os.path.exists(archive_path):
        return False

    try:
        # Filename parsing
        basename = os.path.basename(archive_path)
        name_no_ext = os.path.splitext(basename)[0]
        remote_path = f'/tmp/{basename}'
        release_path = f'/data/web_static/releases/{name_no_ext}'

        # Upload archive
        put(archive_path, remote_path)

        # Create release directory
        run(f'mkdir -p {release_path}')

        # Extract archive
        run(f'tar -xzf {remote_path} -C {release_path}')

        # Clean up remote archive
        run(f'rm {remote_path}')

        # Move contents
        run(f'mv {release_path}/web_static/* {release_path}/')
        run(f'rm -rf {release_path}/web_static')

        # Update symbolic link
        run('rm -rf /data/web_static/current')
        run(f'ln -s {release_path} /data/web_static/current')

        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
