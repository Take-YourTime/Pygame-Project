# 🕐 Digital and Analog Clock

A funny real-time clock application built with **Python** and **Pygame** that displays the current time using both a digital readout and an analog clock face.

---

## ✨ Features
- **Analog clock** — rotating hour, minute, and second hands drawn with Pygame graphics
- **Digital clock** — current time displayed with custom-rendered digit sprites
- **Live update** — refreshes every frame to always show the accurate current time
- **Resizable window** — the window can be resized and the clock scales accordingly

---

## 📁 File Structure
```
Digital and Analog Clock/
├── Digital and Analog Clock.py  # Main entry point
├── Number.py                    # Sprite class for digital digit rendering
├── function.py                  # Shared utility functions
└── background.jpg               # Background image
```

---

## 🚀 How to Run
1. Open this folder in **VS Code** (or any terminal).
2. Make sure **Pygame** is installed:
   ```bash
   pip install pygame
   ```
3. Run the main file:
   ```bash
   python "Digital and Analog Clock.py"
   ```

---

## 🗒️ Notes
- The clock reads the system time via Python's `datetime` module.
- Window size: **1500 × 800** (resizable).
