# Geo Conquest — omrisherman.github.io

Marketing and policy site for **Geo Conquest**, a geography quiz and map-conquest
game for iOS and Android by BigBrain Global.

Served by GitHub Pages at <https://omrisherman.github.io/>.

## Pages

| File | URL | Purpose |
| --- | --- | --- |
| `index.html` | `/` | Landing page: pitch, quiz modes, core loop, fast facts, FAQ, store links |
| `support.html` | `/support.html` | Support & FAQ — gameplay, economy, accounts, troubleshooting |
| `privacy.html` | `/privacy.html` | Privacy policy (linked from both app store listings) |
| `tos.html` | `/tos.html` | Terms of service |
| `404.html` | any unknown path | Branded not-found page |

## SEO / GEO files

| File | Purpose |
| --- | --- |
| `robots.txt` | Allows search and AI crawlers; disallows `/admin-dashboards/`; points to the sitemap |
| `sitemap.xml` | The four indexable URLs — update `lastmod` when a page changes |
| `llms.txt` | First-party factual summary and index for AI answer engines, so they cite correct facts |
| `llms-full.txt`, `index.md`, `support.md` | Clean Markdown versions of the key pages — **generated**, do not hand-edit |
| `tools/build_markdown.py` | Regenerates the three files above from the HTML and prints token estimates |
| `og-image.png` | 1200×630 social share card, in the app palette (`#0a0a1a` / `#1a1a2e` / `#ffd700`) |
| `img/` | Pixel-art icons copied from the app's `assets/avatars/` — re-copy if the art changes |
| `favicon.ico`, `icon-192.png`, `icon-512.png`, `apple-touch-icon.png` | Site icons |

## Keeping facts straight

`index.html`, `support.html` and `llms.txt` all state the same facts about the game
(quiz modes, unlock rules, ads, leaderboard, Conqueror Pass). **When gameplay changes,
update all three** — search engines and AI assistants read them as one source, and a
contradiction between pages gets surfaced to users.

`app-ads.txt` is required by AdMob and must stay at the domain root.

## After editing any page

```
python3 tools/build_markdown.py     # refresh index.md, support.md, llms-full.txt
```

Then update the facts in `llms.txt` by hand, bump `Last updated:` in it and in `robots.txt`,
and update `lastmod` in `sitemap.xml`. Re-check `llms.txt` at least quarterly.

## Agent / WebMCP note

`index.html` registers two **read-only** WebMCP tools (`get_geo_conquest_download_links`,
`get_geo_conquest_facts`) when a browser exposes `navigator.modelContext` / `document.modelContext`.
WebMCP is a draft spec; the script feature-detects and does nothing otherwise. The site has no
forms, sign-in or checkout, so there is nothing consequential for an agent to submit.
