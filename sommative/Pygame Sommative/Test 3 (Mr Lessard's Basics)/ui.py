import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.font.init()
font_title  = pygame.font.SysFont("consolas", 72, bold=True)
font_large  = pygame.font.SysFont("consolas", 42, bold=True)
font_medium = pygame.font.SysFont("consolas", 28)
font_small  = pygame.font.SysFont("consolas", 22)
font_hud    = pygame.font.SysFont("consolas", 20)
font_sm     = pygame.font.SysFont("consolas", 16)

# ── Colour palette ────────────────────────────────────────────────────────────
C_BG      = (12,  14,  20)
C_PANEL   = (20,  24,  36)
C_BORDER  = (60,  80, 140)
C_WHITE   = (230, 230, 240)
C_YELLOW  = (255, 220,  50)
C_GREEN   = ( 60, 220, 100)
C_RED     = (255,  60,  60)
C_BLUE    = ( 60, 160, 255)
C_PURPLE  = (180,  60, 255)
C_GREY    = (100, 110, 130)

def draw_text_centered(surf, text, font, color, y):
    t = font.render(text, True, color)
    surf.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2, y))

def draw_text(surf, text, font, color, x, y):
    surf.blit(font.render(text, True, color), (x, y))

# ── Generic button ────────────────────────────────────────────────────────────
class Button:
    def __init__(self, rect, label, color=C_BLUE, text_color=C_WHITE):
        self.rect       = pygame.Rect(rect)
        self.label      = label
        self.color      = color
        self.text_color = text_color
        self._hover     = False

    def draw(self, surf):
        mx, my = pygame.mouse.get_pos()
        self._hover = self.rect.collidepoint(mx, my)
        col = tuple(min(255, c+40) for c in self.color) if self._hover else self.color
        pygame.draw.rect(surf, col, self.rect, border_radius=8)
        pygame.draw.rect(surf, C_WHITE, self.rect, 2, border_radius=8)
        lbl = font_medium.render(self.label, True, self.text_color)
        surf.blit(lbl, (self.rect.centerx - lbl.get_width()//2,
                         self.rect.centery - lbl.get_height()//2))

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))

# ── Feedback flash  (correct / wrong) ────────────────────────────────────────
class FeedbackFlash:
    def __init__(self):
        self.text    = ""
        self.color   = C_WHITE
        self.timer   = 0
        self.delta   = 0

    def show(self, text, color, ms=1200):
        self.text  = text
        self.color = color
        self.timer = ms

    def update(self, dt):
        if self.timer > 0:
            self.timer -= dt

    def draw(self, surf):
        if self.timer <= 0: return
        alpha = min(255, int(self.timer / 300 * 255))
        t = font_large.render(self.text, True, self.color)
        t.set_alpha(alpha)
        surf.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2,
                       SCREEN_HEIGHT//2 - 180))

# ── Question overlay ──────────────────────────────────────────────────────────
class QuestionOverlay:
    """Blocking multiple-choice question panel."""

    PANEL_W = 900
    PANEL_H = 420

    def __init__(self):
        self.active    = False
        self.question  = ""
        self.choices   = []
        self.answer    = 0
        self.selected  = -1
        self.confirmed = False   # True once player clicks an answer
        self.correct   = False
        self._buttons  = []
        self._panel_rect = pygame.Rect(
            SCREEN_WIDTH//2 - self.PANEL_W//2,
            SCREEN_HEIGHT//2 - self.PANEL_H//2,
            self.PANEL_W, self.PANEL_H)

    def open(self, question: dict):
        self.question  = question["q"]
        self.choices   = question["choices"]
        self.answer    = question["answer"]
        self.selected  = -1
        self.confirmed = False
        self.correct   = False
        self.active    = True
        self._build_buttons()

    def _build_buttons(self):
        self._buttons = []
        bw, bh = self.PANEL_W - 60, 52
        bx = self._panel_rect.x + 30
        by = self._panel_rect.y + 160
        for i, ch in enumerate(self.choices):
            self._buttons.append(
                Button(pygame.Rect(bx, by + i*(bh+10), bw, bh),
                       f"{chr(65+i)}.  {ch}", color=(30,40,70)))

    def handle_event(self, event):
        if not self.active or self.confirmed:
            return None   # no result yet
        for i, btn in enumerate(self._buttons):
            if btn.clicked(event):
                self.selected  = i
                self.confirmed = True
                self.correct   = (i == self.answer)
                return "correct" if self.correct else "wrong"
        return None

    def draw(self, surf):
        if not self.active: return

        # Dim background
        dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim.fill((0,0,0,160))
        surf.blit(dim, (0,0))

        # Panel
        pygame.draw.rect(surf, C_PANEL,  self._panel_rect, border_radius=12)
        pygame.draw.rect(surf, C_BORDER, self._panel_rect, 3, border_radius=12)

        # Question text (word-wrap at ~80 chars)
        words = self.question.split()
        lines = []; line = ""
        for w in words:
            if len(line) + len(w) + 1 > 62:
                lines.append(line); line = w
            else:
                line = (line + " " + w).strip()
        lines.append(line)

        qy = self._panel_rect.y + 24
        for ln in lines:
            t = font_medium.render(ln, True, C_YELLOW)
            surf.blit(t, (self._panel_rect.x + 30, qy))
            qy += 34

        # Choices
        for i, btn in enumerate(self._buttons):
            if self.confirmed:
                if i == self.answer:
                    btn.color = (20, 80, 30)
                elif i == self.selected:
                    btn.color = (80, 20, 20)
            btn.draw(surf)

        # After confirmed — show result label
        if self.confirmed:
            label = "✓ Correct!" if self.correct else "✗ Wrong"
            col   = C_GREEN if self.correct else C_RED
            t = font_large.render(label, True, col)
            surf.blit(t, (self._panel_rect.centerx - t.get_width()//2,
                           self._panel_rect.bottom + 18))

# ── HUD bar ───────────────────────────────────────────────────────────────────
def draw_hud(surf, score, lang, diff, completed, total, diff_cfg):
    bar = pygame.Surface((SCREEN_WIDTH, 42), pygame.SRCALPHA)
    bar.fill((10, 12, 20, 210))
    surf.blit(bar, (0, 0))
    col = diff_cfg["label_color"]
    items = [
        (f"Score: {score}",             C_YELLOW),
        (f"Lang: {lang}",               C_BLUE),
        (f"Difficulty: {diff}",         col),
        (f"Computers: {completed}/{total}", C_GREEN),
    ]
    x = 12
    for text, c in items:
        t = font_hud.render(text, True, c)
        surf.blit(t, (x, 10))
        x += t.get_width() + 40

# ── Interaction prompt ────────────────────────────────────────────────────────
def draw_interact_prompt(surf):
    t = font_small.render("[ E ]  Interact with computer", True, C_GREEN)
    surf.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2, SCREEN_HEIGHT - 60))