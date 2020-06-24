import os
import asyncio

async def execute(revocation):
    """Node fail over script

    This script will be sent to the OpenShift controller along with a payload/
    folder.
    When a node is compromised. Keylime verifier will inform all machines
    running an agent to peform location actions. The local action in this case
    is to run `oc` command and migrate the pod to the 2nd node.
    """
    if revocation['type']!='revocation':
        return
    # Code goes here
