import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, LANGUAGES, DIFFICULTIES, DIFFICULTY
from ui import (Button, draw_text_centered, draw_text,
                font_title, font_large, font_medium, font_small, font_hud,
                C_BG, C_PANEL, C_BORDER, C_WHITE, C_YELLOW,
                C_GREEN, C_RED, C_BLUE, C_PURPLE, C_GREY)


def _bg(surf):
    surf.fill(C_BG)
    # Simple scanline effect
    for y in range(0, SCREEN_HEIGHT, 4):
        pygame.draw.line(surf, (0,0,0), (0,y), (SCREEN_WIDTH,y))


# ── Main Menu ─────────────────────────────────────────────────────────────────
class MainMenu:
    def __init__(self):
        cx = SCREEN_WIDTH//2
        self.play_btn = Button(pygame.Rect(cx-200, 460, 400, 64), "▶  PLAY",  color=(30,100,60))
        self.quit_btn = Button(pygame.Rect(cx-200, 550, 400, 64), "✕  QUIT",  color=(100,30,30))

    def handle(self, event):
        if self.play_btn.clicked(event): return "language_select"
        if self.quit_btn.clicked(event): return "quit"
        return None

    def draw(self, surf):
        _bg(surf)
        draw_text_centered(surf, "BALDI'S CODING BASICS",  font_title,  C_YELLOW,  180)
        draw_text_centered(surf, "Can you answer all the questions?", font_medium, C_GREY, 290)
        draw_text_centered(surf, "Find the computers — survive.", font_small, (120,130,160), 335)
        self.play_btn.draw(surf)
        self.quit_btn.draw(surf)
        draw_text_centered(surf, "F3 = open hitbox editor", font_hud, (60,70,100), SCREEN_HEIGHT-36)


# ── Language Select ───────────────────────────────────────────────────────────
class LanguageSelect:
    COLORS = {
        "Python":  (40,  80, 160),
        "Ruby":    (140, 30,  60),
        "Arduino": (30, 100,  80),
    }
    DESC = {
        "Python":  "Variables, loops, functions, OOP and more",
        "Ruby":    "Blocks, symbols, metaprogramming",
        "Arduino": "setup/loop, GPIO, PWM, interrupts",
    }

    def __init__(self):
        self.selected = None
        cx = SCREEN_WIDTH // 2
        bw, bh = 340, 90
        gap = 30
        total = len(LANGUAGES) * (bh+gap) - gap
        start_y = SCREEN_HEIGHT//2 - total//2
        self._buttons = {}
        for i, lang in enumerate(LANGUAGES):
            col = self.COLORS[lang]
            r   = pygame.Rect(cx - bw//2, start_y + i*(bh+gap), bw, bh)
            self._buttons[lang] = Button(r, lang, color=col)
        self.back_btn = Button(pygame.Rect(40, SCREEN_HEIGHT-80, 180, 50),
                               "← Back", color=(40,40,70))

    def handle(self, event):
        for lang, btn in self._buttons.items():
            if btn.clicked(event):
                self.selected = lang
                return ("difficulty_select", lang)
        if self.back_btn.clicked(event):
            return ("menu", None)
        return None

    def draw(self, surf):
        _bg(surf)
        draw_text_centered(surf, "SELECT LANGUAGE", font_large, C_YELLOW, 100)
        mx, my = pygame.mouse.get_pos()
        for lang, btn in self._buttons.items():
            btn.draw(surf)
            if btn.rect.collidepoint(mx, my):
                desc = self.DESC[lang]
                t = font_small.render(desc, True, C_GREY)
                surf.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2,
                               btn.rect.bottom + 8))
        self.back_btn.draw(surf)


