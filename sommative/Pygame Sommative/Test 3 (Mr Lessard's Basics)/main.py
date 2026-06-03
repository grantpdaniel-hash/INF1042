import pygame
import sys
import random

pygame.init()

from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
                      DIFFICULTY, INTERACT_DIST)
from camera        import Camera
from map_loader    import MapLoader
from player        import Player
from editor        import HitboxEditor
from menu          import (MainMenu, LanguageSelect, DifficultySelect,
                            PauseMenu, VictoryScreen, GameOverScreen)
from ui            import (QuestionOverlay, FeedbackFlash,
                            draw_hud, draw_interact_prompt,
                            font_hud, font_small, C_WHITE, C_YELLOW, C_GREEN, C_RED)
from score_manager import ScoreManager
from questions     import QUESTIONS
from enemy         import Baldi

# ── Window ────────────────────────────────────────────────────────────────────
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# ── Global objects ────────────────────────────────────────────────────────────
camera     = Camera()
map_loader = MapLoader()
player     = Player()
editor     = HitboxEditor(map_loader, camera)

# ── Menu instances ────────────────────────────────────────────────────────────
main_menu       = MainMenu()
lang_select     = LanguageSelect()
diff_select     = DifficultySelect()
pause_menu      = PauseMenu()
victory_screen  = VictoryScreen()
gameover_screen = GameOverScreen()

# ── Game state ────────────────────────────────────────────────────────────────
state           = "menu"
language        = "Python"
difficulty      = "Beginner"
score_mgr       = ScoreManager(150, -10)
question_pool   = []
q_overlay       = QuestionOverlay()
feedback        = FeedbackFlash()
active_computer = None
q_close_timer   = 0
gameover_reason = ""

baldi = Baldi()
show_hitboxes = False

_comp_fill_cache = {}

def _comp_fill(w, h, completed):
    key = (w, h, completed)
    if key not in _comp_fill_cache:
        col = (20, 80, 30) if completed else (30, 180, 60)
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill((*col, 60))
        _comp_fill_cache[key] = s
        if len(_comp_fill_cache) > 256:
            _comp_fill_cache.pop(next(iter(_comp_fill_cache)))
    return _comp_fill_cache[key]


def handle_baldi_catch(penalty):
    score_mgr.score += penalty
    feedback.show(f"{penalty}  Caught by Baldi!", C_RED)
    sx, sy = map_loader.first_spawn()
    player.teleport(sx, sy)
    baldi.player_respawned()


def start_session():
    global score_mgr, question_pool, active_computer, q_close_timer, baldi

    diff_cfg      = DIFFICULTY[difficulty]
    score_mgr     = ScoreManager(diff_cfg["score_correct"], diff_cfg["score_wrong"])
    question_pool = list(QUESTIONS.get(language, {}).get(difficulty, []))
    random.shuffle(question_pool)

    map_loader.reset_computers()
    active_computer  = None
    q_close_timer    = 0
    q_overlay.active = False
    feedback.timer   = 0

    baldi          = Baldi(speed=diff_cfg["enemy_speed"])
    baldi.on_catch = handle_baldi_catch

    # Load checkpoint graph
    pts, adj = map_loader.baldi_checkpoint_graph()
    if pts:
        baldi.set_checkpoint_graph(pts, adj)

    sx, sy = map_loader.first_spawn()
    player.teleport(sx, sy)
    camera.zoom = 1.0
    camera.x    = sx - SCREEN_WIDTH  / 2
    camera.y    = sy - SCREEN_HEIGHT / 2


