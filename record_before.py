import os
import subprocess
import imageio_ffmpeg
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
from game.game_engine import GameEngine

def record_before():
    pygame.init()
    WIDTH, HEIGHT = 600, 600
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    FPS = 30
    TOTAL_SECONDS = 10
    TOTAL_FRAMES = FPS * TOTAL_SECONDS

    output_path = "gameplay_before.mp4"
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.Popen([
        ffmpeg_exe, "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", output_path
    ], stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    engine = GameEngine(WIDTH, HEIGHT)

    # Place food so it is visible
    engine.food.x = 22
    engine.food.y = 15

    for frame in range(TOTAL_FRAMES):
        SCREEN.fill((0, 0, 0))

        # At frame 60 (2.0s), player taps LEFT while snake is moving RIGHT
        if frame == 60:
            print("Action: Tapping LEFT while moving RIGHT (bug trigger)")
            engine.handle_keydown(pygame.K_LEFT)

        # After frame 90, simulate player trying to press keys (UP, DOWN, SPACE)
        if frame == 120:
            engine.handle_keydown(pygame.K_UP)
        elif frame == 180:
            engine.handle_keydown(pygame.K_SPACE)

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        # Overlay a subtle visual label explaining the buggy behavior
        font = pygame.font.SysFont("Arial", 22)
        if frame < 60:
            status_text = font.render("[BEFORE] Snake moving RIGHT...", True, (255, 255, 100))
        elif frame < 90:
            status_text = font.render("[BUG] Pressed LEFT -> Instant unfair death into neck!", True, (255, 80, 80))
        else:
            status_text = font.render("[BUG] Frozen without Game Over UI or Replay menu", True, (255, 120, 120))
        SCREEN.blit(status_text, (10, 560))

        frame_bytes = pygame.image.tobytes(SCREEN, "RGB")
        proc.stdin.write(frame_bytes)

    proc.stdin.close()
    proc.wait()
    pygame.quit()
    print(f"Recorded before video successfully to {output_path}")

if __name__ == "__main__":
    record_before()
