# Lab 4: VibeCoding - Submission Package

**Student Roll No**: 45  
**Assigned Repository**: [SETAPESU26/45_snake](https://github.com/SETAPESU26/45_snake)  
**Vibe Coding Partner**: Google Antigravity AI Assistant  

---

## Deliverables Summary

Per the instructions in `Lab_4_VibeCoding_Student_handout.pdf`:

### a. Videos (before and after)
Located in `videos/`:
- `gameplay_before.mp4` (10 seconds): Demonstrates the original 180° reverse-turn instant death bug and frozen game state without a Game Over UI.
- `gameplay_after.mp4` (10 seconds): Demonstrates the fixed reversal guard, smooth food collection and growth (+1 score, eat sound chime), fair collision detection, interactive Game Over screen, difficulty selection, and instant replay.

### b. Updated Code
Located in `code/`:
- `game/snake.py`: Collision detection refinement and input queue buffering.
- `game/game_engine.py`: Game Over overlay, difficulty modes (Easy: 6/s, Medium: 10/s, Hard: 16/s), replay logic, and sound integration.
- `assets/sounds/`: Synthesized audio effects (`eat.wav` and `game_over.wav`).
- `main.py`: Pygame event loop and window handling.
- `requirements.txt`: Dependencies (`pygame-ce`).

### c. Chat history exported as a doc/pdf
Located in the root of `Lab-4/`:
- `Chat_History_Lab4.pdf`: Styled multi-page PDF transcript of the complete pair programming session.
- `Chat_History_Lab4.docx`: Microsoft Word document format of the same transcript.

---

## Instructions Completed
- [x] 1. Go to the repo assigned to you (Sl. No 45 -> SETAPESU26/45_snake)
- [x] 2. Go through the ReadMe file to understand the deliverables
- [x] 3. Clone or Fork the repo
- [x] 4. Run the Python based code (Game)
- [x] 5. Record 10 seconds of video before making any changes (`gameplay_before.mp4`)
- [x] 6. Write prompts and fix the broken code (Task 1: Collision & Reversal Guard)
- [x] 7. Write prompts to add all the features listed in the ReadMe file:
  - Task 1: Refined Collision Detection
  - Task 2: Game Over Condition & Screen
  - Task 3: Replay Option with Difficulty Selection
  - Task 4: Sound Feedback (Eat & Game Over sounds)
- [x] 8. Record another 10 seconds of video again after making all the changes (`gameplay_after.mp4`)
- [x] 9. Push the code to your repo (Do not raise PR to main repo SETAPESU26)
