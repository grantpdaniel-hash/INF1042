import pygame
import math
import random

CATCH_DIST    = 48
SIGHT_DIST    = 600
PENALTY       = -75
RESPAWN_FLASH = 1800
REACH_DIST    = 50


# ── Line-segment vs AABB intersection ────────────────────────────────────────
def _segment_hits_rect(ax, ay, bx, by, rect: pygame.Rect) -> bool:
    """
    Returns True if the line segment A→B intersects the pygame.Rect.
    Uses the Liang-Barsky algorithm.
    """
    dx = bx - ax
    dy = by - ay
    # rect edges
    rx, ry, rw, rh = rect.x, rect.y, rect.width, rect.height

    p = [-dx, dx, -dy, dy]
    q = [ax - rx, rx + rw - ax, ay - ry, ry + rh - ay]

    t0, t1 = 0.0, 1.0
    for pi, qi in zip(p, q):
        if pi == 0:
            if qi < 0:
                return False   # parallel and outside
        elif pi < 0:
            t0 = max(t0, qi / pi)
        else:
            t1 = min(t1, qi / pi)
        if t0 > t1:
            return False
    return True


def _has_clear_line(ax, ay, bx, by, walls) -> bool:
    """True if no wall rect blocks the segment from (ax,ay) to (bx,by)."""
    for w in walls:
        if _segment_hits_rect(ax, ay, bx, by, w):
            return False
    return True


