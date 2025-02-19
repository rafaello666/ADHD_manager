// static/sw.js
self.addEventListener('push', function(event) {
    console.log('Otrzymano wydarzenie push');
    let notificationData = {};
    if (event.data) {
      try {
        notificationData = event.data.json();
      } catch (e) {
        notificationData = { title: 'ADHD Manager', body: event.data.text() };
      }
    }
    const title = notificationData.title || 'ADHD Manager';
    const options = {
      body: notificationData.body || event.data.text() || 'Nowe powiadomienie.',
      icon: '/static/icon.png' // (Uzupełnij ścieżkę do ikony, jeśli posiadasz plik graficzny)
    };
    event.waitUntil(
      self.registration.showNotification(title, options)
    );
  });
  
  self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(
      clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clientList => {
        if (clientList.length > 0) {
          return clientList[0].focus();
        }
        return clients.openWindow('/');
      })
    );
  });
  