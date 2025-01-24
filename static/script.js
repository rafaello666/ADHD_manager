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
  
    updateProgress();
  }
  
  // Aktualizacja wskaźnika postępu na podstawie ukończonych zadań
  function updateProgress() {
    const statusSpans = document.querySelectorAll('.status');
    const totalTasks = statusSpans.length;
    const doneTasks = Array.from(statusSpans).filter(span => span.classList.contains('done')).length;
    const completionRate = totalTasks > 0 ? doneTasks / totalTasks : 0;
  
    // Aktualizacja tekstu
    const progressText = document.getElementById('progress-text');
    progressText.innerHTML = `${Math.round(completionRate * 100)}%<br/>Ogólny Postęp`;
  
    // Aktualizacja wskaźnika SVG
    const progressCircle = document.querySelector('.progress-ring__progress');
    const totalLength = 314; // 2πr przy r=50
    const offset = totalLength - (totalLength * completionRate);
    progressCircle.style.strokeDashoffset = offset;
  }
  
  // Przykładowo wczytywanie dynamicznej wartości progresu (jeśli chcesz)
  document.addEventListener('DOMContentLoaded', function() {
    updateProgress();
  });
  