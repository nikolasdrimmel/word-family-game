# Word Family Rush — iOS / Home-Screen edition 🌱📱

This is a **separate copy** of the Word Family game, set up to install on an
iPhone as a real Home-Screen app (a "PWA"). **Your original `Word Family Game`
folder is untouched** — edit and play that one exactly as before. This folder
adds three things on top of it:

1. **A built-in on-screen keyboard.** On a phone, the game shows **its own
   keyboard** instead of the iOS one — so there is **no autocorrect, no
   predictive text, and no auto-capitalising** fighting you as you type word
   families. The Spanish keyboard adds an accent row (`á é í ó ú ü ñ`). Your
   physical keyboard still works normally on a computer.
2. **Installable + offline** (`manifest.webmanifest`, `service-worker.js`,
   icons) — once added to the Home Screen it launches fullscreen, with its own
   icon, and works with no internet.
3. Everything else is **identical** to the original game.

## Same editing workflow as before

The word lists and build step are unchanged:

- Edit **`families.txt`** (English) / **`familias.txt`** (Spanish).
- Run `python build.py` to regenerate `index.html`.

The keyboard and offline support live in `index.template.html`, so they survive
every rebuild automatically.

```bash
python build.py
```

## Putting it on your iPhone (one time, ~10 minutes)

An iPhone needs to load the game once from an **https** address before it can go
offline (that's what the service worker requires). Free ways to host it:

1. **Host the folder.** Easiest options, all free:
   - [Netlify Drop](https://app.netlify.com/drop) — drag this whole folder onto
     the page, get an `https://…netlify.app` link. (Nothing to install.)
   - [Cloudflare Pages](https://pages.cloudflare.com) or
     [GitHub Pages](https://pages.github.com) work the same way.
   - Upload **all** files in this folder (`index.html`, `manifest.webmanifest`,
     `service-worker.js`, and the three `.png` icons).
2. **Open the link in Safari** on your iPhone.
3. Tap the **Share** button → **Add to Home Screen** → **Add**.
4. Open it once with internet. After that it runs **offline, fullscreen**, like
   any other app. Delete it any time by long-pressing the icon.

> Note: this is *not* the Apple App Store — no `$99` fee, no Mac, no review.
> If you ever want the App Store version later, this same folder is exactly what
> a tool like Capacitor wraps, so none of this work is wasted.

## Files in this folder

| File | What it is |
|------|------------|
| `index.html` | The game (generated). The file you host / open. |
| `index.template.html` | Game code **+ keyboard + PWA hooks**. Edited by hand. |
| `families.txt` / `familias.txt` | Word-family databases (edit these). |
| `build.py` | Rebuilds `index.html` from the databases + template. |
| `manifest.webmanifest` | Makes it installable (name, icon, colours). |
| `service-worker.js` | Caches the game so it works offline. |
| `icon-192.png`, `icon-512.png`, `apple-touch-icon.png` | App icons. |
