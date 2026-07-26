# File Sync: Errors, Conflicts, and Recovery

## Supported sync scope
Only the Desktop, Documents, and Pictures folders are redirected and synced by policy `FS-JP-REDIR-01`. Files saved anywhere else on the local disk, including the root of `C:` and any secondary partition, are **not** backed up and are lost if the machine is rebuilt. This is the most common cause of data loss reported to the service desk after a hardware swap, and it should be stated explicitly during handover.

## Sync paused
The client pauses sync automatically when the device is on a metered connection or when battery is below 20%. A user reporting that "nothing has synced since this morning" is most often tethering to a mobile hotspot that the client has classified as metered. Resuming manually from the client menu overrides this for the current session only.

## Storage quota
The per-user quota is 1 TB. At 90% the client begins showing a persistent warning; at 100% sync stops entirely and new files remain local only. Quota increases require manager approval and are processed by `EUC-L2`. Before requesting an increase, check whether the user is syncing a local copy of a shared library, which is the usual reason an individual account approaches the quota.

## File name and path restrictions
Files fail to sync silently when the full path exceeds 400 characters, or when the name contains any of the characters that the platform reserves. Deeply nested project folders copied from a legacy file server are the usual source. The fix is to shorten the parent folder names rather than the file names, since shortening the file name alone rarely brings the path under the limit.

Files larger than 250 GB are rejected outright and produce error `SYN-3390`.

## Conflict copies
When the same file is edited on two devices while one is offline, the client keeps both versions and appends the device name to the second one. Conflict copies are not deleted automatically and accumulate. Users should be shown how to compare and remove them rather than having the service desk do it, because deciding which version to keep is a judgement the file owner has to make.

## Recovering deleted files
Deleted files remain in the recycle bin for 93 days and can be restored by the user without a ticket. After 93 days, restoration requires a request to `EUC-L2` and is only possible within the backup retention window of 180 days. Requests to restore beyond 180 days cannot be fulfilled, and this should be communicated clearly rather than escalated further.

Version history retains the last 500 versions of a file. Restoring a previous version does not delete the current one; it adds the restored content as a new version, so the action is reversible.

## Error codes
`SYN-3301` indicates the credential cache is stale and the user must sign out of the client and back in. `SYN-3312` indicates a locked file held open by another application, usually a spreadsheet left open on a second device. `SYN-3390` indicates the file exceeds the size limit as above. `SYN-3404` indicates the sync client version is below the supported minimum and must be updated through Company Portal.
