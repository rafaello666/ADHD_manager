/***************************************
 script.js – front-end logika
***************************************/

const USE_SERVER_TIME_SYNC = true;
let serverTimestamp = 0;
let activeIntervals = {};

document.addEventListener("DOMContentLoaded", () => {
  const serverNowElem = document.getElementById("serverNowValue");
  if (serverNowElem) {
    serverTimestamp = parseFloat(serverNowElem.value) || 0;
  }

  // Inicjalizacja sortowania
  const headers = document.querySelectorAll("#taskTable thead th[data-sort]");
  headers.forEach(h => {
    h.addEventListener("click", () => {
      const sortKey = h.dataset.sort;
      if(currentSortKey === sortKey) {
        sortAsc = !sortAsc;
      } else {
        currentSortKey = sortKey;
        sortAsc = true;
      }
      sortTable(sortKey, sortAsc);
    });
  });

  // Timery
  initGlobalTimers();

  // Initialize Priority Chart
  const priorityCanvas = document.getElementById('priorityChart');
  if (priorityCanvas) {
      const priorityCtx = priorityCanvas.getContext('2d');
      const priorityChart = new Chart(priorityCtx, {
          type: 'pie',
          data: {
              labels: ['Wysoki', 'Średni', 'Niski'],
              datasets: [{
                  data: [priorityData.wysoki, priorityData.sredni, priorityData.niski],
                  backgroundColor: [
                      'rgba(255, 99, 132, 0.6)', // Wysoki
                      'rgba(255, 206, 86, 0.6)',  // Średni
                      'rgba(75, 192, 192, 0.6)'   // Niski
                  ],
                  borderColor: [
                      'rgba(255, 99, 132, 1)',
                      'rgba(255, 206, 86, 1)',
                      'rgba(75, 192, 192, 1)'
                  ],
                  borderWidth: 1
              }]
          },
          options: {
              responsive: true,
              plugins: {
                  legend: {
                      position: 'top',
                  },
                  title: {
                      display: true,
                      text: 'Rozkład Zadań wg. Priorytetu'
                  }
              }
          }
      });
  }

  // Initialize HR/HRV Chart
  const hrvCanvas = document.getElementById('hrvChart');
  if (hrvCanvas) {
      const hrvCtx = hrvCanvas.getContext('2d');
      const hrvChart = new Chart(hrvCtx, {
          type: 'line',
          data: {
              labels: ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00'],
              datasets: [
                {
                  label: 'HR (bpm)',
                  data: [82, 83, 85, 87, 86, 88],
                  borderColor: 'rgba(220,53,69,1)',
                  backgroundColor: 'rgba(220,53,69,0.1)',
                  fill: true,
                  tension: 0.3,
                  yAxisID: 'y1'
                },
                {
                  label: 'HRV (ms)',
                  data: [35, 36, 34, 33, 37, 38],
                  borderColor: 'rgba(32,201,151,1)',
                  backgroundColor: 'rgba(32,201,151,0.1)',
                  fill: true,
                  tension: 0.3,
                  yAxisID: 'y2'
                }
              ]
          },
          options: {
              responsive: true,
              scales: {
                  y1: {
                      type: 'linear',
                      position: 'left',
                      title: {
                          display: true,
                          text: 'HR (bpm)'
                      }
                  },
                  y2: {
                      type: 'linear',
                      position: 'right',
                      title: {
                          display: true,
                          text: 'HRV (ms)'
                      },
                      grid: {
                          drawOnChartArea: false
                      }
                  }
              },
              plugins: {
                  legend: {
                      position: 'bottom'
                  }
              }
          }
      });
  }
});

/***************************************
  Apply Filter Function
***************************************/
function applyFilter() {
  const q = document.getElementById("searchInput").value.trim().toLowerCase();
  const rows = document.querySelectorAll("#taskTable tbody tr");
  rows.forEach(row => {
    const title = row.children[1].innerText.toLowerCase();
    const matches = title.includes(q);
    row.style.display = matches || q === "" ? "" : "none";
  });
}

/***************************************
  Sort Table Function
***************************************/
let currentSortKey = null;
let sortAsc = true;

function sortTable(key, asc) {
  const tbody = document.getElementById("taskTable").getElementsByTagName("tbody")[0];
  const rowsArray = Array.from(tbody.querySelectorAll("tr"));

  rowsArray.sort((a, b) => {
    let valA = getCellValue(a, key);
    let valB = getCellValue(b, key);

    if (typeof valA === 'number' && typeof valB === 'number') {
      return asc ? valA - valB : valB - valA;
    } else {
      valA = valA.toString().toLowerCase();
      valB = valB.toString().toLowerCase();
      if (valA < valB) return asc ? -1 : 1;
      if (valA > valB) return asc ? 1 : -1;
      return 0;
    }
  });

  // Remove existing rows
  while (tbody.firstChild) {
    tbody.removeChild(tbody.firstChild);
  }

  // Append sorted rows
  rowsArray.forEach(row => {
    tbody.appendChild(row);
  });
}

function getCellValue(row, key) {
  switch(key) {
    case "id":
      return parseInt(row.children[0].innerText.trim());
    case "title":
      return row.children[1].innerText.trim().toLowerCase();
    case "priority":
      const text = row.children[3].innerText.trim();
      if(text.includes("Wysoki")) return 3;
      if(text.includes("Średni")) return 2;
      if(text.includes("Niski"))  return 1;
      return 0;
    case "deadline":
      const dl = row.children[2].innerText.trim();
      return dl !== '-' ? new Date(dl).getTime() : 0;
    case "status":
      return row.children[4].innerText.trim() === "Ukończone" ? 1 : 0;
    default:
      return "";
  }
}

/***************************************
  Initialize Global Timers
***************************************/
function initGlobalTimers() {
  const rows = document.querySelectorAll("#taskTable tbody tr");
  const localLoadTime = Date.now() / 1000;

  rows.forEach(row => {
    const isRunning = row.dataset.timerRunning === "true";
    if (!isRunning) return;

    const endTs = parseFloat(row.dataset.timerEnd) || 0;
    let remainSec;
    if (USE_SERVER_TIME_SYNC && serverTimestamp > 0) {
      let serverCalculatedNow = serverTimestamp + (Date.now() / 1000 - localLoadTime);
      remainSec = Math.floor(endTs - serverCalculatedNow);
    } else {
      remainSec = Math.floor(endTs - (Date.now() / 1000));
    }

    if(remainSec <= 0) {
      row.classList.add("alarm-row");
      const disp = row.querySelector(".countdown-display");
      if(disp) disp.textContent = "00:00:00";
    } else {
      startIntervalRow(row, remainSec);
    }
  });
}

function startIntervalRow(row, remainSec) {
  if(!row) return;
  const disp = row.querySelector(".countdown-display");
  if(!disp) return;

  function tick() {
    if(remainSec <= 0) {
      clearInterval(activeIntervals[row.id]);
      row.classList.add("alarm-row");
      disp.textContent = "00:00:00";
      return;
    }
    let h = Math.floor(remainSec / 3600);
    let m = Math.floor((remainSec % 3600) / 60);
    let s = remainSec % 60;
    disp.textContent = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
    remainSec--;
  }
  tick();
  activeIntervals[row.id] = setInterval(tick, 1000);
}

/***************************************
  Toggle Theme Function
***************************************/
function toggleTheme() {
  document.body.classList.toggle("light-mode");
}