# -*- coding: utf-8 -*-
import copy, os
from bs4 import BeautifulSoup
from build_i18n_data import FA, AR, TITLES, META_DESC, OG_LOCALE, JSONLD_JOBTITLE

BASE = "https://javadbavi.com"

with open("index.html", encoding="utf-8") as f:
    base_html = f.read()

def build(lang, translations):
    soup = BeautifulSoup(base_html, "html.parser")

    # html tag lang/dir
    html_tag = soup.find("html")
    html_tag["lang"] = lang
    html_tag["dir"] = "rtl"
    soup.find("body")["class"] = (soup.find("body").get("class") or []) + ["rtl"]

    # translate all data-key text nodes
    for el in soup.find_all(attrs={"data-key": True}):
        key = el.get("data-key")
        if key in translations:
            el.string = translations[key]

    # title
    soup.find("title").string = TITLES[lang]

    # meta description / og / twitter
    desc = META_DESC[lang]
    soup.find("meta", attrs={"name": "description"})["content"] = desc
    soup.find("meta", attrs={"property": "og:description"})["content"] = desc
    soup.find("meta", attrs={"name": "twitter:description"})["content"] = desc
    soup.find("meta", attrs={"property": "og:title"})["content"] = TITLES[lang]
    soup.find("meta", attrs={"name": "twitter:title"})["content"] = TITLES[lang]
    soup.find("meta", attrs={"property": "og:locale"})["content"] = OG_LOCALE[lang]

    # canonical + hreflang alternates (self + siblings, already same absolute set)
    soup.find("link", attrs={"rel": "canonical"})["href"] = f"{BASE}/{lang}/"

    # og:url is not present originally; add for completeness
    head = soup.find("head")

    # fix relative asset paths -> prefix with ../
    for tag, attr in [("link", "href"), ("script", "src"), ("img", "src")]:
        for el in soup.find_all(tag):
            val = el.get(attr)
            if val and not val.startswith(("http://", "https://", "/", "#")):
                el[attr] = "../" + val

    # nav lang-switch: mark active + fix hrefs already absolute (/, /fa/, /ar/) - just set active class
    for a in soup.select(".lang-switch a"):
        href = a.get("href")
        is_active = (href == f"/{lang}/")
        classes = [c for c in (a.get("class") or []) if c != "active"]
        if is_active:
            classes.append("active")
            a["aria-current"] = "page"
        else:
            if a.has_attr("aria-current"):
                del a["aria-current"]
        if classes:
            a["class"] = classes
        elif a.has_attr("class"):
            del a["class"]

    # JSON-LD: translate description + jobTitle + image/contentUrl already absolute
    ld = soup.find("script", id="structured-data")
    if ld:
        import json
        data = json.loads(ld.string)
        for node in data.get("@graph", []):
            if node.get("@type") == "ProfilePage":
                node["description"] = desc
            if node.get("@type") == "Person":
                node["description"] = desc
                node["jobTitle"] = JSONLD_JOBTITLE[lang]
        ld.string = json.dumps(data, ensure_ascii=False)

    # Add Vazirmatn webfont for proper Persian/Arabic typography (keeps the same visual theme)
    preconnect1 = soup.new_tag("link", rel="preconnect", href="https://fonts.googleapis.com")
    preconnect2 = soup.new_tag("link")
    preconnect2["rel"] = "preconnect"
    preconnect2["href"] = "https://fonts.gstatic.com"
    preconnect2["crossorigin"] = ""
    fontlink = soup.new_tag("link", rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&display=swap")
    css_link = soup.find("link", attrs={"href": lambda v: v and v.endswith("style.css")})
    css_link.insert_before(preconnect1)
    css_link.insert_before(preconnect2)
    css_link.insert_before(fontlink)

    outdir = lang
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"wrote {outdir}/index.html")

build("fa", FA)
build("ar", AR)
