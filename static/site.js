/* Adam Richmond - submission to Save the Children Skills Assessment */
/* December 2022 */

function getData() {
    fetch('/get_data')
    .then(response => response.json())
    .then(data => {
        displayData(data);
    })
}

function displayData(data) {
    var update = setInterval(function() {
        const stat_groups = ["survive", "child_poverty", "learn", "protect"];
        for (var i = 0; i < stat_groups.length; i++) {
             var stat_group = stat_groups[i];
             var stat_group_div = document.getElementById(stat_group);
             var counters = [];
             for (const [index, stat] of Object.entries(data)) {
                if (stat.group == stat_group) {
                    counter = createCounter(stat);
                    counters.push(counter);
                }
             }
             stat_group_div.innerHTML = counters.join("");
        }
    }, 1000);
}

function getFractionOfStat(stat) {
    var today = new Date;
    var start = new Date(today.getFullYear(), 0, 0);
    var dayOfYear = (today - start) / (1000 * 60 * 60 * 24);
    fraction = Math.floor((dayOfYear/365) * stat);
    return fraction;
}

function createCounter(stat) {
    converted_value = getFractionOfStat(stat.value)
    counter = `
        <div class="card" style="width: 18rem;">
          <div class="card-body">
            <h5 class="card-title">${converted_value.toLocaleString()}</h5>
            <p class="card-text">${stat.info}</p>
          </div>
        </div>
    `;
    return counter;
}
