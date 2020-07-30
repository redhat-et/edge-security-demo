import os
import asyncio

async def execute(revocation):
    if revocation['type']!='revocation':
        return
    os.remove("/tmp/keylime_approved")
