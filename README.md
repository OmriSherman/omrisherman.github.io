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
| `llms.txt` | First-party factual summary for AI answer engines, so they cite correct facts |
| `og-image.png` | 1200×630 social share card |
| `favicon.ico`, `icon-192.png`, `icon-512.png`, `apple-touch-icon.png` | Site icons |

## Keeping facts straight

`index.html`, `support.html` and `llms.txt` all state the same facts about the game
(quiz modes, unlock rules, ads, leaderboard, Conqueror Pass). **When gameplay changes,
update all three** — search engines and AI assistants read them as one source, and a
contradiction between pages gets surfaced to users.

`app-ads.txt` is required by AdMob and must stay at the domain root.
