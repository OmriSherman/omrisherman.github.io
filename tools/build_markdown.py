#!/usr/bin/env python3
"""Generate Markdown alternatives of the site's pages (AI-friendly, Tier-1 content).

Run from the repo root after editing any HTML page:

    python3 tools/build_markdown.py

Writes index.md, support.md and llms-full.txt, and prints an estimated token
count for each (characters / 4 — a rough guide, not a real tokenizer count).
The HTML pages stay the single source of truth; never hand-edit the .md files.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://omrisherman.github.io"
SKIP = {"script", "style", "nav", "footer", "header", "svg", "img"}


class ToMarkdown(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.out, self.skip, self.link = [], 0, None
        self.in_summary = False
        self.in_dt = False
        self.in_dd = False

    def _w(self, s):
        self.out.append(s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in SKIP and tag != "img":
            # the page <header> on legal pages holds the title; keep h1 via body scan
            if not (tag == "header" and a.get("class") is None and False):
                self.skip += 1
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3"):
            self._w("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "p":
            self._w("\n\n")
        elif tag == "li":
            self._w("\n- ")
        elif tag == "summary":
            self.in_summary = True
            self._w("\n\n### ")
        elif tag == "dt":
            self.in_dt = True
            self._w("\n- **")
        elif tag == "dd":
            self.in_dd = True
        elif tag in ("strong", "b"):
            self._w("**")
        elif tag in ("em", "i"):
            self._w("*")
        elif tag == "a" and a.get("href"):
            href = a["href"]
            if href.startswith("/"):
                href = self.base + href
            elif not re.match(r"^(https?:|mailto:|#)", href):
                href = self.base + "/" + href
            self.link = href
            self._w("[")
        elif tag == "br":
            self._w("\n")

    def handle_endtag(self, tag):
        if tag in SKIP and tag != "img":
            if self.skip:
                self.skip -= 1
            return
        if self.skip:
            return
        if tag in ("div", "article", "section", "dl", "details"):
            self._w("\n\n")
        elif tag in ("strong", "b"):
            self._w("**")
        elif tag in ("em", "i"):
            self._w("*")
        elif tag == "a" and self.link:
            self._w("](%s)" % self.link)
            self.link = None
        elif tag == "summary":
            self.in_summary = False
            self._w("\n")
        elif tag == "dt":
            self.in_dt = False
            self._w(":** ")
        elif tag == "dd":
            self.in_dd = False

    def handle_data(self, data):
        if self.skip:
            return
        text = re.sub(r"\s+", " ", data)
        if text.strip() or (self.out and not self.out[-1].endswith(("\n", " "))):
            self._w(text)


def convert(html_path, title_fallback=None):
    html = html_path.read_text(encoding="utf-8")
    body = re.search(r"<body[^>]*>(.*)</body>", html, re.S).group(1)
    # use <main> when present (landing page); legal/support pages use .container
    m = re.search(r"<main[^>]*>(.*)</main>", body, re.S)
    scope = m.group(1) if m else body
    # decorative eyebrow labels ("Why Geo Conquest", "Eight ways to play") add noise
    scope = re.sub(r'<div class="(?:section-kicker|eyebrow)">.*?</div>', "", scope, flags=re.S)
    p = ToMarkdown(SITE)
    p.feed(scope)
    md = "".join(p.out)
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"\n\n(- \*\*)", r"\n\1", md).strip()
    return md


def est_tokens(s):
    return round(len(s) / 4)


def main():
    idx = convert(ROOT / "index.html")
    sup = convert(ROOT / "support.html")
    # support.html's title lives in a <header> that the converter skips
    sup = "## Support & FAQ\n\n" + re.sub(r"^#+ .*\n", "", sup, count=0)

    index_md = ("# Geo Conquest — geography quiz and world map game\n\n"
                "> Free geography quiz game for iOS and Android by BigBrain Global. "
                "Answer questions on flags, capitals, country shapes and borders, earn gold and XP, "
                "and claim real countries on an interactive world map.\n\n"
                "Canonical page: " + SITE + "/\n\n" + idx + "\n")
    support_md = ("# Geo Conquest Support & FAQ\n\n"
                  "Canonical page: " + SITE + "/support.html\n\n" +
                  re.sub(r"^## Support & FAQ\n\n", "", sup) + "\n")
    full = (index_md + "\n---\n\n" + support_md +
            "\n---\n\n## Policies\n\n"
            "- Privacy policy: " + SITE + "/privacy.html\n"
            "- Terms of service: " + SITE + "/tos.html\n")

    for name, text in (("index.md", index_md), ("support.md", support_md), ("llms-full.txt", full)):
        (ROOT / name).write_text(text, encoding="utf-8")
        print(f"{name:15s} {len(text):6d} chars  ~{est_tokens(text):5d} tokens")


if __name__ == "__main__":
    sys.exit(main())
