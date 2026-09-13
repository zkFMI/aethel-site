# Aethel website

English and Japanese product pages for Aethel, the payment-stream receivables
application that settles on zkFMI or on an attested rail, published with GitHub Pages.

## Develop

```sh
python3 build.py
python3 -m http.server 8000 --directory public
```

English is at `/`, Japanese at `/ja/`. Fonts (Bricolage Grotesque, Inter,
JetBrains Mono) are self-hosted under `static/fonts/`; nothing is fetched from
a third party at runtime, there is no script, no tracking and no form.

## Layout

- `build.py` — bilingual copy and the page template, including the inline SVG
  hero diagram (signed stream → receivable → settlement). On narrow screens the
  diagram is replaced by a text list.
- `static/style.css` — the one stylesheet. Cool paper, ink; ultramarine for
  decisions, amber for cover, teal for what settled.
- `static/og.png` — social card, rendered from `brand/og.html` at 1200×630.
- `public/` — build output, not committed.

## Publish

Push the reviewed source to `main`. GitHub Actions builds `public/` and deploys
it to Pages. The served `version.txt` contains the source commit. The default
`SITE_URL` is `https://aethel.fi`; DNS, the Pages certificate and HTTPS
enforcement are in place. Links to æmeth point at `https://aemeth.fi/`.

## Content ownership

Product statements follow `zkFMI/aethel` (README, the enterprise PoC guide and
the "current limits" list on zkfmi.com). Aethel records the meaning and
lifecycle of a receivable; cash, securities, title, identity records and
guarantee ledgers stay at the settlement rail and qualification port the
deployment chooses (DeFMI, DeKYX and DeCCP on zkFMI; operator- and
issuer-signed records on the attested rail), and the site says so. Rail
statements follow `docs/RAIL_INDEPENDENCE_JA.md` in `zkFMI/aethel`.
Research status and limitations must remain explicit. No unverified
affiliations or financing offers are published. No contact email is configured
at the user's request.

## Review

Check both languages on desktop and a narrow viewport, exercise navigation and
outbound links (PoC guide, source, zkfmi.com), and compare the served
`version.txt` with the deployed commit. Build success is a development check,
not acceptance evidence.
