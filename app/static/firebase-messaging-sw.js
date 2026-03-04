// Firebase Service Worker - 백그라운드 푸시 알림 처리
importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyACrdE8rQvj7i1l8Lnl32xTqY-GVGw556Q",
  authDomain: "cloud9-care.firebaseapp.com",
  projectId: "cloud9-care",
  storageBucket: "cloud9-care.firebasestorage.app",
  messagingSenderId: "879037848068",
  appId: "1:879037848068:web:cc2a4b44d3432c8e7db351",
});

const messaging = firebase.messaging();

// 백그라운드 메시지 수신 처리
messaging.onBackgroundMessage((payload) => {
  console.log('📱 Service Worker: 백그라운드 메시지 수신', payload);
  const { title, body } = payload.notification;
  self.registration.showNotification(title, {
    body,
    icon: '/static/img/pill_front.png',
    data: payload.data,
    actions: [{ action: 'confirm', title: '확인' }],
  });
  console.log('✅ Service Worker: 알림 표시 완료');
});

// 알림 클릭 처리
self.addEventListener('notificationclick', (event) => {
  console.log('👆 Service Worker: 알림 클릭', event.action);
  event.notification.close();
  if (event.action === 'confirm') {
    const alarmId = event.notification.data?.alarm_id;
    console.log('✅ Service Worker: 알람 확인 요청', alarmId);
    if (alarmId) {
      event.waitUntil(
        fetch(`/api/v1/alarms/history/confirm/${alarmId}`, { method: 'POST' })
          .then(() => console.log('✅ Service Worker: 알람 확인 완료'))
          .catch(e => console.error('❌ Service Worker: 알람 확인 실패', e))
      );
    }
  }
  event.waitUntil(clients.openWindow('/alarm'));
});
