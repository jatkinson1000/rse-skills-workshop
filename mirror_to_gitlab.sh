#!/usr/bin/env bash
#
# Script to set up mirroring from GitHub to GitLab. Requires ssh access to both.
# Clone github git file as a mirror, add a gitlab remote, push to gitlab as mirror.
# Can be run from inside main repo.

rm -rf power-up-python.git
git clone --mirror git@github.com:jatkinson1000/rse-skills-workshop.git
cd power-up-python.git
git remote add gitlab git@gitlab.com:jatkinson1000/power-up-python.git
git push --mirror gitlab
