This folder is NOT part of the deployed website — do not upload it to Cloudflare Pages.

It's the source used to generate the Persian (/fa/) and Arabic (/ar/) static pages
from the English index.html template, so translations can be edited and regenerated
later without touching HTML by hand.

To regenerate after editing translations in build_i18n_data.py:
  1. Make sure index.html (English, at the project root) is up to date first —
     it is the template all languages are generated from.
  2. Run: python3 i18n-tools/build_i18n.py   (from the project root)
  3. This overwrites fa/index.html and ar/index.html.

Requires Python 3 with beautifulsoup4 installed (pip install beautifulsoup4).
