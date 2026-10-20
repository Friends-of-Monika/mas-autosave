# Privacy Policy — Autosave Cloud

**Effective date:** 2026-10-20

This policy explains what data the Autosave Cloud service collects, why, and what rights you
have. It applies to the cloud backup feature of the Autosave submod for Monika After Story and
to the Autosave Cloud web page at `https://saves.mon.icu` (also reachable at
`https://autosave.worker.mon.icu`, which the submod uses to connect).
It does not apply to the GitHub backup feature, which stores data in your own GitHub repository
under GitHub's terms.

## Summary

- Your save data is encrypted on your device before it is uploaded. We cannot read it.
- We do not have accounts, and we do not store names, email addresses or IP addresses.
- Your backups are linked only to a pseudonymous ID derived from your secret code.
- Backups are deleted automatically 30 days after upload.
- You can delete all your data at any time on the Autosave Cloud web page.

## Who is responsible

This service is operated by Friends of Monika. Official contact for all privacy matters,
including exercising your rights under this policy: **privacy@mon.icu**.

Friends of Monika is committed to upholding this privacy policy. The identity of the
responsible natural person will be disclosed to competent supervisory authorities, and to data
subjects upon request where legally required.

## How the service works

When you enable cloud backups, the submod generates a random **secret code** (a UUID) or lets
you enter one from another device. From this code, two values are derived on your device:

- an **encryption key**, used to encrypt your save data (AES-256-GCM);
- a **user ID**, a one-way hash (SHA-512) of the code, used to store and find your backups.

Only the encrypted data and the user ID are sent to our servers. **The secret code and the
encryption key never leave your device.** The user ID cannot be turned back into the secret
code, and it cannot be used to decrypt your backups.

The same applies to the web page: when you enter your secret code there, the user ID and key
are derived in your browser, and the code is not sent to our servers.

## What data we store

For each backup, we store:

| Data                                                                                       | Purpose |
|--------------------------------------------------------------------------------------------|-----------------------------------------------|
| Encrypted save data (your `persistent` file)                                               | To let you restore it later                   |
| User ID (pseudonymous hash of your secret code)                                            | To find your backups                          |
| Upload time                                                                                | To show backup history and delete old backups |
| File size and a content hash of the encrypted file                                         | To show backup history and avoid duplicates   |
| Backup reason (a short label such as "Goodbye" or "Daily auto-backup", sent by the submod) | To show backup history                        |

We cannot read the contents of your save data. Because the user ID links your backups
together, this data is **pseudonymous**, not anonymous, and we treat it as personal data.

We do not store your IP address, name, email address, or any other information about you.

## Data processed by our provider

The service runs on **Cloudflare** (Cloudflare Workers and Cloudflare R2 storage). Like any
internet service, Cloudflare receives technical request data, including your IP address and
request headers, to deliver traffic and protect against abuse. Cloudflare processes this data
on our behalf as a processor. See
[Cloudflare's Privacy Policy](https://www.cloudflare.com/privacypolicy/).

We do not keep request logs. For troubleshooting, we may temporarily view live request logs;
these are not stored.

Backups are stored in Cloudflare's Eastern Europe storage region. Cloudflare may process data outside
your country, including in the United States. Cloudflare is certified under the EU–U.S. Data Privacy
Framework and uses the European Commission's Standard Contractual Clauses for these transfers.

## Cookies and tracking

The Autosave Cloud web page does not use cookies, analytics, or third-party trackers, and
does not load content from third-party sites.

## Legal basis

We process your data to provide the backup service you asked for (Art. 6(1)(b) GDPR). The
technical request data processed by Cloudflare is also processed for our legitimate interest
in keeping the service secure and available (Art. 6(1)(f) GDPR).

## How long we keep data

- Each backup is deleted automatically **30 days after it was uploaded**.
- We keep at most **20 backups** per user ID. When you upload more, the oldest are deleted.
- The backup list is updated on every upload and is deleted 30 days after your last upload.
- If you contact us by email, we keep your email only as long as needed to handle your request.

## Your rights

Depending on where you live, you may have the right to access, export, correct, restrict or
delete your data, and to object to its processing.

- **Access and export:** enter your secret code on the Autosave Cloud web page to see all your
  backups and download them.
- **Deletion:** on the same page, use **"Delete all my data"**. This immediately and
  permanently deletes all your backups and your backup list.
- **Correction:** your save data is encrypted and we cannot change it. You can upload a new
  backup from the submod at any time.
- **Other requests:** email us at **privacy@mon.icu**.
  Include your **user ID**, not your secret code. Never send us your secret code. To get your
  user ID, enter your secret code on the Autosave Cloud web page and click **"Copy user ID"**.

**If you lose your secret code**, we cannot work out which backups are yours, so we cannot
find, return or delete them for you (Art. 11 GDPR), unless you can give us your user ID. Your
backups will still be deleted automatically within 30 days.

You also have the right to lodge a complaint with a data protection authority, in particular
in the country where you live or work.

## Security

Your save data is encrypted on your device with AES-256-GCM, using a key derived from your
secret code. The server only ever holds encrypted data.

**Keep your secret code safe.** Anyone who has it can read and delete your cloud backups. The
code is stored in your local Monika After Story save data, so anyone with a copy of your
`persistent` file can also access your cloud backups. Do not share your `persistent` file if
you use cloud backups.

## Children

The service is not intended for children under 13. If you are under the age required by the
law of your country to agree to data processing yourself (13 to 16 in the EU), ask a parent
or guardian before using the cloud backup feature.

## Changes to this policy

We may update this policy. Changes are published in the
[mas-autosave repository](https://github.com/friends-of-monika/mas-autosave), with the
effective date at the top updated. Significant changes will also be announced in the
repository's release notes.

## Contact

E-mail: **privacy@mon.icu**