# ── Difficulty Select ─────────────────────────────────────────────────────────
class DifficultySelect:
    COLORS = {
        "Beginner":    (30, 100, 50),
        "Medium":      (140, 100, 20),
        "Chase Level": (140, 20,  20),
    }
    DESC = {
        "Beginner":    "Easy questions, forgiving scoring, slower enemies",
        "Medium":      "Balanced challenge, standard scoring",
        "Chase Level": "Hard questions, harsh penalties, fast enemies",
    }

    def __init__(self, language="Python"):
        self.language = language
        cx = SCREEN_WIDTH // 2
        bw, bh = 380, 90
        gap = 30
        total = len(DIFFICULTIES) * (bh+gap) - gap
        start_y = SCREEN_HEIGHT//2 - total//2
        self._buttons = {}
        for i, diff in enumerate(DIFFICULTIES):
            col = self.COLORS[diff]
            r   = pygame.Rect(cx - bw//2, start_y + i*(bh+gap), bw, bh)
            col_cfg = DIFFICULTY[diff]["label_color"]
            self._buttons[diff] = Button(r, diff, color=col, text_color=col_cfg)
        self.back_btn = Button(pygame.Rect(40, SCREEN_HEIGHT-80, 180, 50),
                               "← Back", color=(40,40,70))

    def handle(self, event):
        for diff, btn in self._buttons.items():
            if btn.clicked(event):
                return ("playing", diff)
        if self.back_btn.clicked(event):
            return ("language_select", None)
        return None

    def draw(self, surf):
        _bg(surf)
        draw_text_centered(surf, "SELECT DIFFICULTY", font_large, C_YELLOW, 100)
        draw_text_centered(surf, f"Language: {self.language}", font_medium,
                           C_BLUE, 160)
        mx, my = pygame.mouse.get_pos()
        for diff, btn in self._buttons.items():
            btn.draw(surf)
            if btn.rect.collidepoint(mx, my):
                t = font_small.render(self.DESC[diff], True, C_GREY)
                surf.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2,
                               btn.rect.bottom + 8))
        self.back_btn.draw(surf)


# ── Pause Menu ────────────────────────────────────────────────────────────────
class PauseMenu:
    def __init__(self):
        cx = SCREEN_WIDTH//2
        self.resume_btn = Button(pygame.Rect(cx-200, 360, 400, 60), "▶  Resume",   color=(30,80,50))
        self.menu_btn   = Button(pygame.Rect(cx-200, 440, 400, 60), "⌂  Main Menu", color=(40,40,80))
        self.quit_btn   = Button(pygame.Rect(cx-200, 520, 400, 60), "✕  Quit",      color=(100,30,30))

    def handle(self, event):
        if self.resume_btn.clicked(event): return "playing"
        if self.menu_btn.clicked(event):   return "menu"
        if self.quit_btn.clicked(event):   return "quit"
        return None

    def draw(self, surf):
        dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim.fill((0,0,0,160)); surf.blit(dim,(0,0))
        draw_text_centered(surf, "PAUSED", font_large, C_YELLOW, 260)
        self.resume_btn.draw(surf)
        self.menu_btn.draw(surf)
        self.quit_btn.draw(surf)


# ── Victory Screen ────────────────────────────────────────────────────────────
class VictoryScreen:
    def __init__(self):
        cx = SCREEN_WIDTH//2
        self.menu_btn    = Button(pygame.Rect(cx-220, 520, 200, 60), "⌂ Menu",   color=(30,60,100))
        self.restart_btn = Button(pygame.Rect(cx+20,  520, 200, 60), "↺ Retry",  color=(30,100,60))

    def handle(self, event):
        if self.menu_btn.clicked(event):    return "menu"
        if self.restart_btn.clicked(event): return "playing"
        return None

    def draw(self, surf, score, lang, diff):
        _bg(surf)
        draw_text_centered(surf, "YOU WIN!",                font_title,  C_GREEN,  180)
        draw_text_centered(surf, "All computers answered!", font_medium, C_WHITE,  295)
        draw_text_centered(surf, f"Final Score:  {score}",  font_large,  C_YELLOW, 360)
        draw_text_centered(surf, f"{lang}  |  {diff}",      font_small,  C_GREY,   430)
        self.menu_btn.draw(surf)
        self.restart_btn.draw(surf)


# ── Game Over Screen ──────────────────────────────────────────────────────────
class GameOverScreen:
    def __init__(self):
        cx = SCREEN_WIDTH//2
        self.menu_btn    = Button(pygame.Rect(cx-220, 520, 200, 60), "⌂ Menu",  color=(30,60,100))
        self.restart_btn = Button(pygame.Rect(cx+20,  520, 200, 60), "↺ Retry", color=(100,30,30))

    def handle(self, event):
        if self.menu_btn.clicked(event):    return "menu"
        if self.restart_btn.clicked(event): return "playing"
        return None

    def draw(self, surf, score, reason=""):
        _bg(surf)
        draw_text_centered(surf, "GAME OVER",         font_title,  C_RED,    180)
        if reason:
            draw_text_centered(surf, reason,          font_medium, C_WHITE,  300)
        draw_text_centered(surf, f"Score: {score}",   font_large,  C_YELLOW, 370)
        self.menu_btn.draw(surf)
        self.restart_btn.draw(surf)