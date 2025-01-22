#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import env, local, run, cd, settings
import os

# Update these with your actual server IP addresses
env.hosts = ['100.26.231.45', '54.209.63.0']  # Replace with your actual IPs
env.user = 'ubuntu'
env.key_filename = 'your_ssh_private_key'  # Replace with your actual key path


def do_clean(number=0):
    """
    Deletes out-of-date archives

    Args:
        number (int): The number of archives to keep.
            If 0 or 1, keeps only the most recent archive.
            If 2, keeps the two most recent archives, etc.
    """
    try:
        # Convert number to integer if it's a string
        number = int(number)

        # Keep at least 1 archive
        if number < 1:
            number = 1

        # Clean local archives
        with settings(warn_only=True):
            # Check if versions directory exists
            if os.path.isdir("versions"):
                local_cmd = "ls -tr versions/*.tgz 2>/dev/null"
                archives = local(local_cmd, capture=True).split('\n')
                archives = [a for a in archives if a]  # Remove empty strings

                if len(archives) > number:
                    archives = archives[:-number]  # Keep the last 'number' of archives
                    for archive in archives:
                        local('rm -f {}'.format(archive))

        # Clean remote archives
        with settings(warn_only=True):
            with cd('/data/web_static/releases'):
                # List all web_static_* directories, excluding 'current'
                remote_cmd = "ls -td web_static_* 2>/dev/null"
                releases = run(remote_cmd).split('\n')
                releases = [r for r in releases if r and 'current' not in r]  # Remove empty strings and 'current'

                if len(releases) > number:
                    releases = releases[:-number]  # Keep the last 'number' of releases
                    for release in releases:
                        run('rm -rf {}'.format(release))

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    return True


if __name__ == "__main__":
    do_clean()