class Baldi:
    """
    Patrol mode  : walks the checkpoint graph, picking random *visible*
                   neighbours at each junction (line-of-sight checked).
    Chase mode   : player within SIGHT_DIST AND has clear LOS → direct chase.
    Returns to patrol after losing sight for 3 s.
    """

    COLOR        = (220,  60,  60)
    ALERT_COLOR  = (255, 200,   0)
    PATROL_COLOR = (255, 140,   0)
    SIZE         = 36

    def __init__(self, speed: float = 2.5):
        self.x      = 0.0
        self.y      = 0.0
        self.speed  = speed
        self.active  = False
        self.spawned = False
        self.alerted = False
        self.alert_cooldown   = 0
        self.invincible_timer = 0
        self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)

        self._points: list[tuple[float, float]] = []
        self._adj:    dict[int, list[int]]       = {}
        self._current_idx: int = 0
        self._target_idx:  int = -1

        # Wall list updated each frame from main so LOS checks work
        self._walls: list[pygame.Rect] = []

        self._anger   = 0
        self.on_catch = None

    # ── Public API ────────────────────────────────────────────────────────────

    def set_checkpoint_graph(self, points, adjacency):
        self._points = [(float(x), float(y)) for x, y in points]
        self._adj    = adjacency
        if self._points:
            self._current_idx = 0
            self._pick_next(from_idx=0)

    def first_wrong_answer(self, spawn_x: float, spawn_y: float):
        if not self.spawned:
            self.teleport(spawn_x, spawn_y)
            self._current_idx = self._nearest_checkpoint(spawn_x, spawn_y)
            self.spawned = True
        self.active = True
        self._anger_up()
        self._pick_next(from_idx=self._current_idx)

    def wrong_answer(self):
        self._anger_up()

    def teleport(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def player_respawned(self):
        self.alerted        = False
        self.alert_cooldown = 0
        self.invincible_timer = RESPAWN_FLASH
        self._pick_next(from_idx=self._current_idx)

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt: int, player_rect: pygame.Rect, walls: list):
        if not self.active:
            return
        # Store walls so _pick_next can do LOS checks
        self._walls = walls

        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            return

        bx = self.x + self.SIZE / 2
        by = self.y + self.SIZE / 2
        px, py = float(player_rect.centerx), float(player_rect.centery)
        dist_player = math.hypot(px - bx, py - by)

        # ── Sight check (player needs clear LOS too) ──────────────────────────
        player_visible = (dist_player <= SIGHT_DIST and
                          _has_clear_line(bx, by, px, py, walls))

        if player_visible:
            self.alerted        = True
            self.alert_cooldown = 3000
        elif self.alerted:
            self.alert_cooldown -= dt
            if self.alert_cooldown <= 0:
                self.alerted = False
                self._current_idx = self._nearest_checkpoint(self.x, self.y)
                self._pick_next(from_idx=self._current_idx)

        # ── Decide move target ────────────────────────────────────────────────
        if self.alerted:
            tx, ty = px, py
        else:
            if self._target_idx < 0 or not self._points:
                # Try to pick again — maybe a wall cleared
                self._pick_next(from_idx=self._current_idx)
                return
            cp = self._points[self._target_idx]
            tx = cp[0] - self.SIZE / 2
            ty = cp[1] - self.SIZE / 2

            # Reached checkpoint?
            if math.hypot(cp[0] - bx, cp[1] - by) < REACH_DIST:
                self._current_idx = self._target_idx
                self._pick_next(from_idx=self._current_idx)
                return

            # Mid-path LOS recheck — if the target checkpoint got blocked
            # (e.g. Baldi cut a corner), pick another
            if not _has_clear_line(bx, by, cp[0], cp[1], walls):
                self._pick_next(from_idx=self._current_idx)
                return

        # ── Move ──────────────────────────────────────────────────────────────
        dx = tx - self.x
        dy = ty - self.y
        d  = math.hypot(dx, dy)
        if d < 1:
            return

        step = self.speed * (dt / 16.67)
        nx   = dx / d * step
        ny   = dy / d * step
        old_x, old_y = self.x, self.y

        self.x += nx
        self.rect.x = int(self.x)
        for w in walls:
            if self.rect.colliderect(w):
                self.x = old_x
                self.rect.x = int(self.x)
                if not self.alerted:
                    self._pick_next(from_idx=self._current_idx)
                break

        self.y += ny
        self.rect.y = int(self.y)
        for w in walls:
            if self.rect.colliderect(w):
                self.y = old_y
                self.rect.y = int(self.y)
                if not self.alerted:
                    self._pick_next(from_idx=self._current_idx)
                break

        # ── Catch check ───────────────────────────────────────────────────────
        if self.alerted and dist_player <= CATCH_DIST:
            if self.on_catch:
                self.on_catch(PENALTY)

    # ── Draw ──────────────────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface, camera):
        if not self.spawned:
            return

        # Patrol path edges
        if not self.alerted and len(self._points) > 1:
            drawn = set()
            for a, neighbours in self._adj.items():
                for b in neighbours:
                    key = (min(a, b), max(a, b))
                    if key in drawn:
                        continue
                    drawn.add(key)
                    ax, ay = camera.world_to_screen(*self._points[a])
                    bx, by = camera.world_to_screen(*self._points[b])
                    pygame.draw.line(screen, (255, 140, 0),
                                     (int(ax), int(ay)), (int(bx), int(by)), 1)

        # Checkpoint dots
        for i, (cx, cy) in enumerate(self._points):
            sx, sy     = camera.world_to_screen(cx, cy)
            is_target  = (i == self._target_idx)
            is_current = (i == self._current_idx)
            col    = (255, 255, 80) if is_target else (255, 140, 0)
            radius = 8 if (is_target or is_current) else 5
            pygame.draw.circle(screen, col, (int(sx), int(sy)), radius)
            try:
                from ui import font_hud
                t = font_hud.render(str(i), True, col)
                screen.blit(t, (int(sx) + 8, int(sy) - 8))
            except Exception:
                pass

        # Baldi body
        sr  = camera.apply_rect(self.rect)
        col = self.ALERT_COLOR if self.alerted else self.PATROL_COLOR
        pygame.draw.rect(screen, col, sr, border_radius=6)
        pygame.draw.rect(screen, (255, 255, 255), sr, 2, border_radius=6)

        ew = max(4, sr.width  // 6)
        eh = max(4, sr.height // 6)
        lx = sr.x + sr.width  // 3 - ew // 2
        rx = sr.x + sr.width  * 2 // 3 - ew // 2
        ey = sr.y + sr.height // 3
        pygame.draw.ellipse(screen, (10, 10, 10), (lx, ey, ew, eh))
        pygame.draw.ellipse(screen, (10, 10, 10), (rx, ey, ew, eh))

        if self.alerted:
            brow_y = ey - max(3, sr.height // 8)
            pygame.draw.line(screen, (10, 10, 10),
                             (lx, brow_y + 3), (lx + ew, brow_y), 2)
            pygame.draw.line(screen, (10, 10, 10),
                             (rx, brow_y), (rx + ew, brow_y + 3), 2)
            if self.invincible_timer <= 0:
                try:
                    from ui import font_hud, C_YELLOW
                    t = font_hud.render("!", True, C_YELLOW)
                    screen.blit(t, (sr.centerx - t.get_width() // 2,
                                     sr.y - t.get_height() - 4))
                except Exception:
                    pass

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _pick_next(self, from_idx: int):
        """
        Choose a random connected neighbour that has a clear line of sight
        from Baldi's current position.  If none are visible, set target to -1
        (Baldi waits in place until a path opens).
        """
        if not self._points:
            self._target_idx = -1
            return

        bx = self.x + self.SIZE / 2
        by = self.y + self.SIZE / 2

        neighbours = self._adj.get(from_idx, [])
        visible = [
            n for n in neighbours
            if _has_clear_line(bx, by,
                               self._points[n][0],
                               self._points[n][1],
                               self._walls)
        ]

        if visible:
            self._target_idx = random.choice(visible)
        else:
            # No visible neighbours — wait; retry next frame via update()
            self._target_idx = -1

    def _nearest_checkpoint(self, wx: float, wy: float) -> int:
        if not self._points:
            return 0
        best_i, best_d = 0, float("inf")
        for i, (cx, cy) in enumerate(self._points):
            d = math.hypot(cx - wx, cy - wy)
            if d < best_d:
                best_i, best_d = i, d
        return best_i

    def _anger_up(self):
        self._anger += 1
        if self._anger > 1:
            self.speed = (self.speed
                          * (1 + 0.10 * self._anger)
                          / (1 + 0.10 * (self._anger - 1)))