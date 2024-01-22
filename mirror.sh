#!usr/bin/env bash
#
# Script to set up mirroring from GitLab to GitHub. Requires ssh access to both.
# Clone gitlab git file as a mirror, add a github remote, push to github as mirror.
# Can be run from inside main repo.

git clone --mirror git@gitlab.com:jatkinson1000/power-up-python.git
cd power-up-python.git
git remote add github git@github.com:jatkinson1000/power-up-python.git
git push --mirror github
