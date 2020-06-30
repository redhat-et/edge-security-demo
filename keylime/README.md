# Keylime Demo Files

This folder contains the various files needed for Keylime, such as configuration
autorun scripts and payload / revocation scripts, whitelists and exclude lists.

Using a controller as an example, the following actions would be followed.

Firstly the `keylime.conf.controller` should be copied to the controller machine
as `/etc/keylime.conf`. This will need the following values customized:

`cloudverifier_ip = ${verfier_ip}`

`registrar_ip = ${registrar_ip}`

From the demo machine, perform the following steps:

Ensure you have the `payloads` folder for your machine type, so in this instance
copy `payloads\controller_payload` to your local machine used for running the demo.

Ensure you have the `whitelist_${machine_type}.txt` for your machine type (in
  our case `whitelist_controller.txt`).

Ensure you have the `excludes_${machine_type}.txt` for your machine type (in
  our case `excludes_controller.txt`).

Start the following services on controller machine:

`tpm_serverd`

`systemctl restart tpm2-abrmd`

`keylime_ima_emulator`

`keylime_agent`

From the machine that is driving the demo, use the `keylime_tenant` command
to put the machine into IMA monitoring state.

```
keylime_tenant -v 127.0.0.1 -t 127.0.0.1 -f /root/excludes.txt -u ${UUID} --whitelist /root/whitelist_controller.txt --exclude /root/excludes_controller.txt --cert /root/democa --include /root/controller_payload -c add
```

The controller machine will then enter into a running state. When the 1st
OpenShift node is compromised the `keylime_agent` on the controller will run a
local action of `local_action_node_failover`.

This will then failover the pod to the 2nd OpenShift node.
