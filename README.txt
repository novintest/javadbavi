JAVAD BAVI — CLOUDFLARE-READY STATIC SITE (multilingual: EN / FA / AR)

Upload the entire contents of this package as the deployment root
(except the "i18n-tools" folder — see below).

Structure:
index.html              English (default / root)
fa/index.html            Persian — fully pre-rendered, RTL, own URL
ar/index.html            Arabic — fully pre-rendered, RTL, own URL
assets/css/style.css
assets/js/script.js
assets/images/*
assets/fonts/
favicon.svg
robots.txt
sitemap.xml              includes all 3 URLs with hreflang alternates
site.webmanifest
i18n-tools/               NOT deployed — source used to regenerate fa/ar
                           pages if you edit translations later. See its
                           own README.txt.

Each language is a real, separately-crawlable page (not just a JS text
swap), with correct <html lang>/<dir>, translated <title>/meta
description/Open Graph tags, translated structured data (JSON-LD), and
hreflang alternate links pointing to the other two languages — this is
what lets Google index and rank the Persian and Arabic content on their
own, and show the right language in search results for the right
audience.

SEO note: replace "javadbavi.com" across index.html, fa/index.html,
ar/index.html, robots.txt and sitemap.xml with your final domain before
production, if it differs.
