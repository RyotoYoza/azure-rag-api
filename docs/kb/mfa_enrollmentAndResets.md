# MFA Enrolment, Resets, and Lockouts

## Enrolment
All staff must enrol at least two multi-factor methods. The supported methods are the authenticator application on a mobile device and a hardware token from the `TK-2` series. SMS was withdrawn as a method in January 2026 and any account still showing SMS as a registered method should be flagged to `IAM-L2` for cleanup.

Enrolment is completed at the account portal from a corporate network or over VPN. Enrolment attempts from outside the corporate network are blocked by conditional access policy `CA-JP-ENROL-01`, which returns the message "You cannot access this right now" with no further detail. This is expected behaviour and not a fault; the user must be on VPN or on site.

## Reset requests
A reset removes all registered methods and requires the user to enrol again. Resets must be verified in person or over a video call in which the user shows their employee badge. Verification over chat or email alone is not sufficient, because MFA reset is the most common target for social engineering against the service desk. Record in the ticket which verification method was used and the name of the agent who performed it.

Resets are performed from the identity console under the user's account, using the "Require re-registration" action. The change takes effect at the user's next sign-in and can take up to 15 minutes to propagate.

## Lockouts
An account locks after 10 consecutive failed sign-in attempts within 5 minutes. The lock releases automatically after 30 minutes. Manual unlock is available to `IAM-L2` but should not be used routinely, because repeated manual unlocks mask a compromised-credential pattern that the security team monitors. If a user is locked out more than twice in one week, raise a ticket to `SEC-L2` rather than unlocking again.

## Travelling users
Sign-ins from outside Japan trigger the risk-based policy `CA-RISK-02` and prompt for an additional check. Users travelling for business should be advised to register the authenticator application before departure, since enrolling a new method from an overseas network requires an exception approved by their manager and processed by `IAM-L2`. Exceptions are granted for a maximum of 14 days.

## Lost or replaced phone
When a user replaces a phone, they should add the new device as a method before removing the old one. If the old device is already gone, this becomes a reset and follows the verification process above. A common failure is the user restoring a phone backup and expecting the authenticator entries to be restored with it; on most configurations they are not, and the account will still require a reset.

## Error codes
Code `IAM-7701` at sign-in means the method list is empty and the account needs re-enrolment. Code `IAM-7715` means the conditional access policy blocked the attempt because of network location. Code `IAM-7742` means the hardware token has drifted out of time synchronisation and must be re-synchronised from the identity console before it will be accepted.
