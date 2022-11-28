from bs4 import BeautifulSoup
import requests
import functools
import re
import json
import html
import unicodedata

base_url = "https://manager.aftonbladet.se"

teams = {}

def collect_stats(name, url):
    teams[name] = {}
    res = requests.get(base_url + url)

    parsed_html = BeautifulSoup(res.content, "html.parser")
    growth = parsed_html.body.findAll('tr', attrs={'growth': True})

    total_round_tr2 = parsed_html.find("div", id="growth")

    growths = [int(x["growth"]) for x in growth if x != "0"]
    filtered = [x for x in growths if x != 0]

    teams[name]["average"] = int(unicodedata.normalize("NFKD", "".join(total_round_tr2.findAll("h3")[0].text.split()))) / len(filtered)

    turn_summary = parsed_html.find("div", id="turn-summary")
    total_tr = turn_summary.find_next("tr", attrs={"class": "total"})
    teams[name]["total"] = int("".join(unicodedata.normalize("NFKD", total_tr.findAll("td")[1].text).split(" ")[:-1]))

    total_round_tr = turn_summary.findAll("tr", attrs={"class": "total"})[1]
    teams[name]["total_round"] = int("".join(unicodedata.normalize("NFKD", total_round_tr.findAll("td")[1].text).split(" ")[:-1]))

    teams[name]["players_left"] = 11-len(filtered)

def lambda_handler(event, context):
    res_teams = requests.get(
        "https://manager.aftonbladet.se/se/ab-2022-world-fantasy/leaderboards/dalens_basta_gang")
    parsed_teams = BeautifulSoup(res_teams.content, "html.parser")
    strong = parsed_teams.body.findAll('strong', id=re.compile("^team-"))
    refs = []
    for s in strong:
        refs.append(s.findChildren('a', href=re.compile(".*userteams.*"))[0])

    teamlinks = {x.text: x["href"] for x in refs}

    for name, url in teamlinks.items():
        collect_stats(name, url)

    return {
        'statusCode': 200,
        'headers': {
        "Access-Control-Allow-Origin": "*",
        },
        'body': json.dumps(teams)
    }
