from bs4 import BeautifulSoup
import requests
import functools
import re

base_url = "https://manager.aftonbladet.se"


def avg_for_team(name, url):
    res = requests.get(base_url + url)

    parsed_html = BeautifulSoup(res.content, "html.parser")
    growth = parsed_html.body.findAll('tr', attrs={'growth': True})
    #print("\n".join([x["fs-player-name"] + " " + x["growth"] for x in growth]))

    growths = [int(x["growth"]) for x in growth if x != "0"]
    filtered = [x for x in growths if x != 0]

    average = functools.reduce(lambda a, b: a+b, filtered) / len(filtered)

    turn_summary = parsed_html.find("div", id="turn-summary")
    total_tr = turn_summary.find_next("tr", attrs={"class": "total"})
    total_val = total_tr.findAll("td")[1].text

    total_round_tr = turn_summary.findAll("tr", attrs={"class": "total"})[1]
    total_round_val = total_round_tr.findAll("td")[1].text

    print(name + " average: " + str(round(average)) +
          ", " + "total: " + str(total_val) + ", round: " + total_round_val)


res_teams = requests.get(
    "https://manager.aftonbladet.se/se/ab-2022-world-fantasy/leaderboards/dalens_basta_gang")
parsed_teams = BeautifulSoup(res_teams.content, "html.parser")
strong = parsed_teams.body.findAll('strong', id=re.compile("^team-"))
refs = []
for s in strong:
    refs.append(s.findChildren('a', href=re.compile(".*userteams.*"))[0])

teamlinks = {x.text: x["href"] for x in refs}

for name, url in teamlinks.items():
    if name == "Stackars Giraffer":
        avg_for_team(name, url)
