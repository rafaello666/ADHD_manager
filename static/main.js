// static/main.js
const publicVapidKey = "<TWÓJ_PUBLICZNY_KLUCZ VAPID>";  // Upewnij się, że klucz jest zgodny z tym w .env

if ('serviceWorker' in navigator && 'PushManager' in window) {
  navigator.serviceWorker.register('/static/sw.js')
    .then(registration => {
      console.log('Service Worker zarejestrowany.');
      return Notification.requestPermission().then(permission => {
        if (permission !== 'granted') {
          throw new Error('Brak zgody na powiadomienia push.');
        }
        const convertedKey = urlB64ToUint8Array(publicVapidKey);
        return registration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: convertedKey
        });
      });
    })
    .then(subscription => {
      console.log('Uzyskano subskrypcję push:', subscription);
      return fetch('/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(subscription)
      });
    })
    .then(response => {
      if (response.ok) {
        console.log('Subskrypcja zapisana na serwerze.');
      } else {
        console.error('Błąd podczas zapisywania subskrypcji.');
      }
    })
    .catch(err => console.error('Błąd konfiguracji push:', err));
} else {
  console.warn('Powiadomienia push nie są obsługiwane w tej przeglądarce.');
}

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const rawData = window.atob(base64);
  return Uint8Array.from([...rawData].map(char => char.charCodeAt(0)));
}
