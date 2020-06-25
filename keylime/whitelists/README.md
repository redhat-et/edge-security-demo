# Keylime Whitelist Files

This folder contains the whitelists needed for each agent running machine
to be provisioned

To create a whitelist, run this on the target machine:

```
keylime/scripts/create_whitelist.sh whitelist_${machine_type}.txt sha256sum
```
