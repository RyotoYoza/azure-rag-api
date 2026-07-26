# VPN: Repeated Disconnections and Failed Connections

## Scope
Applies to all corporate laptops running the Aegis VPN client on the `CORP-JP-PROD` profile. Site-to-site tunnels used by the Kumagaya lab network are out of scope and handled by the Network team via queue `NET-L3`.

## Required client version
The minimum supported client version is **5.2.4**. Versions earlier than 5.2.0 fail silently: the client shows "Connected" for roughly 40 seconds and then drops with no error dialog and no entry in the user-visible log. Confirm the version from the client's About panel or by running the version check described in the useful commands document. Client upgrades are pushed through Intune under the assignment group `INT-VPN-CLIENT-JP`; if the machine has not checked in for more than 14 days it will still be on the old build.

## Certificate expiry (most common root cause)
The `JP-Cert-2026` machine certificate is required for the `CORP-JP-PROD` profile. It expires annually on **31 March** and is re-issued automatically by Intune two weeks before expiry, provided the device has completed a successful check-in during that window. Devices that were powered off or off-network for the whole re-issue window will hold an expired certificate and will show error `AEG-4412` in the client log.

To confirm: open the certificate store for the local machine, look under Personal, and check the expiry date on the certificate issued to `JP-Cert-2026`. If it is expired or absent, force an Intune sync from Company Portal and wait ten minutes. If the certificate does not reappear, escalate to `EUC-L2` with the device serial number and the output of the client log.

## Split tunnel and bandwidth symptoms
Users on the `CORP-JP-PROD` profile route only corporate subnets through the tunnel. If a user reports that general internet browsing is slow while connected, check whether they have been placed on the legacy `CORP-JP-FULL` profile, which forces all traffic through the Tokyo concentrator. The legacy profile is retained only for the Finance shared-services group and should not appear on standard user devices. Moving a user off the legacy profile requires an approval from the profile owner recorded in the ticket.

## Repeated drops every 8 hours
A disconnection almost exactly every 8 hours is expected behaviour, not a fault. The concentrator enforces a maximum session lifetime of 8 hours and requires re-authentication. Users who work longer shifts should be told to expect one reconnection prompt per shift. If drops occur at intervals shorter than 30 minutes, capture the client log and attach it to the ticket before escalating.

## Wi-Fi roaming
Drops that happen only when the user walks between floors are usually access point roaming, not VPN. The Aegis client tolerates a network change of up to 12 seconds before tearing down the tunnel. Confirm by asking whether the drop coincides with movement, and if so route the ticket to `NET-L2` rather than `EUC-L2`.

## Escalation
Escalate to `EUC-L2` with: device serial, client version, certificate expiry date, profile name, the contents of the client log covering the failure, and whether the user is on corporate Wi-Fi, home broadband, or mobile tethering. Tickets without the client log are returned to the queue.