def draw_computers(vr):
    for comp in map_loader.computers:
        if not comp.rect.colliderect(vr): continue
        sr = camera.apply_rect(comp.rect)
        screen.blit(_comp_fill(max(1, sr.width), max(1, sr.height), comp.completed),
                    (sr.x, sr.y))
        border_col = (60, 220, 80) if not comp.completed else (40, 100, 40)
        pygame.draw.rect(screen, border_col, sr, 3, border_radius=4)
        t = font_small.render("💻" if not comp.completed else "✓", True,
                               (60, 220, 80) if not comp.completed else (80, 160, 80))
        screen.blit(t, (sr.centerx - t.get_width() // 2,
                         sr.centery - t.get_height() // 2))


def draw_debug_hitboxes():
    vr = camera.visible_world_rect()
    for w in map_loader.visible_walls(vr):
        pygame.draw.rect(screen, (255, 60, 60),  camera.apply_rect(w), 2)
    for d in map_loader.visible_doors(vr):
        pygame.draw.rect(screen, (60, 200, 255), camera.apply_rect(d), 2)


# ─────────────────────────────────────────────────────────────────────────────
while True:
    dt = clock.tick(FPS)
    mx, my = pygame.mouse.get_pos()

    if state == "editor" and pygame.mouse.get_pressed()[2]:
        rel = pygame.mouse.get_rel()
        camera.x -= rel[0] / camera.zoom
        camera.y -= rel[1] / camera.zoom
    else:
        pygame.mouse.get_rel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                if state == "playing": state = "editor"
                elif state == "editor": state = "playing"

            if event.key == pygame.K_F1 and state == "playing":
                show_hitboxes = not show_hitboxes

            if event.key == pygame.K_ESCAPE:
                if state == "playing":  state = "pause"
                elif state == "pause":  state = "playing"
                elif state == "editor": state = "playing"

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                map_loader.save()

            if event.key == pygame.K_e and state == "playing" and not q_overlay.active:
                for comp in map_loader.computers:
                    if not comp.completed and comp.in_range(player.rect):
                        if question_pool:
                            q = question_pool.pop(0)
                        else:
                            question_pool[:] = list(
                                QUESTIONS.get(language, {}).get(difficulty, []))
                            random.shuffle(question_pool)
                            q = question_pool.pop(0)
                        q_overlay.open(q)
                        active_computer = comp
                        break

        if state == "menu":
            result = main_menu.handle(event)
            if result == "language_select": state = "language_select"
            elif result == "quit":          pygame.quit(); sys.exit()

        elif state == "language_select":
            result = lang_select.handle(event)
            if result:
                action, val = result
                if action == "difficulty_select":
                    language    = val
                    diff_select = DifficultySelect(language)
                    state       = "difficulty_select"
                elif action == "menu":
                    state = "menu"

        elif state == "difficulty_select":
            result = diff_select.handle(event)
            if result:
                action, val = result
                if action == "playing":
                    difficulty = val
                    start_session()
                    state = "playing"
                elif action == "language_select":
                    state = "language_select"

        elif state == "playing":
            if q_overlay.active and q_close_timer <= 0:
                result = q_overlay.handle_event(event)
                if result == "correct":
                    pts = score_mgr.correct()
                    feedback.show(f"+{pts}  Correct!", C_GREEN)
                    if active_computer:
                        active_computer.complete()
                        active_computer = None
                    q_close_timer = 1400
                elif result == "wrong":
                    pts = score_mgr.wrong()
                    feedback.show(f"{pts}  Wrong!", C_RED)
                    active_computer = None
                    q_close_timer   = 1400
                    spawns = map_loader.monster_spawns()
                    if spawns:
                        s  = spawns[0]
                        sx = s["x"] + s.get("w", 64) // 2
                        sy = s["y"] + s.get("h", 64) // 2
                        if not baldi.spawned:
                            baldi.first_wrong_answer(sx, sy)
                        else:
                            baldi.wrong_answer()

        elif state == "pause":
            result = pause_menu.handle(event)
            if result == "playing":  state = "playing"
            elif result == "menu":   state = "menu"
            elif result == "quit":   pygame.quit(); sys.exit()

        elif state == "victory":
            result = victory_screen.handle(event)
            if result == "menu":      state = "menu"
            elif result == "playing": start_session(); state = "playing"

        elif state == "gameover":
            result = gameover_screen.handle(event)
            if result == "menu":      state = "menu"
            elif result == "playing": start_session(); state = "playing"

        elif state == "editor":
            editor.handle_event(event, mx, my)

    # ── UPDATE ────────────────────────────────────────────────────────────────
    if state == "playing":
        feedback.update(dt)
        if q_overlay.active and q_close_timer > 0:
            q_close_timer -= dt
            if q_close_timer <= 0:
                q_overlay.active = False

        if not q_overlay.active:
            keys = pygame.key.get_pressed()
            pr   = player.rect
            nearby_walls = map_loader.walls_near(pr.x - 200, pr.y - 200,
                                                  pr.width + 400, pr.height + 400)
            player.update(keys, nearby_walls)
            camera.follow(player.rect)

            baldi_walls = map_loader.walls_near(
                baldi.x - 200, baldi.y - 200,
                baldi.SIZE + 400, baldi.SIZE + 400)
            baldi.update(dt, player.rect, baldi_walls)

        total     = len(map_loader.computers)
        completed = sum(1 for c in map_loader.computers if c.completed)
        if total > 0 and completed >= total:
            state = "victory"

    # ── DRAW ──────────────────────────────────────────────────────────────────
    screen.fill((12, 14, 20))

    if state == "playing":
        step = max(64, int(256 * camera.zoom))
        sx0  = int((-camera.x % (step / camera.zoom)) * camera.zoom)
        sy0  = int((-camera.y % (step / camera.zoom)) * camera.zoom)
        for gx in range(sx0, SCREEN_WIDTH,  step):
            pygame.draw.line(screen, (20, 22, 30), (gx, 0), (gx, SCREEN_HEIGHT))
        for gy in range(sy0, SCREEN_HEIGHT, step):
            pygame.draw.line(screen, (20, 22, 30), (0, gy), (SCREEN_WIDTH, gy))

        map_loader.draw(screen, camera)
        vr = camera.visible_world_rect()
        draw_computers(vr)
        if show_hitboxes:
            draw_debug_hitboxes()

        pygame.draw.rect(screen, (255, 200, 0), camera.apply_rect(player.rect))
        baldi.draw(screen, camera)

        for comp in map_loader.computers:
            if not comp.completed and comp.in_range(player.rect):
                draw_interact_prompt(screen)
                break

        total     = len(map_loader.computers)
        completed = sum(1 for c in map_loader.computers if c.completed)
        draw_hud(screen, score_mgr.score, language, difficulty,
                 completed, total, DIFFICULTY[difficulty])
        feedback.draw(screen)
        if q_overlay.active:
            q_overlay.draw(screen)

        wx, wy = camera.screen_to_world(mx, my)
        screen.blit(font_hud.render(
            f"Player({int(player.x)},{int(player.y)})  "
            f"Mouse world({int(wx)},{int(wy)})  F1=hitboxes  F3=editor  ESC=pause",
            True, (60, 70, 100)), (8, SCREEN_HEIGHT - 28))

    elif state == "editor":
        step = max(32, int(128 * camera.zoom))
        sx0  = int((-camera.x % (step / camera.zoom)) * camera.zoom)
        sy0  = int((-camera.y % (step / camera.zoom)) * camera.zoom)
        for gx in range(sx0, SCREEN_WIDTH,  step):
            pygame.draw.line(screen, (30, 35, 45), (gx, 0), (gx, SCREEN_HEIGHT))
        for gy in range(sy0, SCREEN_HEIGHT, step):
            pygame.draw.line(screen, (30, 35, 45), (0, gy), (SCREEN_WIDTH, gy))
        map_loader.draw(screen, camera)
        editor.draw(screen, mx, my)
        wx, wy = camera.screen_to_world(mx, my)
        screen.blit(font_hud.render(
            f"[EDITOR]  screen({mx},{my})  world({int(wx)},{int(wy)})  "
            f"Zoom:{camera.zoom:.2f}  Ctrl+S=save  F3=game  ESC=game",
            True, (255, 180, 50)), (8, SCREEN_HEIGHT - 28))

    elif state == "menu":
        main_menu.draw(screen)
    elif state == "language_select":
        lang_select.draw(screen)
    elif state == "difficulty_select":
        diff_select.draw(screen)
    elif state == "pause":
        map_loader.draw(screen, camera)
        vr = camera.visible_world_rect()
        draw_computers(vr)
        pygame.draw.rect(screen, (255, 200, 0), camera.apply_rect(player.rect))
        baldi.draw(screen, camera)
        pause_menu.draw(screen)
    elif state == "victory":
        victory_screen.draw(screen, score_mgr.score, language, difficulty)
    elif state == "gameover":
        gameover_screen.draw(screen, score_mgr.score, gameover_reason)

    pygame.display.flip()