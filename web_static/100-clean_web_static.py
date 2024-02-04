#!/usr/bin/python3
"""
Deletes out-of-date archives
fab -f 100-clean_web_static.py do_clean:number=2
    -i ssh-key -u ubuntu > /dev/null 2>&1
"""

import os
from fabric.api import *

# Define the lists of hosts
env.hosts = ['54.84.10.163', '52.3.255.87']


def do_clean(number=0):
    """
    Delete out-of-date archives.

    Args:
        number (in): The number of archives to keep. Defaults to 0.

    If number is 0 or 1, keeps only the most recent archive. If number is 2,
    keeps the most and second-most recent archives, etc.
    """

    # Convert number to integer
    number = int(number)

    # Ensure number is at least 1
    number = max(number, 1)

    # Get list of archives sorted by modification time
    archives = sorted(os.listdir("versions"))

    # Remove the specified number of latest archives
    [archives.pop() for i in range(number)]

    # Delete local archives
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    # Switch to remote directory
    with cd("/data/web_static/releases"):
        # Get list of archives sorted by modification time
        archives = run("ls -tr").split()
        # Filter out only archives related to web_static
        archives = [a for a in archives if "web_static_" in a]
        # Remove the specified number of latest archives
        [archives.pop() for i in range(number)]
        #Delete remote archives
        [run("rm -rf ./{}".format(a)) for a in archives]
