// script.js

// Example function to sort table by column
function sortTable(n) {
    const table = document.querySelector('table');
    let rows, switching, i, x, y, shouldSwitch, dir, switchCount = 0;
    let switchable = true;
    dir = "asc";

    while (switchable) {
        switching = false;
        rows = table.rows;

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];

            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }
        }

        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchCount++;
        } else {
            if (switchCount === 0 && dir === "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

// Example function to filter tasks by title
function filterTasks() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase();
    const table = document.querySelector('table');
    const tr = table.getElementsByTagName('tr');

    for (let i = 1; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName('td')[0]; // Assuming the title is in the first column
        if (td) {
            let txtValue = td.textContent || td.innerText;
            tr[i].style.display = txtValue.toLowerCase().indexOf(filter) > -1 ? "" : "none";
        }
    }
}
