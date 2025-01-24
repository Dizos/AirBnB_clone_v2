#!/usr/bin/python3
"""
Fabric script to pack and deploy web_static to web servers
"""
from fabric.api import *
import os
from datetime import datetime

def do_pack():
    """
    Creates a compressed archive of web_static folder
    
    Returns:
        str: Path to created archive, or None if failed
    """
    # Ensure versions directory exists
    local('mkdir -p versions')
    
    # Generate archive name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = f'versions/web_static_{timestamp}.tgz'
    
    try:
        # Create compressed archive
        local(f'tar -czvf {archive_path} web_static')
        
        return archive_path
    except Exception:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    
    Args:
        archive_path (str): Path to archive to deploy
    
    Returns:
        bool: True if deployment successful, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Filename parsing
        basename = os.path.basename(archive_path)
        name_no_ext = os.path.splitext(basename)[0]
        remote_path = f'/tmp/{basename}'
        release_path = f'/data/web_static/releases/{name_no_ext}'

        # Upload and deploy
        put(archive_path, remote_path)
        run(f'mkdir -p {release_path}')
        run(f'tar -xzf {remote_path} -C {release_path}')
        run(f'rm {remote_path}')
        run(f'mv {release_path}/web_static/* {release_path}/')
        run(f'rm -rf {release_path}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {release_path} /data/web_static/current')

        return True
    except Exception:
        return False

def deploy():
    """
    Create and distribute archive to web servers
    
    Returns:
        bool: True if deployment successful, False otherwise
    """
    # Pack the archive
    archive_path = do_pack()
    
    # Check if packing was successful
    if not archive_path:
        return False
    
    # Deploy to servers
    return do_deploy(archive_path)

# SSH configuration
env.hosts = ['54.157.32.137', '52.55.249.213']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'
