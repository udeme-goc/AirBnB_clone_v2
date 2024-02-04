#!/usr/bin/python3
"""
Fabric script to generate a tgz archive of web_static directory.
Execute: fab -f 1-pack_web_static.py do_pack
"""

from datetime import datetime
from fabric.api import *


def do_pack():
    """
    Create a tgz archive of web_static directory.
    """

    # Get current date and time
    current_time = datetime.now()

    # Define archive filename with timestamp
    archive_name = 'web_static_' + current_time.strftime("%Y%m%d%H%M%S") + '.tgz'

    # Create versions directory if it doesn't exist
    local('mkdir -p versions')

    # Create tgz archive
    create_archive = local('tar -cvzf versions/{} web_static'.format(archive_name))

    # Create if archive creation was successful
    if create_archive.succeeded:
        return 'versions/' + archive_name   # Return archive path
    else:
        return None # Return None if archive creation failed
