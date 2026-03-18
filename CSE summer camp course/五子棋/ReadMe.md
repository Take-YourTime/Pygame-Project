# ♟️ 五子棋 (Gomoku / Five in a Row)

A two-player **Gomoku** (Five in a Row) board game built with Pygame.  
Players take turns placing black and white pieces on a 15×15 grid — the first to get five in a row wins!

---

## ✨ Features
- **15 × 15 game board** rendered with Pygame graphics
- **Black and white piece sprites** loaded from image files
- **Win detection** — checks rows, columns, and diagonals for five consecutive pieces
- **Semi-transparent piece preview** on mouse hover
- **60 FPS** smooth rendering
- **Custom font** for UI text display

---

## 📁 File Structure
```
五子棋/
├── Game.py      # 🎮 Main entry point — run this to start the game
├── Pieces.py    # Piece and PiecesGroup sprite classes
├── Setting.py   # Global constants (window size, board dimensions, colors)
├── img/
│   ├── Black.png   # Black piece image
│   ├── White.png   # White piece image
│   └── font.ttf    # Font used for UI text
└── sound/          # Sound assets
```

---

## 🚀 How to Run
1. Open this folder in **VS Code** (or any terminal).
2. Make sure **Pygame** is installed:
   ```bash
   pip install pygame
   ```
3. Run the main file **from inside this folder**:
   ```bash
   python Game.py
   ```

---

## 🕹️ How to Play
| Input | Action |
|-------|--------|
| Mouse Move | Preview piece placement |
| Left Mouse Button | Place a piece |

- **Player 1** plays Black pieces.
- **Player 2** plays White pieces.
- Players alternate turns — the first to place **5 pieces in a row** (horizontally, vertically, or diagonally) wins!

---

## 🗒️ Notes
- Window size: **750 × 750**.
- Board: **15 lines × 15 lines** (standard Gomoku size).
- This game was built to practice object-oriented programming with Pygame sprites during the summer camp.
