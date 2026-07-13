import json, os, re, urllib.request

TOKEN = os.environ["TOKEN"]

def gh(url):
    req = urllib.request.Request(
        url, 
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "User-Agent": "banner-stats",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

USER = "Nihalpujari"
u = gh(f"https://api.github.com/users/{USER}")
stats = {"followers": u["followers"], "public_repos": u["public_repos"], "stars": 0, "forks": 0}

def pages(endpoint, field):
    page = 1
    while True:
        rs = gh(f"{endpoint}?per_page=100&page={page}")
        if not rs: break
        for r in rs:
            stats[field] += r["stargazers_count"] if field == "stars" else r["forks_count"]
        if len(rs) < 100: break
        page += 1

pages("https://api.github.com/users/{}/repos".format(USER), "stars")
pages("https://api.github.com/users/{}/repos".format(USER), "forks")

def sub_stats(svg, stats):
    svg = re.sub(r'GitHub followers ([^/]+/Followers)', 'Followers: {}'.format(stats["followers"]), svg)
    svg = re.sub(r'GitHub stars across all repos ([^/]+/Total%20Stars)', 'Total Stars: {}'.format(stats["stars"]), svg)
    svg = re.sub(r'GitHub forks across all repos ([^/]+/Total%20Forks)', 'Total Forks: {}'.format(stats["forks"]), svg)
    svg = re.sub(r'GitHub public repos ([^/]+/Public%20Repos)', 'Public Repos: {}'.format(stats["public_repos"]), svg)
    return svg

dark = open('assets/dark.svg').read()
dark = sub_stats(dark, stats)
open('assets/dark.svg', 'w').write(dark)

repl = [...] # Color mappings (paste the full list from before)
for a, b in repl:
    dark = dark.replace(a, b)
open('assets/light.svg', 'w').write(dark)