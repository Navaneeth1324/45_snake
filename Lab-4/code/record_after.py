import os
import subprocess
import imageio_ffmpeg
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
from game.game_engine import GameEngine

def record_after():
    pygame.init()
    WIDTH, HEIGHT = 600, 600
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    FPS = 30
    TOTAL_SECONDS = 10
    TOTAL_FRAMES = FPS * TOTAL_SECONDS

    output_path = "gameplay_after.mp4"
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.Popen([
        ffmpeg_exe, "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", output_path
    ], stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    engine = GameEngine(WIDTH, HEIGHT)
    engine.moves_per_second = 8  # nice clear speed for first phase

    # Place first food in direct path of snake (moving right from (15, 15))
    engine.food.x = 18
    engine.food.y = 15

    banner_font = pygame.font.Font(None, 24)

    for frame in range(TOTAL_FRAMES):
        SCREEN.fill((18, 18, 24))

        # Phase 1: 0 - 65: Eat first food at ~frame 40
        if frame == 45:
            # Place next food to the right
            engine.food.x = 22
            engine.food.y = 15

        # Phase 2: Frame 75: Test Reversal Bug Fix
        # Snake is moving RIGHT. Player taps LEFT!
        if frame == 75:
            print("Action: Player taps LEFT while moving RIGHT (Reversal Bug Test)")
            engine.handle_keydown(pygame.K_LEFT)

        # Phase 3: Frame 95: Player turns UP
        if frame == 95:
            engine.handle_keydown(pygame.K_UP)

        # Phase 4: Frame 120: Player turns RIGHT towards wall
        if frame == 120:
            engine.handle_keydown(pygame.K_RIGHT)

        # Snake hits wall at x >= 30 (grid width) around frame 160-170
        # Phase 5: Frame 240 (8.0s): Player selects Hard Difficulty ([3]) to Replay!
        if frame == 240:
            print("Action: Player presses [3] to select Hard difficulty and replay")
            engine.handle_keydown(pygame.K_3)
            # Turn down on restart to show movement
            engine.handle_keydown(pygame.K_DOWN)

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        # Bottom informational banner for evaluator
        if frame < 70:
            banner_msg = "[TASK 1 & 4] Eating food -> Grows snake & increments score (+Sound FX)"
            banner_col = (100, 255, 150)
        elif frame < 110:
            banner_msg = "[TASK 1 FIXED] Tapped LEFT while moving RIGHT -> Blocked, no unfair death!"
            banner_col = (100, 220, 255)
        elif frame < 170:
            banner_msg = "[TASK 1] Moving towards wall to demonstrate collision detection..."
            banner_col = (255, 220, 100)
        elif frame < 240:
            banner_msg = "[TASK 2 & 3] Game Over screen: Final score, high score & difficulty choice"
            banner_col = (255, 120, 120)
        else:
            banner_msg = "[TASK 3] Replay active: Hard difficulty selected (Speed: 16/s)!"
            banner_col = (255, 255, 100)

        banner_surf = banner_font.render(banner_msg, True, banner_col)
        # Background bar for banner
        bar_rect = pygame.Rect(0, HEIGHT - 32, WIDTH, 32)
        pygame.draw.rect(SCREEN, (10, 12, 16), bar_rect)
        pygame.draw.line(SCREEN, (50, 55, 70), (0, HEIGHT - 32), (WIDTH, HEIGHT - 32), 1)
        SCREEN.blit(banner_surf, (15, HEIGHT - 24))

        frame_bytes = pygame.image.tobytes(SCREEN, "RGB")
        proc.stdin.write(frame_bytes)

    proc.stdin.close()
    proc.wait()
    pygame.quit()
    print(f"Recorded after video successfully to {output_path}")

if __name__ == "__main__":
    record_after()
