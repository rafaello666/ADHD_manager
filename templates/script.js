// Funkcja przykładowa: zmiana statusu zadania na ukończone (lub odwrotnie).
function toggleDone(button) {
    const statusSpan = button
      .closest('tr')
      .querySelector('.status');
  
    if (statusSpan.classList.contains('not-done')) {
      statusSpan.textContent = 'Ukończone';
      statusSpan.classList.remove('not-done');
      statusSpan.classList.add('done');
    } else {
      statusSpan.textContent = 'Nieukończone';
      statusSpan.classList.remove('done');
      statusSpan.classList.add('not-done');
    }
  }
  
  // Przykładowo wczytywanie dynamicznej wartości progresu (jeśli chcesz)
  document.addEventListener('DOMContentLoaded', function() {
    const progressCircle = document.querySelector('.progress-ring__progress');
    const totalLength = 314; // 2πr przy r=50
    let completionRate = 0.80; // 80% w recenzji
  
    const offset = totalLength - (totalLength * completionRate);
    progressCircle.style.strokeDashoffset = offset;
  });
  