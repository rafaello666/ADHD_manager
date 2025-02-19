// Plik: MotionTrackerService.kt
package com.example.adhdmanager

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.os.Handler
import android.os.Looper
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import androidx.core.app.NotificationCompat
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.content.Context

class MotionTrackerService : Service(), SensorEventListener {
    private lateinit var sensorManager: SensorManager
    private var lastAcceleration: Float = 0.0f
    private val handler = Handler(Looper.getMainLooper())
    private val inactivityRunnable = Runnable {
        // Kod wysyłający powiadomienie po 15 minutach bez ruchu
        sendInactivityNotification()
    }

    override fun onCreate() {
        super.onCreate()
        // Inicjalizacja czujnika akcelerometru
        sensorManager = getSystemService(Context.SENSOR_SERVICE) as SensorManager
        val accel = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
        // Rejestracja nasłuchiwacza czujnika
        sensorManager.registerListener(this, accel, SensorManager.SENSOR_DELAY_NORMAL)
        // Utworzenie kanału powiadomień (dla Android 8.0+)
        createNotificationChannel()
        // Zaplanowanie pierwszego powiadomienia po 15 minutach braku ruchu
        handler.postDelayed(inactivityRunnable, 15 * 60 * 1000)
    }

    override fun onDestroy() {
        super.onDestroy()
        // Wyrejestrowanie nasłuchiwacza czujnika i usunięcie oczekujących zadań
        sensorManager.unregisterListener(this)
        handler.removeCallbacks(inactivityRunnable)
    }

    override fun onBind(intent: Intent?): IBinder? {
        // Nie korzystamy z komunikacji z service (tzw. unbound service)
        return null
    }

    override fun onSensorChanged(event: SensorEvent) {
        if (event.sensor.type == Sensor.TYPE_ACCELEROMETER) {
            val x = event.values[0]
            val y = event.values[1]
            val z = event.values[2]
            // Obliczenie łącznej siły przyspieszenia (uwzględnia grawitację)
            val totalAcceleration = Math.sqrt((x*x + y*y + z*z).toDouble()).toFloat()
            // Sprawdzenie, czy nastąpiła istotna zmiana (ruch) względem poprzedniego pomiaru
            if (Math.abs(totalAcceleration - lastAcceleration) > 0.5f) {
                // Wykryto ruch – zresetuj licznik bezruchu
                handler.removeCallbacks(inactivityRunnable)
                handler.postDelayed(inactivityRunnable, 15 * 60 * 1000)  // ponowne 15 minut
            }
            lastAcceleration = totalAcceleration
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        // Nie używamy w tej implementacji
    }

    private fun sendInactivityNotification() {
        val notificationId = 1
        val channelId = "movement_alerts"
        val notificationBuilder = NotificationCompat.Builder(this, channelId)
            .setSmallIcon(R.drawable.ic_notification)  // Upewnij się, że taki zasób istnieje
            .setContentTitle("Przypomnienie o ruchu")
            .setContentText("Minęło 15 minut bez zmiany pozycji. Czas się poruszyć!")
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)

        // Wyświetlenie powiadomienia
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.notify(notificationId, notificationBuilder.build())
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channelId = "movement_alerts"
            val channelName = "Alerty o bezruchu"
            val importance = NotificationManager.IMPORTANCE_DEFAULT
            val channel = NotificationChannel(channelId, channelName, importance)
            channel.description = "Powiadomienia o braku ruchu przez 15 minut"
            val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }
}
