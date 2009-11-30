from fabric.api import *
import os

def test():
    if os.path.exists("./project-for-testing"):
        local("mv ./project-for-testing ./project")
    local("bin/django test tagging")
    local("mv ./project ./project-for-testing")

