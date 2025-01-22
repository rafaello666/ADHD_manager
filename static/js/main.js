document.addEventListener("DOMContentLoaded", () => {
  // Inicjalizacja filtrów
  const searchInput = document.getElementById("searchInput");
  searchInput.addEventListener("input", applyFilter);

  // Inicjalizacja wykresów
  initializeCharts();

  // Inicjalizacja licznika
  initializeCountdownTimer();
});

/**
 * Filtruje tabelę zadań na podstawie wprowadzonego zapytania
 */
function applyFilter() {
  const query = document.getElementById("searchInput").value.trim().toLowerCase();
  const rows = document.querySelectorAll("#taskTable tbody tr");
  rows.forEach((row) => {
    const title = row.children[1].innerText.toLowerCase();
    const matches = title.includes(query);
    row.style.display = matches || query === "" ? "" : "none";
  });
}

/**
 * Inicjalizuje wykresy za pomocą Chart.js
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
            data: [priorityData.wysoki, priorityData.sredni, priorityData.niski],
            backgroundColor: [
              "rgba(220,53,69,0.7)",   // Wysoki
              "rgba(255,193,7,0.7)",   // Średni
              "rgba(25,135,84,0.7)",   // Niski
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
          title: {
            display: false,
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
              beginAtZero: true,
            },
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
              beginAtZero: true,
            },
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
 * Inicjalizuje licznik odliczający do zakończenia zadania lub sesji
 */
function initializeCountdownTimer() {
  const countdownDisplay = document.getElementById("countdownDisplay");
  if (!countdownDisplay) return;

  // Przykładowy czas zakończenia (w przyszłości)
  const endTime = new Date();
  endTime.setMinutes(endTime.getMinutes() + 30); // 30 minut od teraz

  function updateCountdown() {
    const now = new Date();
    const distance = endTime - now;

    if (distance < 0) {
      clearInterval(countdownInterval);
      countdownDisplay.textContent = "00:00:00";
      countdownDisplay.classList.add("text-danger", "fw-bold");
      return;
    }

    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    countdownDisplay.textContent = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  }

  updateCountdown(); // Początkowe wywołanie
  const countdownInterval = setInterval(updateCountdown, 1000);
}