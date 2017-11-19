#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

TMP_DIR=tmp

rm -rf ${TMP_DIR}
mkdir ${TMP_DIR} ; cd ${TMP_DIR}

sudo apt-get update ; sudo apt-get install libgconf2-4 libnss3-1d libxss1 unzip xvfb

if ! dpkg -l | fgrep google-chrome-stable > /dev/null ; then
    echo "Installing Google Chrome"
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    #Install the package, forcing install of dependencies:
    sudo dpkg -i --force-depends google-chrome-stable_current_amd64.deb
    #In case any dependencies didn't install (you would have a warning or failure message for this), you can force them via:
    sudo apt-get install -f
fi

if ! test -e /opt/google/chrome/chromedriver ; then
    echo "Installing chromedriver"
    wget 'https://chromedriver.storage.googleapis.com/2.33/chromedriver_linux64.zip'
    unzip chromedriver_linux64.zip
    sudo cp chromedriver /opt/google/chrome/
fi

cd -
