'use strict'



async function main() {
    const loading = document.createElement("div");
    loading.innerHTML = "Laddar...";
    loading.id = "loading";
    document.body.appendChild(loading)
    const fetchResponse = await fetch("https://5coh2fljzk.execute-api.eu-west-1.amazonaws.com/stats");
    //document.getElementById("loading");
    loading.remove();
    const teams = await fetchResponse.json();
    const tbody = document.getElementById("body")

    Object.entries(teams).sort((a,b) => a[1]["average"] - b[1]["average"]).reverse().forEach(entry => {
        const [name, stats] = entry;
        const row = tbody.insertRow();
        const nameCell = row.insertCell(0);
        nameCell.innerHTML = name;

        const avgCell = row.insertCell(1);
        avgCell.innerHTML = Math.round(Number.parseFloat(stats.average)).toLocaleString("sv-SE");
        avgCell.classList.add("align-right");

        const totalCell = row.insertCell(2);
        totalCell.innerHTML = Math.round(Number.parseFloat(stats.total_round)).toLocaleString("sv-SE");
        totalCell.classList.add("align-right");
    });
}






main();