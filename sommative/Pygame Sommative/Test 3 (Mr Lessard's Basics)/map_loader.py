import pygame
import json
import os
from settings import (BASE_DIR, ASSET_DIR, MAP_DATA_FILE,
                      MAP_FILE, MAP_KEY, CHUNK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
from computer import Computer


class ChunkMap:
    def __init__(self):
        self._grid  = {}
        self._rects = []

    def _cells(self, x, y, w, h):
        x0 = int(x)                   // CHUNK_SIZE
        y0 = int(y)                   // CHUNK_SIZE
        x1 = max(int(x), int(x+w-1)) // CHUNK_SIZE
        y1 = max(int(y), int(y+h-1)) // CHUNK_SIZE
        for cx in range(x0, x1+1):
            for cy in range(y0, y1+1):
                yield (cx, cy)

    def rebuild(self, rects):
        self._grid  = {}
        self._rects = rects
        for i, e in enumerate(rects):
            for cell in self._cells(e[0], e[1], e[2], e[3]):
                self._grid.setdefault(cell, []).append(i)

    def query(self, x, y, w, h):
        seen = set(); out = []
        for cell in self._cells(x, y, w, h):
            for idx in self._grid.get(cell, []):
                if idx not in seen:
                    seen.add(idx)
                    out.append(self._rects[idx])
        return out

    def query_rects(self, x, y, w, h):
        return [pygame.Rect(e[0], e[1], e[2], e[3]) for e in self.query(x, y, w, h)]


class MapLoader:
    def __init__(self):
        self.image = None
        self.map_w = self.map_h = 0
        _p = os.path.join(ASSET_DIR, MAP_FILE)
        if os.path.exists(_p):
            self.image = pygame.image.load(_p).convert()
            self.map_w, self.map_h = self.image.get_size()
            print(f"[INFO] Map loaded  {self.map_w}x{self.map_h}")
        else:
            print(f"[WARN] {_p} not found")

        self._cached_zoom = None
        self._cached_surf = None

        if os.path.exists(MAP_DATA_FILE):
            with open(MAP_DATA_FILE) as f:
                self.data = json.load(f)
        else:
            self.data = {}
        self._ensure_key()

        self._wall_chunks    = ChunkMap()
        self._door_chunks    = ChunkMap()
        self._spawn_chunks   = ChunkMap()
        self._monster_chunks = ChunkMap()
        self.rebuild_chunks()

        self.computers: list[Computer] = self._build_computers()

    def _ensure_key(self):
        d = self.data.setdefault(MAP_KEY, {})
        for k in ("walls", "doors", "computers", "spawns",
                  "monster_spawns", "baldi_checkpoints", "baldi_connections"):
            d.setdefault(k, [])

    def entries(self, htype) -> list:
        return self.data[MAP_KEY].get(htype, [])

    def rebuild_chunks(self):
        self._wall_chunks.rebuild(self.entries("walls"))
        self._door_chunks.rebuild(self.entries("doors"))
        self._spawn_chunks.rebuild(
            [[e["x"], e["y"], e.get("w", 64), e.get("h", 64)]
             for e in self.entries("spawns")])
        self._monster_chunks.rebuild(
            [[e["x"], e["y"], e.get("w", 64), e.get("h", 64)]
             for e in self.entries("monster_spawns")])

    def _build_computers(self):
        return [Computer(e) for e in self.entries("computers")]

    def reset_computers(self):
        for c in self.computers:
            c.completed = False

    def walls_near(self, x, y, w, h):
        return self._wall_chunks.query_rects(x, y, w, h)

    def visible_walls(self, vr: pygame.Rect):
        return self._wall_chunks.query_rects(vr.x, vr.y, vr.width, vr.height)

    def visible_doors(self, vr: pygame.Rect):
        return self._door_chunks.query_rects(vr.x, vr.y, vr.width, vr.height)

    def first_spawn(self):
        spawns = self.entries("spawns")
        if spawns:
            s = spawns[0]
            return s["x"] + s.get("w", 64)//2, s["y"] + s.get("h", 64)//2
        return self.map_w//2, self.map_h//2

    def monster_spawns(self):
        return self.entries("monster_spawns")

    def baldi_checkpoint_graph(self):
        """
        Returns (points, adjacency) where:
          points      = list of (x, y)
          adjacency   = dict  { idx: [neighbour_idx, ...] }
        """
        pts  = [(e["x"], e["y"]) for e in self.entries("baldi_checkpoints")]
        adj  = {i: [] for i in range(len(pts))}
        for a, b in self.entries("baldi_connections"):
            if 0 <= a < len(pts) and 0 <= b < len(pts):
                if b not in adj[a]: adj[a].append(b)
                if a not in adj[b]: adj[b].append(a)
        return pts, adj

    def scaled(self, zoom):
        if zoom != self._cached_zoom:
            if self.image:
                sw = max(1, int(self.map_w * zoom))
                sh = max(1, int(self.map_h * zoom))
                self._cached_surf = pygame.transform.scale(self.image, (sw, sh))
            self._cached_zoom = zoom
        return self._cached_surf

    def save(self):
        self.data[MAP_KEY]["computers"] = [c.to_dict() for c in self.computers]
        with open(MAP_DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=2)
        self.rebuild_chunks()
        print("[INFO] map_data.json saved.")

    def draw(self, screen, camera):
        surf = self.scaled(camera.zoom)
        if surf:
            sx, sy  = camera.world_to_screen(0, 0)
            map_sr  = pygame.Rect(int(sx), int(sy),
                                  surf.get_width(), surf.get_height())
            clip    = map_sr.clip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            if clip.width > 0 and clip.height > 0:
                src_x = clip.x - map_sr.x
                src_y = clip.y - map_sr.y
                screen.blit(surf.subsurface(
                    pygame.Rect(src_x, src_y, clip.width, clip.height)),
                    (clip.x, clip.y))