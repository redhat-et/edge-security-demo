import os
import asyncio

async def execute(revocation):
    """Node fail over script

    This script will be sent to the keylime_agent running on a machine
    which has an OpenShift client (oc) installed and configured.

    When a node is compromised this script will run `oc adm cordon` and
    `oc adm drain` commands to remove that worker node from the OpenShift
    cluster
    """
    if revocation['type']!='revocation':
        return

    # TODO - get the node name
    node_name = "XXX"
    rc = os.system("oc adm cordon {}".format(node_name))
    if rc != 0:
        print("Could not cordon node {}: Command failed with code {}".format(node_name, rc))
        return

    rc = os.system("oc adm drain {}".format(node_name))
    if rc != 0:
        print("Could not drain node {}: Command failed with code {}".format(node_name, rc))
        return
