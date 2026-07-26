# Offboarding: Account Closure and Asset Return

## Trigger and timing
Offboarding starts from the leaver record raised by HR, which arrives in queue `EUC-L1` seven calendar days before the last working day. Tickets raised by a manager without a corresponding HR record cannot be actioned, because account closure requires the HR record as the authoritative source. Managers asking to close an account early should be directed to HR.

## Account actions on the last working day
On the last working day, at the end of business, the account is disabled rather than deleted. Disabling preserves the mailbox and files for the retention period; deletion destroys them immediately and is not reversible. Accounts are deleted automatically 90 days after being disabled.

Registered MFA methods are removed at the same time. Group memberships are retained during the 90-day window so that access can be reconstructed if the leaver returns or if an audit query arises.

## Mailbox and file access for the manager
The leaver's manager may request delegated access to the mailbox and the leaver's redirected folders for up to 90 days. The request must name a business reason and is approved by the manager's own manager, not by the service desk. Access is granted read-only. Requests to forward the leaver's incoming mail to another mailbox are handled differently: forwarding is set for a maximum of 30 days and an automatic reply is enabled for the same period.

## Asset return
All assets issued to the leaver must be returned before the last working day: laptop, dock, headset, hardware token, and any loaner equipment. Each returned item is checked against the asset record and marked returned with the date and the receiving agent's ID. Items not returned are recorded as outstanding and reported to the manager and to Finance in the monthly exceptions report.

Returned laptops are wiped and re-imaged before reissue. A returned laptop must not be reissued without a wipe, regardless of how briefly it was held, because the disk still contains the previous user's cached credentials and locally stored files.

## Data on the local disk
Remind the leaver during the return process that anything saved outside the redirected Desktop, Documents, and Pictures folders is not backed up and will be destroyed by the wipe. Leavers frequently keep work in a local project folder on a second partition. If the leaver identifies such data as business-critical, copy it to a location nominated by the manager before wiping, and record that transfer in the ticket.

## Contractors and fixed-term staff
Contractor accounts carry an expiry date set at creation and disable automatically on that date without an HR leaver record. Extension requires the sponsoring manager to submit a renewal at least five working days before expiry. An expired contractor account that needs to be reinstated within the 90-day window can be re-enabled; after 90 days a new account must be created and the previous access reconstructed manually.

## Escalation
Escalate to `IAM-L2` if the account cannot be disabled because of an active session lock, and to `EUC-L2` if an asset is returned damaged and needs to be written off. Write-offs require the asset tag, a photograph of the damage, and the cost centre.
