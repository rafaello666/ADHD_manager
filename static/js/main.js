/***************************************************
 * main.js
 * Obsługa timera (start/stop), filtracji zadań
 * oraz inicjalizacja wykresów Chart.js.
 **************************************************/

document.addEventListener("DOMContentLoaded", () => {
  // Filtracja tabeli zadań
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", applyFilter);
  }

  // Inicjalizacja wykresów (Chart.js)
  initializeCharts();

  // Licznik Start/Stop
  initializeCountdownTimer();
});

/**
 * Filtruje tabelę zadań na podstawie wpisanego tekstu.
 */
function applyFilter() {
  const query = document.getElementById("searchInput").value.trim().toLowerCase();
  const rows = document.querySelectorAll("#taskTable tbody tr");

  rows.forEach((row) => {
    const title = row.children[1].innerText.toLowerCase();
    row.style.display = (title.includes(query) || query === "") ? "" : "none";
  });
}

/**
 * Inicjalizuje wykresy Chart.js.
 *  - Wykres priorytetów (Pie Chart)
 *  - Wykres HR/HRV (Line Chart)
 */
function initializeCharts() {
  // Wykres Priorytetów
  const priorityCanvas = document.getElementById("priorityChart");
  if (priorityCanvas) {
    const ctx = priorityCanvas.getContext("2d");
    new Chart(ctx, {
      type: "pie",
      data: {
        labels: ["Wysoki", "Średni", "Niski"],
        datasets: [
          {
            data: [
              priorityData.wysoki || 0,
              priorityData.sredni || 0,
              priorityData.niski || 0
            ],
            backgroundColor: [
              "rgba(220,53,69,0.7)",   // Wysoki (czerwony)
              "rgba(255,193,7,0.7)",  // Średni (żółty)
              "rgba(25,135,84,0.7)",  // Niski  (zielony)
            ],
            borderColor: [
              "rgba(220,53,69,1)",
              "rgba(255,193,7,1)",
              "rgba(25,135,84,1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  }

  // Wykres HR/HRV
  const hrvCanvas = document.getElementById("hrvChart");
  if (hrvCanvas) {
    const ctx = hrvCanvas.getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00"],
        datasets: [
          {
            label: "HR (bpm)",
            data: [82, 83, 85, 87, 86, 88],
            borderColor: "rgba(220,53,69,1)",
            backgroundColor: "rgba(220,53,69,0.1)",
            fill: true,
            tension: 0.3,
            yAxisID: "y1",
          },
          {
            label: "HRV (ms)",
            data: [35, 36, 34, 33, 37, 38],
            borderColor: "rgba(25,135,84,1)",
            backgroundColor: "rgba(25,135,84,0.1)",
            fill: true,
            tension: 0.3,
            yAxisID: "y2",
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y1: {
            type: "linear",
            position: "left",
            title: {
              display: true,
              text: "HR (bpm)",
            },
            ticks: {
              beginAtZero: true
            }
          },
          y2: {
            type: "linear",
            position: "right",
            title: {
              display: true,
              text: "HRV (ms)",
            },
            grid: {
              drawOnChartArea: false,
            },
            ticks: {
              beginAtZero: true
            }
          },
        },
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  }
}

/**
 * Inicjalizuje licznik (countdown) z przyciskami Start/Stop.
 * Możesz zmienić zachowanie, np. restartować licznik itp.
 */
function initializeCountdownTimer() {
  const countdownDisplay = document.getElementById("countdownDisplay");
  const startBtn = document.getElementById("startTimerBtn");
  const stopBtn = document.getElementById("stopTimerBtn");

  // Sprawdzamy, czy elementy istnieją na stronie
  if (!countdownDisplay || !startBtn || !stopBtn) return;

  // Domyślnie 30 minut
  const initialMinutes = 30;
  let endTime = null;
  let paused = true;
  let countdownInterval = null;

  /**
   * Aktualizuje widok (countdownDisplay).
   * Jeśli timer dojdzie do zera, zatrzymuje się i wyświetla 00:00:00.
   */
  function updateCountdown() {
    if (paused || !endTime) return;

    const now = new Date();
    const distance = endTime - now;

    // Gdy czas się skończy
    if (distance <= 0) {
      clearInterval(countdownInterval);
      countdownInterval = null;
      countdownDisplay.textContent = "00:00:00";
      countdownDisplay.classList.add("text-danger", "fw-bold");
      stopBtn.disabled = true;
      startBtn.disabled = true;
      return;
    }

    // Obliczamy hh:mm:ss
    const hours = Math.floor(distance / 3600000);
    const minutes = Math.floor((distance % 3600000) / 60000);
    const seconds = Math.floor((distance % 60000) / 1000);

    countdownDisplay.textContent =
      `${String(hours).padStart(2, "0")}:` +
      `${String(minutes).padStart(2, "0")}:` +
      `${String(seconds).padStart(2, "0")}`;
  }

  // START
  startBtn.addEventListener("click", () => {
    if (paused) {
      // Jeśli pierwszy raz startujemy (endTime pusty), ustawiamy go
      if (!endTime) {
        const now = new Date();
        endTime = new Date(now.getTime() + initialMinutes * 60 * 1000);
      }
      paused = false;
      stopBtn.disabled = false;
      startBtn.disabled = true;
      countdownDisplay.classList.remove("text-danger", "fw-bold");

      // Uruchamiamy update co 1 sek, jeśli nie mamy jeszcze intervala
      if (!countdownInterval) {
        countdownInterval = setInterval(updateCountdown, 1000);
      }
    }
  });

  // STOP/PAUZA
  stopBtn.addEventListener("click", () => {
    if (!paused) {
      paused = true;
      stopBtn.disabled = true;
      startBtn.disabled = false;
    }
  });

  // Na starcie wyświetlamy "00:30:00"
  countdownDisplay.textContent = `00:${String(initialMinutes).padStart(2, "0")}:00`;
}
