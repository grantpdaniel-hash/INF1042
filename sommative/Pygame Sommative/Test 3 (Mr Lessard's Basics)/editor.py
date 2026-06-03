import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_KEY, HB_COLORS

pygame.font.init()
_font      = pygame.font.SysFont("consolas", 18)
_font_bold = pygame.font.SysFont("consolas", 18, bold=True)
_font_sm   = pygame.font.SysFont("consolas", 14)

# baldi_checkpoints is click-to-place, not drag
HB_TYPES_DRAG  = ["walls", "doors", "computers", "spawns", "monster_spawns"]
HB_TYPES_CLICK = ["baldi_checkpoints"]
HB_TYPES       = HB_TYPES_DRAG + HB_TYPES_CLICK

PANEL_W = 340
PANEL_X = SCREEN_WIDTH - PANEL_W

CP_RADIUS = 10   # display radius for checkpoint dots

_dim_surf      = None
_dim_surf_size = (0, 0)
_fill_cache    = {}

def _get_dim(w, h):
    global _dim_surf, _dim_surf_size
    if (w, h) != _dim_surf_size:
        _dim_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        _dim_surf.fill((0, 0, 0, 70))
        _dim_surf_size = (w, h)
    return _dim_surf

def _get_fill(w, h, col, alpha):
    key = (w, h, *col, alpha)
    if key not in _fill_cache:
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill((*col, alpha))
        _fill_cache[key] = s
        if len(_fill_cache) > 512:
            _fill_cache.pop(next(iter(_fill_cache)))
    return _fill_cache[key]


class HitboxEditor:
    def __init__(self, map_loader, camera):
        self.ml         = map_loader
        self.camera     = camera
        self.hb_type    = "walls"
        self.draw_start = None
        self.sel_idx    = -1
        self.sel_type   = "walls"

        # Connection drawing state:
        # when hb_type == "baldi_checkpoints" and user RMB-clicks two dots
        self._conn_a: int = -1   # first selected checkpoint index for a new connection

    # ── Raw entry helpers ─────────────────────────────────────────────────────
    def _entries(self, htype):
        return self.ml.data[MAP_KEY].get(htype, [])

    def _checkpoints(self):
        return self._entries("baldi_checkpoints")

    def _connections(self):
        return self.ml.data[MAP_KEY].setdefault("baldi_connections", [])

    def _to_rect(self, e):
        if isinstance(e, dict):
            return pygame.Rect(e["x"], e["y"], e.get("w", 64), e.get("h", 64))
        return pygame.Rect(e[0], e[1], e[2], e[3])

    # ── Hit-test a checkpoint dot ─────────────────────────────────────────────
    def _cp_at_screen(self, mx, my):
        """Return index of checkpoint whose dot is under screen pos, or -1."""
        for i, cp in enumerate(self._checkpoints()):
            sx, sy = self.camera.world_to_screen(cp["x"], cp["y"])
            if (mx - sx)**2 + (my - sy)**2 <= (CP_RADIUS + 4)**2:
                return i
        return -1

    # ── Events ────────────────────────────────────────────────────────────────
    def handle_event(self, event, mx, my):
        cam = self.camera
        mw  = self.ml.map_w or 99999
        mh  = self.ml.map_h or 99999

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                idx = (HB_TYPES.index(self.hb_type) + 1) % len(HB_TYPES)
                self.hb_type = HB_TYPES[idx]
                self.sel_idx  = -1
                self._conn_a  = -1

            if event.key == pygame.K_DELETE:
                if self.hb_type == "baldi_checkpoints" and self.sel_idx >= 0:
                    # Remove checkpoint and all connections referencing it
                    cps = self._checkpoints()
                    idx = self.sel_idx
                    if 0 <= idx < len(cps):
                        cps.pop(idx)
                        # Rebuild connections: remove any using idx, shift higher indices
                        new_conns = []
                        for a, b in self._connections():
                            if a == idx or b == idx:
                                continue
                            a2 = a - (1 if a > idx else 0)
                            b2 = b - (1 if b > idx else 0)
                            new_conns.append([a2, b2])
                        self.ml.data[MAP_KEY]["baldi_connections"] = new_conns
                        self.sel_idx = -1
                        self.ml.rebuild_chunks()
                elif self.sel_idx >= 0:
                    lst = self._entries(self.sel_type)
                    if 0 <= self.sel_idx < len(lst):
                        lst.pop(self.sel_idx)
                        self.sel_idx = min(self.sel_idx, len(lst) - 1)
                        self.ml.rebuild_chunks()

            # Delete a selected connection with Backspace
            if event.key == pygame.K_BACKSPACE and self.hb_type == "baldi_checkpoints":
                if self.sel_idx >= 0 and self.sel_type == "baldi_connections":
                    conns = self._connections()
                    if 0 <= self.sel_idx < len(conns):
                        conns.pop(self.sel_idx)
                        self.sel_idx = -1

        if event.type == pygame.MOUSEWHEEL and mx < PANEL_X:
            zoom = cam.zoom * (1.1 if event.y > 0 else 0.9)
            cam.zoom = max(0.05, min(zoom, 6.0))
            wx, wy = cam.screen_to_world(mx, my)
            cam.x = wx - mx / cam.zoom
            cam.y = wy - my / cam.zoom

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mx >= PANEL_X:
                if event.button == 1:
                    self._panel_click(mx, my)
                return

            # ── Left click ────────────────────────────────────────────────────
            if event.button == 1:
                if self.hb_type == "baldi_checkpoints":
                    # Place a new checkpoint dot at world position
                    wx_w, wy_w = cam.screen_to_world(mx, my)
                    cps = self._checkpoints()
                    cps.append({"x": int(wx_w), "y": int(wy_w), "id": len(cps)})
                    self.sel_idx  = len(cps) - 1
                    self.sel_type = "baldi_checkpoints"
                    self._conn_a  = -1
                    self.ml.rebuild_chunks()
                else:
                    wx_w, wy_w = cam.screen_to_world(mx, my)
                    self.draw_start = (wx_w, wy_w)
                    self.sel_idx = -1

            # ── Right click ───────────────────────────────────────────────────
            if event.button == 3:
                if self.hb_type == "baldi_checkpoints":
                    hit = self._cp_at_screen(mx, my)
                    if hit >= 0:
                        if self._conn_a < 0:
                            # First endpoint
                            self._conn_a  = hit
                            self.sel_idx  = hit
                            self.sel_type = "baldi_checkpoints"
                        else:
                            # Second endpoint — create connection if not duplicate
                            a, b = self._conn_a, hit
                            if a != b:
                                conns = self._connections()
                                pair  = sorted([a, b])
                                if pair not in [sorted(c) for c in conns]:
                                    conns.append(pair)
                            self._conn_a = -1
                    else:
                        self._conn_a = -1
                else:
                    self._select_at(cam.screen_to_world(mx, my))

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.hb_type not in HB_TYPES_CLICK and self.draw_start:
                wx_e, wy_e = cam.screen_to_world(mx, my)
                x0 = max(0, min(self.draw_start[0], mw))
                y0 = max(0, min(self.draw_start[1], mh))
                x1 = max(0, min(wx_e, mw))
                y1 = max(0, min(wy_e, mh))
                x0, x1 = min(x0, x1), max(x0, x1)
                y0, y1 = min(y0, y1), max(y0, y1)
                if x1 - x0 > 4 and y1 - y0 > 4:
                    self._add_entry(int(x0), int(y0), int(x1 - x0), int(y1 - y0))
                    self.ml.rebuild_chunks()
                self.draw_start = None

    def _add_entry(self, x, y, w, h):
        lst = self.ml.data[MAP_KEY].setdefault(self.hb_type, [])
        if self.hb_type == "computers":
            lst.append({"x": x, "y": y, "w": w, "h": h, "id": len(lst), "completed": False})
        elif self.hb_type == "spawns":
            lst.append({"x": x, "y": y, "w": w, "h": h, "spawn_id": len(lst)})
        elif self.hb_type == "monster_spawns":
            lst.append({"x": x, "y": y, "w": w, "h": h, "enemy_type": "baldi"})
        else:
            lst.append([x, y, w, h])

    def _select_at(self, world_pos):
        wx, wy = world_pos
        self.sel_idx = -1
        for htype in HB_TYPES_DRAG:
            for i, e in enumerate(self._entries(htype)):
                if self._to_rect(e).collidepoint(wx, wy):
                    self.sel_idx  = i
                    self.sel_type = htype
                    self.hb_type  = htype
                    return

    def _panel_click(self, mx, my):
        by = 90
        for htype in HB_TYPES:
            r = pygame.Rect(PANEL_X + 8, by, PANEL_W - 16, 34)
            if r.collidepoint(mx, my):
                self.hb_type = htype
                self.sel_idx  = -1
                self._conn_a  = -1
                return
            by += 40

    # ── Draw ──────────────────────────────────────────────────────────────────
    def draw(self, screen, mx, my):
        vr = self.camera.visible_world_rect()

        screen.blit(_get_dim(PANEL_X, SCREEN_HEIGHT), (0, 0))

        map_r = pygame.Rect(0, 0, self.ml.map_w or 1920, self.ml.map_h or 1080)
        pygame.draw.rect(screen, (255, 200, 50), self.camera.apply_rect(map_r), 2)

        # Draw regular hitbox types
        for htype in HB_TYPES_DRAG:
            col = HB_COLORS[htype]
            for i, e in enumerate(self._entries(htype)):
                er = self._to_rect(e)
                if not er.colliderect(vr): continue
                sr  = self.camera.apply_rect(er)
                sel = (htype == self.sel_type and i == self.sel_idx)
                screen.blit(_get_fill(max(1, sr.width), max(1, sr.height),
                             col, 80 if sel else 30), (sr.x, sr.y))
                pygame.draw.rect(screen, (255, 255, 80) if sel else col, sr, 2)
                screen.blit(_font_sm.render(str(i), True,
                             (255, 255, 80) if sel else col), (sr.x + 3, sr.y + 2))

        # Draw checkpoint connections
        cp_col = HB_COLORS["baldi_checkpoints"]
        cps    = self._checkpoints()
        conns  = self._connections()
        for conn in conns:
            if len(conn) == 2:
                a, b = conn
                if 0 <= a < len(cps) and 0 <= b < len(cps):
                    ax, ay = self.camera.world_to_screen(cps[a]["x"], cps[a]["y"])
                    bx, by_ = self.camera.world_to_screen(cps[b]["x"], cps[b]["y"])
                    pygame.draw.line(screen, cp_col,
                                     (int(ax), int(ay)), (int(bx), int(by_)), 2)

        # Draw checkpoint dots
        for i, cp in enumerate(cps):
            sx, sy = self.camera.world_to_screen(cp["x"], cp["y"])
            sel    = (self.sel_type == "baldi_checkpoints" and i == self.sel_idx)
            is_conn_a = (i == self._conn_a)
            dot_col   = (255, 255, 80) if sel else ((0, 255, 255) if is_conn_a else cp_col)
            pygame.draw.circle(screen, dot_col, (int(sx), int(sy)), CP_RADIUS)
            pygame.draw.circle(screen, (255, 255, 255), (int(sx), int(sy)), CP_RADIUS, 1)
            screen.blit(_font_sm.render(str(i), True, (10, 10, 10)),
                        (int(sx) - 4, int(sy) - 7))

        # Drag preview (non-click types)
        if self.draw_start and self.hb_type not in HB_TYPES_CLICK:
            wx_e, wy_e = self.camera.screen_to_world(mx, my)
            mw = self.ml.map_w or 99999; mh = self.ml.map_h or 99999
            x0 = max(0, min(self.draw_start[0], mw))
            y0 = max(0, min(self.draw_start[1], mh))
            x1 = max(0, min(wx_e, mw))
            y1 = max(0, min(wy_e, mh))
            x0, x1 = min(x0, x1), max(x0, x1)
            y0, y1 = min(y0, y1), max(y0, y1)
            sp  = self.camera.apply_rect(
                pygame.Rect(int(x0), int(y0), int(x1 - x0), int(y1 - y0)))
            col = HB_COLORS[self.hb_type]
            screen.blit(_get_fill(max(1, sp.width), max(1, sp.height), col, 70),
                        (sp.x, sp.y))
            pygame.draw.rect(screen, col, sp, 2)
            screen.blit(_font_sm.render(f"{int(x1-x0)}x{int(y1-y0)}", True, col),
                        (sp.x + 4, sp.y + 4))

        # Pending connection line preview
        if self._conn_a >= 0 and self._conn_a < len(cps):
            ax, ay = self.camera.world_to_screen(
                cps[self._conn_a]["x"], cps[self._conn_a]["y"])
            pygame.draw.line(screen, (0, 255, 255),
                             (int(ax), int(ay)), (mx, my), 1)

        self._draw_panel(screen, mx, my)

    def _draw_panel(self, screen, mx, my):
        surf = pygame.Surface((PANEL_W, SCREEN_HEIGHT), pygame.SRCALPHA)
        surf.fill((8, 10, 16, 235))
        screen.blit(surf, (PANEL_X, 0))

        y = 10
        screen.blit(_font_bold.render("── HITBOX EDITOR ──", True, (255, 180, 50)),
                    (PANEL_X + 8, y)); y += 28

        counts = {h: len(self._entries(h)) for h in HB_TYPES_DRAG}
        screen.blit(_font.render(
            f"W:{counts['walls']} D:{counts['doors']} C:{counts['computers']} "
            f"S:{counts['spawns']} M:{counts['monster_spawns']}",
            True, (160, 160, 180)), (PANEL_X + 8, y)); y += 16
        screen.blit(_font.render(
            f"CP:{len(self._checkpoints())}  Conn:{len(self._connections())}",
            True, (255, 140, 0)), (PANEL_X + 8, y)); y += 22

        for htype in HB_TYPES:
            col    = HB_COLORS[htype]
            active = (self.hb_type == htype)
            r      = pygame.Rect(PANEL_X + 8, y, PANEL_W - 16, 34)
            pygame.draw.rect(screen, col if active else (20, 25, 38), r, border_radius=4)
            pygame.draw.rect(screen, col, r, 2, border_radius=4)
            lbl = _font.render(htype.upper(), True, (10, 10, 10) if active else col)
            screen.blit(lbl, (r.centerx - lbl.get_width() // 2,
                               r.centery - lbl.get_height() // 2))
            y += 40

        y += 6
        if self.hb_type == "baldi_checkpoints":
            hints = [
                "LMB = place checkpoint dot",
                "RMB dot 1 then dot 2 = connect",
                "Cyan dot = waiting for 2nd",
                "DEL = delete selected cp",
                "BACKSPACE = delete selected conn",
                "Tab=cycle  Ctrl+S=save",
            ]
        else:
            hints = [
                "LMB drag=draw  RMB=select",
                "DEL=delete  Tab=cycle type",
                "Scroll=zoom  RMB drag=pan",
                "Ctrl+S=save  F3=game",
            ]
        for line in hints:
            screen.blit(_font_sm.render(line, True, (120, 135, 155)),
                        (PANEL_X + 8, y)); y += 16
        y += 8

        # Selected info
        if self.sel_idx >= 0:
            if self.sel_type == "baldi_checkpoints":
                cps = self._checkpoints()
                if self.sel_idx < len(cps):
                    cp  = cps[self.sel_idx]
                    col = HB_COLORS["baldi_checkpoints"]
                    screen.blit(_font.render(f"CP [{self.sel_idx}]", True, (255, 255, 80)),
                                (PANEL_X + 8, y)); y += 18
                    screen.blit(_font_sm.render(f"  x:{cp['x']}  y:{cp['y']}", True, col),
                                (PANEL_X + 8, y)); y += 14
                    # Neighbours
                    nbrs = [b for a, b in self._connections() if a == self.sel_idx] + \
                           [a for a, b in self._connections() if b == self.sel_idx]
                    screen.blit(_font_sm.render(f"  connects to: {nbrs}", True, col),
                                (PANEL_X + 8, y)); y += 14
            else:
                entries = self._entries(self.sel_type)
                if self.sel_idx < len(entries):
                    e   = entries[self.sel_idx]
                    col = HB_COLORS.get(self.sel_type, (200, 200, 200))
                    screen.blit(_font.render(f"Selected [{self.sel_idx}]", True, (255, 255, 80)),
                                (PANEL_X + 8, y)); y += 20
                    if isinstance(e, dict):
                        for k, v in e.items():
                            screen.blit(_font_sm.render(f"  {k}: {v}", True, col),
                                        (PANEL_X + 8, y)); y += 14
                    else:
                        screen.blit(_font_sm.render(
                            f"  x{e[0]} y{e[1]} w{e[2]} h{e[3]}", True, col),
                            (PANEL_X + 8, y)); y += 14

        # Abbreviated checkpoint list
        if self.hb_type == "baldi_checkpoints":
            y += 6
            col = HB_COLORS["baldi_checkpoints"]
            screen.blit(_font_bold.render("CHECKPOINTS:", True, col),
                        (PANEL_X + 8, y)); y += 18
            for i, cp in enumerate(self._checkpoints()):
                sel = (self.sel_type == "baldi_checkpoints" and i == self.sel_idx)
                tc  = (255, 255, 100) if sel else (130, 140, 160)
                screen.blit(_font_sm.render(f"[{i}] ({cp['x']},{cp['y']})", True, tc),
                            (PANEL_X + 8, y)); y += 14
                if y > SCREEN_HEIGHT - 40: break
            y += 4
            screen.blit(_font_bold.render("CONNECTIONS:", True, col),
                        (PANEL_X + 8, y)); y += 18
            for i, conn in enumerate(self._connections()):
                screen.blit(_font_sm.render(f"  {conn[0]} ↔ {conn[1]}", True, (130, 140, 160)),
                            (PANEL_X + 8, y)); y += 14
                if y > SCREEN_HEIGHT - 20: break
        else:
            y += 6
            screen.blit(_font_bold.render(f"{self.hb_type.upper()}:",
                        True, HB_COLORS.get(self.hb_type, (200,200,200))),
                        (PANEL_X + 8, y)); y += 18
            for i, e in enumerate(self._entries(self.hb_type)):
                sel = (self.hb_type == self.sel_type and i == self.sel_idx)
                tc  = (255, 255, 100) if sel else (130, 140, 160)
                txt = (f"[{i}] x{e['x']} y{e['y']}" if isinstance(e, dict)
                       else f"[{i}] x{e[0]} y{e[1]} w{e[2]} h{e[3]}")
                screen.blit(_font_sm.render(txt, True, tc), (PANEL_X + 8, y)); y += 14
                if y > SCREEN_HEIGHT - 20: break