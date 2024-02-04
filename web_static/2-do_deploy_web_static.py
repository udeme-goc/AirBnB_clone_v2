#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists

# Define the list of web servers
env.hosts = ['54.84.10.163', '52.3.255.87']

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    
    Args:
        archive_path (str): Path to the archive file to be deployed.
    
    Returns:
        bool: True if deployment is successful, False otherwise.
    """

    # Check if the archive exists
    if exists(archive_path) is False:
        return False

    try:
        # Extract filename and directory name from the archive path
        file_name = archive_path.split("/")[-1]
        directory_name = file_name.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload the archive to the remote server's /tmp/ directory
        put(archive_path, '/tmp/')

        # Create directory for the release and extract contents of the archive
        run('mkdir -p {}{}/'.format(path, directory_name))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, directory_name))

        # Remove the archive from the /tmp/ directory
        run('rm /tmp/{}'.format(file_name))

        # Move contents of extracted directory to parent directory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, directory_name))

        # Remove the now-empty web_static directory
        run('rm -rf {}{}/web_static'.format(path, directory_name))

        # Remove the existing /data/web_static/current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link pointing to the latest release
        run('ln -s {}{}/ /data/web_static/current'.format(path, directory_name))

        return True
    except Exception as e:
        print("Error deploying archive:", e)
        return False
