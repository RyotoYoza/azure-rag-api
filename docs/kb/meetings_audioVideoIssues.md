# Meetings: Audio, Video, and Room Equipment

## Standard headsets
The supported headsets are the `HS-40` wired model and the `HS-70W` wireless model. The `HS-70W` requires the dongle it shipped with; dongles are paired at manufacture and are not interchangeable between units. A user reporting that their wireless headset stopped working after borrowing a colleague's dongle needs their original dongle, not a replacement headset.

## No audio at all
Check the application's own device selection first. The client remembers the last used device per machine, so a headset unplugged during a previous session leaves the application pointing at a device that no longer exists, and the user hears nothing while the operating system reports the headset as working normally. Reselecting the device inside the application resolves this in most cases.

If the operating system also shows no device, check whether the endpoint protection agent has blocked the driver. Blocked drivers appear in the agent panel under Recent Actions and require `EUC-L2` to release.

## Echo
Echo is almost always caused by two devices in the same physical room joined to the same meeting with speakers active. Ask how many people in the room are connected. Room systems should be the only joined device in a meeting room; laptops in the room should join muted or not at all. Software echo cancellation cannot compensate for two open microphones in one room.

## Poor video quality
The client reduces video resolution automatically when available bandwidth falls below 1.2 Mbps. On VPN, video traffic is excluded from the tunnel on the `CORP-JP-PROD` profile, so poor video while connected to VPN is a local internet problem rather than a VPN problem. Users on the legacy `CORP-JP-FULL` profile do route meeting traffic through the concentrator and will see degraded quality at peak hours; this is a known limitation of that profile.

## Meeting rooms
Room systems in Kumagaya are named by floor and room, in the pattern `KMG-3F-A` through `KMG-3F-D`. Each room console must show "Ready" on its home screen; a console showing "Signing in" for more than ten minutes has lost its resource account session and must be restarted from the console settings, not by unplugging the display.

Room bookings must be made against the room resource account for the console to display the meeting. A meeting created without inviting the room will not appear on the console, and the participants will need to join manually from a laptop. This is the most frequent room-related ticket and is a booking error rather than a fault.

## Content sharing
Wireless sharing in rooms requires the sharing client and the room code shown on the display. Codes rotate every 24 hours. HDMI sharing bypasses the code and is the reliable fallback when a guest cannot install the client. Guest laptops cannot join the corporate wireless network and should use the guest network, which does not permit wireless sharing.

## Escalation
Escalate room hardware faults to `AV-L2` with the room name, the console status text, and whether the fault affects audio, video, or sharing. Escalate client-side audio faults to `EUC-L2` with the device serial, headset model, and whether the fault occurs in all applications or only one.
