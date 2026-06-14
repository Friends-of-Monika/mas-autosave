# 🌥️ Configuring Cloudflare backend

> [!NOTE]
> Every step has screenshots to help you, click on the spoiler to reveal them!

Cloudflare is the easiest (not without its tradeoffs &mdash; please read important info up ahead)
way to store automated backups in Friends of Monika provided online storage. All it takes is
for you to write down a unique key the submod will generate for you and keep it somewhere safe
in case you'll need to restore a backup.

That's pretty much it, actually. On this page you'll see important info and FAQs rather than a guide,
it's that easy.

## ⚠️ Important information

**Don't care about legalese?** Here's a *tl;dr &mdash; Cloudflare backend is experimental, stuff
may go wrong and we may lose all stored data, including your persistent. We'll let you know if
something like this happens at [our Discord server](https://mon.icu/discord) so keep an eye out on it.*

Please note that as of v0.1.0 the Cloudflare backend is *experimental* and can be subject to change.
**That means changes to how it works server-side may render your previous saves unavailable.**

We at Friends of Monika will do our absolute best not to break anything, but, since the storage is
provided and managed by Cloudflare and we're subject to their policies and rules, we provide this feature
AS IS and cannot guarantee complete data integrity or availability.

In case we will be planning data migration, breaking changes, or any other possible changes in how we
provide this service we will notify our users via [our Discord server](https://mon.icu/discord). We
will also send an announcement if there were any breaking changes from Cloudflare, though we cannot
guarantee immediate response to such changes.

## 🔐 Security

Two quick facts:

- Neither Friends of Monika nor Cloudflare ever gain access to your unencrypted persistent
- Friends of Monika do not know your unique code and cannot identify you using the data we store

Your cloud saves are linked to *a hash* of unique code the submod generates for you; there is no
way to reverse this hash and get a hold of your code, it's statistically absolutely improbable to
guess or find it with brute-force.

Before leaving your computer and being sent to the cloud, your persistent is *locally* encrypted
with AES-256 encryption algorithm using the key derived from unique code &mdash; nobody can look
into your data.

**This also means if you lose your unique code, your saves are permanently lost.** We will not
attempt to find your lost unique code, we are simply unable to.

## 😔 Limitations

Now let's be clear about some of the limitations:

1. Your persistent (after encryption) *must* be less than 2MB in size.
2. You can only store at most 20 persistents in the cloud, once this number is reached your
   oldest saved persistents will be permanently discarded.
3. Your saved persistents are kept for 30 days and will be permanently discarded once this time
   expires.

Unfortunately, we must impose these limitations to provide the cloud storage for many people
for free.

## 🌐 Web interface

You can browse and download your cloud saves directly in the browser at **[autosave.worker.mon.icu](https://autosave.worker.mon.icu/)**.

Enter your backup code, pick the save you want, and the file will be downloaded and decrypted
locally in your browser. Your unique code never leaves your device.

## 🤔 FAQ

**Q:** I no longer have access to my computer, but I have cloud saves and I have my unique code
written down. How do I access my saves?<br>
**A:** Use the web interface at **[https://autosave.worker.mon.icu/](https://autosave.worker.mon.icu/)**.
Enter your backup code, choose the save you want to restore, and it will be downloaded and
decrypted directly in your browser. No game or mod installation needed.

If you run into any issues, contact us:

- At our Discord server: https://mon.icu/discord
- DM the lead developer, @dreamscached, on Reddit: [u/dreamscached](https://reddit.com/u/dreamscached)
- E-mail the lead developer, @dreamscached: [dreamscache.d@gmail.com](mailto:dreamscache.d@gmail.com)
- Submit an issue here on Github
