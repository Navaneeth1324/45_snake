import os
import pygame
from .snake import Snake
from .food import Food

# Game Engine Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (46, 204, 113)
HEAD_GREEN = (39, 174, 96)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
GRAY = (170, 178, 189)
CARD_BG = (28, 30, 38)
BORDER_COLOR = (231, 76, 60)

def safe_font(name, size, bold=False):
    """Safely get a font with fallback to default pygame font if system font is inaccessible."""
    try:
        font = pygame.font.SysFont(name, size, bold=bold)
        if font:
            return font
    except Exception:
        pass
    return pygame.font.Font(None, size)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food = Food(self.grid_width, self.grid_height, self.cell_size)

        self.score = 0
        self.high_score = 0

        self.font = safe_font("Arial", 26)
        self.title_font = safe_font("Arial", 46, bold=True)
        self.score_font = safe_font("Arial", 28, bold=True)
        self.sub_font = safe_font("Arial", 20)

        # Difficulties and move speeds (Task 3)
        self.difficulty_speeds = {
            "Easy": 6,
            "Medium": 10,
            "Hard": 16
        }
        self.difficulty = "Medium"
        self.moves_per_second = self.difficulty_speeds[self.difficulty]
        self._frame_counter = 0

        self.game_over = False
        self._game_over_logged = False

        # Sound effects (Task 4)
        self.eat_sound = None
        self.game_over_sound = None
        self._init_sounds()

    def _init_sounds(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            eat_path = os.path.join(base_dir, "assets", "sounds", "eat.wav")
            go_path = os.path.join(base_dir, "assets", "sounds", "game_over.wav")
            if os.path.exists(eat_path):
                self.eat_sound = pygame.mixer.Sound(eat_path)
            if os.path.exists(go_path):
                self.game_over_sound = pygame.mixer.Sound(go_path)
        except Exception as e:
            # Fallback gracefully if audio hardware/driver is missing
            self.eat_sound = None
            self.game_over_sound = None

    def restart(self, difficulty=None):
        """Reset the game state and optionally update difficulty (Task 3)."""
        if difficulty and difficulty in self.difficulty_speeds:
            self.difficulty = difficulty
        self.moves_per_second = self.difficulty_speeds[self.difficulty]

        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food = Food(self.grid_width, self.grid_height, self.cell_size)
        self.score = 0
        self._frame_counter = 0
        self.game_over = False
        self._game_over_logged = False

    def handle_keydown(self, key):
        if self.game_over:
            # Replay options on Game Over (Task 3)
            if key in (pygame.K_1, pygame.K_e):
                self.restart(difficulty="Easy")
            elif key in (pygame.K_2, pygame.K_m):
                self.restart(difficulty="Medium")
            elif key in (pygame.K_3, pygame.K_h):
                self.restart(difficulty="Hard")
            elif key in (pygame.K_SPACE, pygame.K_RETURN):
                self.restart(difficulty=self.difficulty)
            elif key in (pygame.K_ESCAPE, pygame.K_q):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        # Direction changes during active gameplay
        if key in (pygame.K_UP, pygame.K_w):
            self.snake.set_direction(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.set_direction(0, 1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.set_direction(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.set_direction(1, 0)

    def handle_input(self):
        # Reserved for continuously-held-key input
        pass

    def trigger_game_over(self):
        if not self.game_over:
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            if self.game_over_sound:
                self.game_over_sound.play()
            if not self._game_over_logged:
                print(f"Game over! Final score: {self.score} | High score: {self.high_score}")
                self._game_over_logged = True

    def update(self):
        if self.game_over:
            return

        self._frame_counter += 1
        frames_per_move = max(1, 60 // self.moves_per_second)
        if self._frame_counter < frames_per_move:
            return
        self._frame_counter = 0

        self.snake.move()

        # Task 1 & 2: Wall collision
        if self.snake.collides_with_wall(self.grid_width, self.grid_height):
            self.trigger_game_over()
            return

        # Task 1 & 2: Self collision
        if self.snake.collides_with_self():
            self.trigger_game_over()
            return

        # Food collision & growth
        if self.snake.head_rect().colliderect(self.food.rect()):
            self.snake.grow()
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
            if self.eat_sound:
                self.eat_sound.play()
            self.food.respawn(self.snake.body)

    def render(self, screen):
        # Draw food (pulsing/bordered circle or rounded rect for better aesthetics)
        food_rect = self.food.rect()
        pygame.draw.rect(screen, RED, food_rect, border_radius=4)
        # Inner highlight on food
        inner_rect = food_rect.inflate(-6, -6)
        pygame.draw.rect(screen, (255, 120, 120), inner_rect, border_radius=3)

        # Draw snake body and head
        segments = self.snake.segment_rects()
        for idx, rect in enumerate(segments):
            if idx == 0:
                # Head
                pygame.draw.rect(screen, HEAD_GREEN, rect, border_radius=5)
            else:
                # Body segment
                pygame.draw.rect(screen, GREEN, rect, border_radius=4)

        # Draw HUD: Score and Difficulty
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (15, 12))

        diff_text = self.sub_font.render(f"Speed: {self.difficulty}", True, GRAY)
        screen.blit(diff_text, (self.width - diff_text.get_width() - 15, 16))

        # Task 2 & Task 3: Game Over Screen
        if self.game_over:
            self._render_game_over_screen(screen)

    def _render_game_over_screen(self, screen):
        # Semi-transparent dark background overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 185))
        screen.blit(overlay, (0, 0))

        # Centered Game Over Card
        card_w, card_h = 460, 320
        card_x = (self.width - card_w) // 2
        card_y = (self.height - card_h) // 2
        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)

        pygame.draw.rect(screen, CARD_BG, card_rect, border_radius=12)
        pygame.draw.rect(screen, BORDER_COLOR, card_rect, width=3, border_radius=12)

        # "GAME OVER" Title
        title_surf = self.title_font.render("GAME OVER", True, RED)
        title_x = card_x + (card_w - title_surf.get_width()) // 2
        screen.blit(title_surf, (title_x, card_y + 25))

        # Final Score & High Score
        score_surf = self.score_font.render(f"Final Score: {self.score}", True, WHITE)
        score_x = card_x + (card_w - score_surf.get_width()) // 2
        screen.blit(score_surf, (score_x, card_y + 85))

        high_surf = self.sub_font.render(f"High Score: {self.high_score}", True, YELLOW)
        high_x = card_x + (card_w - high_surf.get_width()) // 2
        screen.blit(high_surf, (high_x, card_y + 120))

        # Divider line
        pygame.draw.line(screen, (60, 65, 80), (card_x + 30, card_y + 155), (card_x + card_w - 30, card_y + 155), 2)

        # Difficulty Selection Prompt
        diff_prompt = self.sub_font.render("Select Difficulty to Play Again:", True, GRAY)
        screen.blit(diff_prompt, (card_x + (card_w - diff_prompt.get_width()) // 2, card_y + 170))

        # Difficulty options with highlight
        opt_y = card_y + 205
        options = [("[1] Easy", "Easy"), ("[2] Medium", "Medium"), ("[3] Hard", "Hard")]
        spacing = card_w // 3
        for i, (label, mode) in enumerate(options):
            is_active = (self.difficulty == mode)
            col = YELLOW if is_active else WHITE
            opt_surf = self.sub_font.render(label, True, col)
            ox = card_x + i * spacing + (spacing - opt_surf.get_width()) // 2
            screen.blit(opt_surf, (ox, opt_y))

        # Replay / Exit instruction
        replay_surf = self.sub_font.render("Press [SPACE] to Replay  |  [ESC/Q] to Exit", True, GRAY)
        screen.blit(replay_surf, (card_x + (card_w - replay_surf.get_width()) // 2, card_y + 255))
