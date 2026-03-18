# 🦟 Mosquito War

A fast-paced clicker game where you battle waves of mosquitoes using your mouse.  
Click quickly to swat them before they escape — or your health runs out!

> Made in **February, 2024**.

---

## ✨ Features
- **Mouse-controlled gameplay** — your cursor becomes a swatting hand
- **Mosquito sprites** with randomized spawn positions
- **Health system** — lose HP each time a mosquito escapes
- **Score tracking** — earn points for each mosquito you kill
- **Menu screen** with start button and animated markers
- **Pause functionality** with a pause screen
- **BGM & sound effects** — fire, hit, kill, swing, and magic sounds
- **Magic circle effects** for visual flair

---

## 📁 File Structure
```
Mosquito War/
├── mosquito.py           # 🎮 Main entry point — run this to start the game
├── forest.jpg            # Background image
├── sunset.jpg            # Alternative background
├── bug.png               # Mosquito sprite
├── hand.png              # Mouse cursor image
├── blood.png             # Blood splatter effect
├── fire.png              # Fire effect sprite
├── magic_circle.png      # Magic circle effect
├── menu.png              # Menu background
├── pause.png             # Pause button icon
├── pause_background.png  # Pause screen background
├── blue_rect.png         # UI rectangle element
├── start_mark1.png       # Animated start marker (frame 1)
├── start_mark2.png       # Animated start marker (frame 2)
├── BreathAndLife.mp3     # Background music
├── Mortals.mp3           # Alternative background music
├── Ragara.otf            # Font file
├── Sunshine.otf          # Font file
├── fire.wav              # Fire sound effect
├── hit.wav               # Hit sound effect
├── kill.wav              # Kill sound effect
├── magic.wav             # Magic sound effect
├── swing.wav             # Swing sound effect
├── wind_path.mp3         # Wind ambience sound
├── pause.mp3             # Pause music
└── start_mark_sound.wav  # Start screen sound effect
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
   python mosquito.py
   ```

---

## 🕹️ Controls
| Input | Action |
|-------|--------|
| Mouse Move | Aim the swatter |
| Left Mouse Button | Swat / click mosquitoes |
| Pause Button (on screen) | Pause the game |

---

## 🗒️ Notes
- Window size: **1280 × 720**.
- Mosquitoes spawn at random positions within the window boundaries.

