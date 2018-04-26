#!/usr/bin/env bash
#######################################################################
#
#  Project......: setup_env.sh
#  Creator......: matteyeux
#  Description..: https://help.github.com/articles/configuring-a-remote-for-a-fork/ and
#				  https://help.github.com/articles/syncing-a-fork/
#  Type.........: Public
#
######################################################################
# Language :
#               bash
# Version : 0.1

# Specify a new remote upstream repository that will be synced with the fork
git remote add upstream https://github.com/matteyeux/autochecker

# Verify the new upstream repository you've specified for your fork
git remote -v

# Fetch the branches and their respective commits from the upstream repository
git fetch upstream

# Check out your fork's local master branch.
git checkout master

# Merge the changes from upstream/master into your local master branch.
git merge upstream/master