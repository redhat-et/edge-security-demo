# OKD Setup

How to create an OKD cluster on PnT Shared Infrasturcture (PSI) - 

1. Extract the binaries from the image using `oc`

    ` $ oc adm release extract --tools quay.io/openshift/okd:4.5.0-0.okd-2020-06-29-110348-beta6`

2. Copy the binaries into your PATH

    `$ export PATH=/path/to/binaries:$PATH`

3. Follow the remaining steps in the PSI setup document.

**NOTE**: According to [openshift/okd](https://github.com/openshift/okd), You need a 4.x version of oc to extract the installer and the latest client.

To install all the package dependencies to run Keylime agents on the node - 

1. List all the nodes

    `oc get nodes`

2. Start a shell session to one of the worker nodes

    `oc debug node/<node_name>`

3. The node root file system is mounted in the `/host` folder

    `chroot /host`

4. Confirm by checking the OS version on the node

    `cat /etc/redhat-release`

5. Because of the controlled mutability of FCOS, not all directories can be worked with

    `cd /tmp`

6. Download the `install_packages.sh` script and run it 

    `chmod +x install_packages.sh && ./install_packages.sh`

**NOTE**: The system will restart in order to choose the latest deployment and display all packages

Check the status of the deployment and list the packages installed using `rpm-ostree status`