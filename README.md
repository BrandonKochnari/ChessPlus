# Chess+ ♟️⚔️

**Chess+** is a Python-based reimagining of traditional chess, built with **Pygame**.  
It blends the strategic foundation of chess with **RPG-inspired mechanics**: health bars, attack stats, and unique special abilities for every piece.  
The result is a fast-paced, tactical experience that challenges players to think beyond standard chess moves.  

---

## ✨ Features

- **Enhanced Chess Gameplay**
  - Each piece has **HP** and **ATK** values instead of being instantly captured.
  - Battles involve attacks, counterattacks, and attrition.
- **Unique Piece Abilities**
  - **Pawn** → *Sacrificial Promotion*: temporarily promotes before perishing.  
  - **Rook** → *Indomitability*: temporary invincibility.  
  - **Knight** → *Double Charge*: two-move turns with weaker follow-up strikes.  
  - **Bishop** → *Healing Prayer*: heals allies by its attack power.  
  - **Queen** → *Charismatic Aura*: buffs nearby allies with doubled HP and ATK.  
  - **King** → *Tactical Exchange*: swap positions with an ally.
- **Dynamic Game Systems**
  - **Timers** for each side, like competitive chess.  
  - **Special gauge** that charges from battle outcomes.  
  - **Custom HP/ATK stat bars** with mouseover adjustments in Strategy mode.  
  - **Turn-based history tracking** with debuff expiration.
- **Interactive GUI**
  - Full **Pygame UI** with menus, buttons, and background music.  
  - Highlighted selections and grid-based rendering.  
  - Win screens for timeouts and checkmate conditions.  

---

## 🛠️ Requirements

- Python **3.10+**  
- Libraries:
  - `pygame`
  - `math`
  - `time`

Install dependencies:
```bash
pip install pygame
```

## 🚀 Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/BrandonKochnari/ChessPlus.git
   cd ChessPlus
2. Run the game:
   ```bash
   python Chess.py
3. Controls:
  • Mouse → select and move pieces.  
  • P → pause music.  
  • R → resume music.  
  • Spacebar → activate special abilities.  

## 🕹️ Example Gameplay

• Openings feel familiar: pawns advance, knights hop forward.  
• A Rook under attack may activate Indomitability to block threats.  
• A Bishop heals a wounded Queen mid-match.  
• Queens buff armies, creating high-stakes showdowns.  
• Games can end by checkmate (taking out all hitpoints of the King) or when the timer expires.  

## 📂 Project Structure

• Chess.py → Main loop, state handling, and rendering.  
• ChessPiece.py → Piece classes with stats and special abilities.  
• GameBoard.py → Board state, observation system, attack counters.  
• MainMenu.py → Menu, options, and button rendering.  
• assets/ → Piece sprites, background images, UI elements, sound.  

## 🔮 Future Improvements

• Finalize transition to Unity Engine (C#)
• AI opponent with adaptive strategy.  
• Online multiplayer support.  
• Expanded abilities and status effects.  
• Addition of animations to taking, abilities, movement etc...  
• Save/load system for loacal matches.  
