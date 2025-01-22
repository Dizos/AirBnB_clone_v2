#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of web_static.
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of web_static folder.
    
    Returns:
        str: path to the archive if successful, None otherwise
    """
    try:
        # Create versions directory if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")
        
        # Generate archive name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        
        # Create tar archive using local from fabric
        local("tar -cvzf {} web_static".format(archive_path))
        
        # Return archive path if successful
        if os.path.exists(archive_path):
            print("web_static packed: {} -> {}Bytes".format(
                archive_path, os.path.getsize(archive_path)))
            return archive_path
        return None
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
