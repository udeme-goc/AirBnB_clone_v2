#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers

execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

# Define the list of web servers
env.hosts = ['54.160.77.90', '10.25.190.21']

def do_pack():
    """
    Generates a tgz archive containing web_static folder.
    
    Returns:
        str: Path to the generated archive on success, None on failure.
    """
    try:
        # Generate timestamp for the archive filename
        date = datetime.now().strftime("%Y%m%d%H%M%S")

        # Create 'versions' directory if it doesn't exist
        if isdir("versions") is False:
            local("mkdir versions")

        # Compress the web_static folder into a tgz archive
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        
        return file_name
    except Exception as e:
        print("Error packing archive:", e)
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it.
    
    Args:
        archive_path (str): Path to the archive file to be deployed.
    
    Returns:
        bool: True if deployment is successful, False otherwise.
    """
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


def deploy():
    """
    Creates and distributes an archive to the web servers.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    
    return do_deploy(archive_path)
