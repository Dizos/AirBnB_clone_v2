#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""

from fabric.api import env, local, put, run
from datetime import datetime
import os

env.hosts = ['<IP web-01>', 'IP web-02']


def do_pack():
    """
    Generates a .tgz archive from the contents of web_static folder
    """
    try:
        if not os.path.exists("versions"):
            local("mkdir -p versions")
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    
    Args:
        archive_path: path to the archive to deploy
    
    Returns:
        True if successful, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract filename and folder name from archive path
        file_name = os.path.basename(archive_path)
        folder_name = file_name.replace('.tgz', '')
        
        # Upload archive to /tmp/ directory on server
        put(archive_path, '/tmp/{}'.format(file_name))
        
        # Create directory for release
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        
        # Extract archive to the releases folder
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            file_name, folder_name))
        
        # Remove the uploaded archive
        run('rm /tmp/{}'.format(file_name))
        
        # Move contents from web_static folder to release folder
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(folder_name, folder_name))
        
        # Remove the now-empty web_static folder
        run('rm -rf /data/web_static/releases/{}/web_static'.format(folder_name))
        
        # Remove current symbolic link if it exists
        run('rm -rf /data/web_static/current')
        
        # Create new symbolic link
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(
            folder_name))
        
        print('New version deployed!')
        return True
    except:
        return False


def deploy():
    """
    Creates and distributes an archive to web servers
    
    Returns:
        True if successful, False otherwise
    """
    # Create archive
    archive_path = do_pack()
    if not archive_path:
        return False
    
    # Deploy archive
    return do_deploy(archive_path)
