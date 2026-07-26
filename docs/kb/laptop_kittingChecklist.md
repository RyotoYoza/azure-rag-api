# Laptop Kitting Checklist (Standard Build)

## Standard hardware models
Two models are in current rotation: the `LT-STD-14` for general office users and the `LT-ENG-16` for engineering and lab users. The `LT-STD-13`, retired in 2025, is no longer imaged and any request for one should be answered with the `LT-STD-14`. Loaner machines carry an asset tag prefixed `LN-` and are tracked in a separate inventory view.

## Imaging
Machines are imaged with Autopilot using the deployment profile `AP-JP-STANDARD`. The profile applies the Japanese regional settings, the corporate wallpaper, and the baseline application set. Imaging requires a wired connection: Autopilot enrolment over Wi-Fi frequently stalls at 82% on the device preparation step, and the machine must then be reset and restarted from the beginning. Always kit from the wired bench.

Expected imaging time is 45 to 60 minutes for the `LT-STD-14` and up to 90 minutes for the `LT-ENG-16` because of the additional lab application set.

## Baseline application set
The following are installed automatically by the profile and must be verified present before handover:

- Aegis VPN client, version 5.2.4 or later
- Company Portal
- The Office suite with the corporate licence applied
- Endpoint protection agent, showing status "Compliant" in the local agent panel
- The print client used by the management portal

Applications requested per-role, such as statistical or lab software, are installed after handover through Company Portal and are not part of the baseline.

## Asset registration
Before handover, record the device in the asset system with: serial number, asset tag, model code, assigned user ID, cost centre, and building code. The building code for Kumagaya is `JP-KMG`. Devices registered without a cost centre are rejected by the monthly reconciliation job and appear on the exceptions report the following month.

## BitLocker and recovery keys
Disk encryption is enabled by the profile. Confirm that the recovery key has escrowed to the directory before handover: an unescrowed key means the machine cannot be recovered if the user forgets their PIN, and this is the single most common cause of a rebuild. If the key has not escrowed within 30 minutes of imaging completing, force a device sync and re-check.

## Handover
At handover, confirm with the user: that they can sign in, that MFA is enrolled on their own device, that the VPN connects on the `CORP-JP-PROD` profile, and that they can reach the intranet home page. Record the handover date in the asset record. Do not hand over a machine that has not completed at least one successful Intune check-in, because pending policy will apply later and can force an unexpected restart during the user's first day.

## Common kitting failures
Autopilot stalling at 82% indicates a Wi-Fi enrolment as described above. A device that reaches the desktop but shows no corporate applications has usually enrolled into the wrong profile group; check group membership before rebuilding. A device that repeatedly prompts for BitLocker recovery at boot after imaging normally has stale firmware and should have its firmware updated before the machine is reissued.
