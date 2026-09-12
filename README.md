# Aethel website

English and Japanese product pages, published with GitHub Pages.

## Develop

Run `python3 build.py`, then `python3 -m http.server 8000 --directory public`.
English is at `/`; Japanese is at `/ja/`. No runtime dependencies, tracking,
forms or external assets are loaded.

## Publish

Push the reviewed source to `main`. GitHub Actions builds only `public/` and
deploys that artifact to Pages. The served `version.txt` contains the source
commit. Set the repository variable `SITE_URL` when the custom domain is enabled;
the default is `https://zkfmi.github.io/aethel-site`.

Requested domain: `aethel.fi` (Marcaria). Domain registration, DNS,
Pages domain binding and HTTPS certificate readiness are separate states.
Do not claim the custom domain is live based only on a successful workflow.

## Content ownership

Aethel uses its own brand and bilingual copy. Technical implementation sources
remain in the zkFMI repositories and at https://zkfmi.com/.
Aemeth is the project brand; zkFMI is the technology stack; Aethel is the
payment-stream receivables application. Research status and operational
limitations must remain explicit. No unverified affiliations or financing
offers are published. No contact email is configured at the user's request.

## Review

Check both languages on desktop and a narrow viewport, exercise navigation and
outbound technical links, and compare the served version with the deployed
commit. Build success is a development check, not acceptance evidence.
