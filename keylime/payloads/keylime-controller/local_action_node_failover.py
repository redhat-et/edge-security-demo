import os
import asyncio
import subprocess

"""Node fail over script

This script will be sent to the keylime_agent running on a machine
which has an OpenShift client (oc) installed and configured.

When a node is compromised this script will run `oc adm cordon` and
`oc adm drain` commands to remove that worker node from the OpenShift
cluster
"""

async def execute(revocation):
    if revocation['type']!='revocation':
        return

    node_name = 'mpeters-okd-zxrh5-' + revocation['agent_id']
    cmd = "KUBECONFIG=/etc/kubeconfig /usr/local/bin/oc adm cordon {}".format(node_name)
    subprocess.call(cmd, shell=True)
    cmd = "KUBECONFIG=/etc/kubeconfig /usr/local/bin/oc adm drain {} --force=true --ignore-daemonsets --delete-local-data".format(node_name)
    subprocess.call(cmd, shell=True)
