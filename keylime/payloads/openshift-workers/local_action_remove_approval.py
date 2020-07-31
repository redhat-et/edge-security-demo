import os
import asyncio

async def execute(revocation):
    logging.info('REVOCATION: ' + pp.pformat(revocation))
    if revocation['type']!='revocation':
        return

    approved_path = "/tmp/keylime_approved"
    if os.path.exists(approved_path):
        os.remove(approved_path)
