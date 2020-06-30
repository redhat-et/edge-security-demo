import os
import asyncio

async def execute(revocation):
    """Container action script

    This script will be sent to the Containers running the tensorflow application
    When the Pod fails, this script will be executed locally on the container.
    """
    if revocation['type']!='revocation':
        return
    # Code goes here
