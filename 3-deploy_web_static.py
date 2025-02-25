#!/usr/bin/python3
# Fabric script (based on the file 2-do_deploy_web_static.py) that creates and
# distributes an archive to your web servers, using the function deploy

from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['52.91.126.74', '34.224.15.231']


def do_pack():
    """ generates a .tgz archive from the contents of the web_static folder """
    try:
        local("mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file))
        return file
    except Exception as e:
        # print(f"Error during packaging: {e}")
        return None


def do_deploy(archive_path):
    """ distributes an archive to your web servers """
    if not path.exists(archive_path):
        print(f"Error: Archive not found at {archive_path}")
        return False

    try:
        put(archive_path, "/tmp/")
        file = archive_path.split("/")[-1]
        folder = "/data/web_static/releases/" + file.split(".")[0]
        run("rm -rf {}".format(folder))
        run("mkdir -p {}".format(folder))
        run("tar -xzf /tmp/{} -C {}".format(file, folder))
        run("rm /tmp/{}".format(file))
        run("mv {}/web_static/* {}".format(folder, folder))
        run("rm -rf {}/web_static".format(folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder))
        print("New version deployed!")
        return True
    except Exception as e:
        # print(f"Error during deployment: {e}")
        return False


def deploy():
    """ creates and distributes an archive to your web servers """
    try:
        archive_path = do_pack()
        if archive_path:
            value = do_deploy(archive_path)
            return value
        else:
            return False
    except Exception as e:
        # print(f"Error during deployment: {e}")
        return False
