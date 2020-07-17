#!/bin/bash
#Script to install all packages to run the Keylime agent

#To clear cached RPM repository metadata and perform a system upgrade
rpm-ostree cleanup -m
rpm-ostree upgrade

# Updating base packages
# Few of the packages that we need to install have requirements of newer verisons of base packages
# rpm-ostree isn't like a normal package manager and can't update already installed packages that are in the base layer.
# So we need to manually download the RPMs and `rpm-ostree override replace` them before we can `rpm-ostree install` the desired packages.
# Example: dbus-devel requires dbus-libs-1.12.20-1 instead of dbus-libs-1.12.18-1 which is a base package on FCOS

curl -L -O http://download-node-02.eng.bos.redhat.com/fedora/linux/updates/32/Everything/x86_64/Packages/d/dbus-libs-1.12.20-1.fc32.x86_64.rpm

curl -L -O http://download-node-02.eng.bos.redhat.com/fedora/linux/updates/32/Everything/x86_64/Packages/g/glib2-2.64.3-2.fc32.x86_64.rpm 

curl -L -O http://download-node-02.eng.bos.redhat.com/fedora/linux/updates/32/Everything/x86_64/Packages/p/pcre2-10.35-3.fc32.x86_64.rpm

curl -L -O http://download-node-02.eng.bos.redhat.com/fedora/linux/updates/32/Everything/x86_64/Packages/p/pcre2-syntax-10.35-3.fc32.noarch.rpm 

rpm-ostree override replace ./dbus-libs-1.12.20-1.fc32.x86_64.rpm ./glib2-2.64.3-2.fc32.x86_64.rpm ./pcre2-syntax-10.35-3.fc32.noarch.rpm ./pcre2-10.35-3.fc32.x86_64.rpm

# Installing packages
# `rpm-ostree install ...` adds packages that are not a part of the original OSTree as "LayeredPackages"

rpm-ostree install automake \
dbus-devel \
gcc \
git \
glib2-devel \
glib2-static \
gnulib \
libselinux-python3 \
libtool \
make \
openssl-devel \
python3-cryptography \
python3-dbus \
python3-devel \
python3-m2crypto \
python3-pip \
python3-setuptools \
python3-sqlalchemy \
python3-simplejson \
python3-tornado \
python3-virtualenv \
python3-yaml \
python3-zmq \
redhat-rpm-config \
tpm2-abrmd \
tpm2-tools \
tpm2-tss \
uthash-devel \
wget \
keylime 

# Reboot to apply changes

systemctl reboot
