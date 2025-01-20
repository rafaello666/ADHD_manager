/***************************************
 script.js – front-end logika
***************************************/

// Czy używać synchronizacji z czasem serwera?
const USE_SERVER_TIME_SYNC = true;

// Odczytamy server_now z input hidden (z index.html)
let serverTimestamp = 0;

document.addEventListener("DOMContentLoaded", () => {
  const serverNowElem = document.getElementById("serverNowValue");
  if (serverNowElem) {
    serverTimestamp = parseFloat(serverNowElem.value) || 0;
  }

  // Inicjalizacja sortowania
  const headers = document.querySelectorAll("#taskTable thead th[data-sort]");
  headers.forEach(h => {
    h.addEventListener("click", ()=>{
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

  // Uruchamiamy timery
  initGlobalTimers();
});

/***************************************
 1) Filtrowanie / Wyszukiwanie
***************************************/
async function applyFilter() {
  const q = document.getElementById("searchInput").value.trim().toLowerCase();
  if(!q) {
    // pusty => reload
    window.location.reload();
    return;
  }
  try {
    const resp = await fetch(`/tasks/search?q=${encodeURIComponent(q)}`);
    const data = await resp.json();
    renderTableRows(data);
  } catch(e) {
    console.error("Błąd wyszukiwania:", e);
  }
}

function renderTableRows(tasks) {
  // Uproszczona wersja dynamicznego generowania
  const tbody = document.getElementById("tableBody");
  tbody.innerHTML = "";

  tasks.forEach(t => {
    const row = document.createElement("tr");
    row.id = "row-" + t.id;
    row.dataset.taskId = t.id;
    row.dataset.timerRunning = t.timer_running ? "true" : "false";
    row.dataset.timerEnd = t.timer_end ? t.timer_end : 0;

    // Kolumny: ID / Tytuł / Priorytet / Deadline / Status / Timer / (Akcje)
    const priorityLabel = (()=>{
      if(t.priority > 7) return '<span class="priority-tag high">Wysoki</span>';
      else if(t.priority > 4) return '<span class="priority-tag medium">Średni</span>';
      else return '<span class="priority-tag low">Niski</span>';
    })();

    const statusLabel = t.completed
      ? '<span class="status-tag done">Ukończone</span>'
      : '<span class="status-tag ongoing">Nieukończone</span>';

    row.innerHTML = `
      <td>${t.id}</td>
      <td>${t.title}</td>
      <td>${priorityLabel}</td>
      <td>${t.deadline || '-'}</td>
      <td>${statusLabel}</td>
      <td class="time-cell">
        <span class="countdown-display">--:--:--</span>
      </td>
      <td>(Brak akcji w tej wersji JS)</td>
    `;
    tbody.appendChild(row);
  });

  initGlobalTimers();
}

/***************************************
 2) Sortowanie
***************************************/
let currentSortKey = null;
let sortAsc = true;

function sortTable(key, asc) {
  const tbody = document.getElementById("tableBody");
  const rowsArr = Array.from(tbody.querySelectorAll("tr"));

  rowsArr.sort((a,b)=>{
    let valA = getCellValue(a, key);
    let valB = getCellValue(b, key);
    if(!isNaN(valA)) valA = parseFloat(valA);
    if(!isNaN(valB)) valB = parseFloat(valB);

    if(valA < valB) return asc ? -1 : 1;
    if(valA > valB) return asc ? 1 : -1;
    return 0;
  });

  rowsArr.forEach(r => tbody.appendChild(r));
}

function getCellValue(row, key) {
  switch(key) {
    case "id":
      return row.children[0].innerText.trim();
    case "title":
      return row.children[1].innerText.trim().toLowerCase();
    case "priority": {
      const text = row.children[2].innerText.trim();
      if(text.includes("Wysoki")) return 3;
      if(text.includes("Średni")) return 2;
      if(text.includes("Niski"))  return 1;
      return 0;
    }
    case "deadline":
      return row.children[3].innerText.trim();
    case "status": {
      const st = row.children[4].innerText.trim();
      return st.includes("Ukończone") ? 1 : 0;
    }
    default:
      return "";
  }
}

/***************************************
 3) Przełączanie Motywu
***************************************/
function toggleTheme() {
  document.body.classList.toggle("light-mode");
}

/***************************************
 4) Global Timer
***************************************/
const localLoadTime = Date.now()/1000;
const activeIntervals = {};

function initGlobalTimers() {
  const rows = document.querySelectorAll("#tableBody tr[data-task-id]");
  rows.forEach(row => {
    const isRunning = (row.dataset.timerRunning === "true");
    if(!isRunning) return;

    const endTs = parseFloat(row.dataset.timerEnd) || 0;
    let nowClient = Date.now()/1000;

    let remainSec;
    if(USE_SERVER_TIME_SYNC && serverTimestamp > 0) {
      // Czas serwera w momencie ładowania strony
      // plus różnica upływu czasu lokalnego
      let serverCalculatedNow = serverTimestamp + (nowClient - localLoadTime);
      remainSec = Math.floor(endTs - serverCalculatedNow);
    } else {
      remainSec = Math.floor(endTs - nowClient);
    }

    console.log(`[initGlobalTimers] row=${row.id}, endTs=${endTs}, remainSec=${remainSec}`);

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
    let m = Math.floor((remainSec % 3600)/60);
    let s = remainSec % 60;
    disp.textContent = String(h).padStart(2,'0') + ":" +
                       String(m).padStart(2,'0') + ":" +
                       String(s).padStart(2,'0');
    remainSec--;
  }
  tick();
  activeIntervals[row.id] = setInterval(tick, 1000);
}
