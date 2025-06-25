
<h1 align="center">📡 Arduino Ultrasonic Obstacle Detection</h1>

<p align="center">
  <em>Real-time distance detection using the HC-SR04 ultrasonic sensor and Arduino Uno</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Arduino-Uno-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Sensor-HC--SR04-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Feature-Distance%20Detection-ff69b4?style=for-the-badge" />
</p>

---

## 🎯 Project Overview

This project uses an **HC-SR04 ultrasonic sensor** connected to an **Arduino Uno** to measure the distance of obstacles in front of it. It calculates the time taken by the ultrasonic pulse to return and converts it to distance (in centimeters), displaying it via the Serial Monitor or an optional LCD.

> 💡 Great for beginner Arduino projects, robotics, or IoT integrations.

---

## 🔧 Components Used

| Component         | Description                       |
|------------------|-----------------------------------|
| Arduino Uno       | Microcontroller board             |
| HC-SR04 Sensor     | Ultrasonic distance sensor        |
| Breadboard & Wires | For easy prototyping              |
| (Optional) Buzzer | Alert on short distance detected  |
| (Optional) LCD     | For displaying distance values    |

---

## 🔌 Wiring Diagram

| HC-SR04 Pin | Connects To       |
|-------------|-------------------|
| VCC         | 5V on Arduino     |
| GND         | GND on Arduino    |
| TRIG        | Digital Pin 9     |
| ECHO        | Digital Pin 10    |

---

## 🧠 Arduino Code

```cpp
#define TRIG_PIN 9
#define ECHO_PIN 10

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  long duration;
  float distanceCm;

  // Send ultrasonic pulse
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Measure response time
  duration = pulseIn(ECHO_PIN, HIGH);
  distanceCm = duration * 0.034 / 2;

  // Display result
  Serial.print("Distance: ");
  Serial.print(distanceCm);
  Serial.println(" cm");

  delay(500);
}
````

---

## 📈 Output Example

```
Distance: 18.23 cm
Distance: 18.31 cm
Distance: 17.98 cm
```

---

## 🚨 Optional Add-ons

| Feature            | Description                                 |
| ------------------ | ------------------------------------------- |
| 🔔 Buzzer          | Add an alert when object is <10cm           |
| 💬 LCD Display     | Show the distance on a 16x2 LCD screen      |
| 🔗 IoT Integration | Send values via WiFi (ESP8266/ESP32)        |
| 🤖 Motor Response  | Stop/redirect robot based on distance logic |

---

## 📦 Project Folder Structure

```
ultrasonic-obstacle-detector/
├── Arduino/
│   └── obstacle_distance.ino
├── images/
│   └── wiring_diagram.png
└── README.md
```

---

## 📸 Gallery

<p align="center">
  <img src="https://your-link.com/wiring_diagram.png" width="400" />
  <br/>
  <em>Basic wiring setup for HC-SR04 and Arduino Uno</em>
</p>

---

## 🤝 Contributing

Feel free to fork this project, add cool features, or help with optimizations!
Pull requests are welcome 💡

---

## 📜 License

This project is open-source under the **MIT License**.
