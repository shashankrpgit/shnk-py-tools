# Robot Framework: Interface Verification

This Robot Framework script automates the verification of interface status (enabled and link up) on a remote DUT.

## ?? What It Does

- Verifies if the interface is marked "enabled" in the config
- Runs a monitor to check if the interface is "LINK_UP"

## ?? Usage

Set the `intList` variable in your setup:

```python
"intList": "EIF1,EIF2"

## Then, call the keyword:

Verify Interface   ${variables['intList']}
