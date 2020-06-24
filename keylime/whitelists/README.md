# Keylime Whitelist Files

This folder contains the whitelists needed for each machine to be provisioned
on machine running the keylime agent.

To create a whitelist, run this on the target machine:

```
keylime/scripts/create_whitelist.sh whitelist_${machine_type}.txt sha256sum
```
