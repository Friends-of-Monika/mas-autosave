# 🌥️ Configuring Cloudflare backend

> [!NOTE]
> Every step has screenshots to help you, click on the spoiler to reveal them!

Cloudflare is the easiest (though has its tradeoffs &mdash; please read important info up ahead)
way to store automated backups in Friends of Monika provided online storage. All it takes is
for you to write down a unique key the submod will generate for you and keep it somewhere safe
in case you'll need to restore a backup.

## ⚠️ Important information

We at Friends of Monika will do our best to keep this running smoothly, but the storage runs on
Cloudflare and is subject to their policies, so this feature is provided **as is**, on a
**best-effort** basis. We **can't guarantee** your backups will always be available or never lost.

Please keep this in mind:
- **Don't make this your only backup.** Copy your persistent somewhere else every now and then.
- **Keep your code safe.** We never see it and cannot recover it for you &mdash; if you lose it,
  your cloud backups are gone for good.

If we plan a data migration, breaking changes, or other changes to how this service works, we'll
announce it on our [Discord server](https://mon.icu/discord) ahead of time. We'll also post an
announcement if changes on Cloudflare's side affect the service, though we can't promise an
immediate response in that case. Join the server if you want to stay in the loop!

## 🔐 Security

Two quick facts:

- Neither Friends of Monika nor Cloudflare can ever see your unencrypted persistent
- Friends of Monika don't know your unique code and can't identify you from the data we store

Your persistent is encrypted *on your computer* with AES-256-GCM, using a key derived from your
unique code, before it's ever sent to the cloud. Nobody can read it, and any tampering is detected
when you restore it.

Your cloud saves are linked only to *a hash* of your unique code. The hash can't be reversed to get
your code back, and the code itself is random enough that guessing it is practically impossible.

**This also means that if you lose your unique code, your saves are lost for good.** We can't
recover it for you.

> [!WARNING]
> Your unique code is stored inside your persistent file. **Anyone who has a copy of your persistent
> can access your cloud backups**, so be careful when sharing it (e.g. for bug reports).

## 😔 Limitations

Let's be upfront about a few limitations:

1. **Each backup can be up to 2 MB**. Larger backups will fail to upload.
2. **Up to 20 backups are kept.** Once you reach that, the oldest one is permanently deleted
   with each new backup. With hourly backups, that's roughly your last 20 hours of play.
3. **Backups are kept for up to 30 days.** Anything older is permanently deleted.

We have to impose these limits to keep cloud storage free for everyone.

## 🌐 Web interface

You can browse and download your cloud saves directly in the browser at **[saves.mon.icu](https://saves.mon.icu/)**.

Enter your backup code, pick the save you want, and the file will be downloaded and decrypted
locally in your browser. Your unique code never leaves your device.

## 🤔 FAQ

**Q:** I no longer have access to my computer, but I have cloud saves and I have my unique code
written down. How do I access my saves?<br>
**A:** Use the web interface at **[https://saves.mon.icu/](https://saves.mon.icu/)**.
Enter your backup code, choose the save you want to restore, and it will be downloaded and
decrypted directly in your browser. No game or mod installation needed.

If you run into any issues, contact us:

- At our Discord server: https://mon.icu/discord
- DM the lead developer, @dreamscached, on Reddit: [u/dreamscached](https://reddit.com/u/dreamscached)
- E-mail the lead developer, @dreamscached: [dreamscache.d@gmail.com](mailto:dreamscache.d@gmail.com)
- Submit an issue here on Github
