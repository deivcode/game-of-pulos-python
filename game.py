# -----------------------------------------------
# Imports
# -----------------------------------------------
import pgzrun
from platformer import *
from characters import Player, WalkingEnemy, FishEnemy
from menu import Menu

# -----------------------------------------------
# Constantes da musica e varivel de rewards
# -----------------------------------------------
music.set_volume(0.25)
music.play('background_music.wav')

jump_sound = sounds.jump_up
coin_sound = sounds.coin_received
jump_sound.set_volume(0.2)
coin_sound.set_volume(0.2)

score_rewards = 0 # Variável global para contar as recompensas
score_coins = 0
game_over_timer = 0
win_timer = 0


# -----------------------------------------------
# Constantes do Jogo
# -----------------------------------------------
TILE_SIZE = 18  # Tamanho de cada bloco em pixels
GRID_WIDTH = 45  # Largura da grade em blocos
GRID_HEIGHT = 33  # Altura da grade em blocos

WIDTH = TILE_SIZE * GRID_WIDTH  # Largura da janela
HEIGHT = TILE_SIZE * GRID_HEIGHT  # Altura da janela
TITLE = "Game Of Pulos"  # Título da janela

# -----------------------------------------------
# Construindo nosso mundo de jogo a partir de arquivos CSV
# -----------------------------------------------

ground = build("platformer_ground.csv", TILE_SIZE)
rewards = build("platformer_rewards.csv", TILE_SIZE)
jumps = build("platformer_jumps.csv", TILE_SIZE)
goal = build("platformer_goal.csv", TILE_SIZE)
platforms = build("platformer_platforms.csv", TILE_SIZE)

for platform in platforms:
    platform._rect.inflate_ip(-10, -4)
moving_platforms = build("platformer_moving_platforms.csv", TILE_SIZE)
for platform in moving_platforms:
    platform._rect.inflate_ip(-10, -4)
branches = build("platformer_branches.csv", TILE_SIZE)
for branch in branches:
    branch._rect.inflate_ip(-10, -4) 
tree = build("platformer_tree.csv", TILE_SIZE)

# -----------------------------------------------
# Carrega os Inimigos
# -----------------------------------------------
walking_enemy_actors = build("platformer_walking_enemies.csv", TILE_SIZE)
fish_enemy_actors = build("platformer_fish_enemies.csv", TILE_SIZE)

walking_enemies = []
for enemy_actor in walking_enemy_actors:
    enemy = WalkingEnemy(image=enemy_actor.image, pos=enemy_actor.pos)
    enemy.initial_x = enemy.x
    walking_enemies.append(enemy)

fish_enemies = []
for fish_actor in fish_enemy_actors:
    fish = FishEnemy(image=fish_actor.image, pos=fish_actor.pos)
    fish.initial_y = fish.y
    fish_enemies.append(fish)


# -----------------------------------------------
# Movimento das plataformas
# -----------------------------------------------
for platform in platforms:
    platform.initial_y = platform.y
    platform.move_direction = 1
    platform.move_range = 50
    platform.move_speed = 1

for platform in moving_platforms:
    platform.initial_x = platform.x
    platform.move_direction_x = 1
    platform.move_range_x = 100
    platform.move_speed_x = 1

# -----------------------------------------------
# Inicialização do jogo
# -----------------------------------------------

game_state = 'menu'  # O jogo começa no menu

main_menu = Menu(WIDTH, HEIGHT)
game_background = Actor('game_background.png')
game_background.pos = WIDTH // 2, HEIGHT // 2

player = Player(jump_sound=jump_sound)
player.bottomleft = (0, HEIGHT - TILE_SIZE * 2)

mouse_pos = (0, 0)

def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos

def reset_level():
    global score_rewards, score_coins, rewards, game_state
    player.bottomleft = (0, HEIGHT - TILE_SIZE * 2)
    score_rewards = 0
    score_coins = 0
    rewards = build("platformer_rewards.csv", TILE_SIZE)
    game_state = 'playing'

# -----------------------------------------------
# Desenho do mundo
# -----------------------------------------------
def draw():
    screen.clear()
    screen.fill((0, 0, 0))

    if game_state == 'menu':
        main_menu.draw(screen, mouse_pos)
    elif game_state == 'playing' or game_state == 'game_over':
        game_background.draw()
        
        for ground_tile in ground:
            ground_tile.draw()

        for reward in rewards:
            reward.draw()
        
        for jump_pad in jumps:
            jump_pad.draw()

        for goal_tile in goal:
            goal_tile.draw()

        for platform in platforms:
            platform.draw()

        for platform in moving_platforms:
            platform.draw()

        for branch in branches:
            branch.draw()

        for tree_part in tree:
            tree_part.draw()

        for enemy in walking_enemies:
            enemy.draw()

        for fish_enemy in fish_enemies:
            fish_enemy.draw()
        
        player.draw()
        
        # Desenha o ícone de diamante e o contador de recompensas
        screen.blit('tile_0067', (WIDTH - 50, 10)) # Posição no canto superior direito
        screen.draw.text(f"{score_rewards}", topleft=(WIDTH - 25, 15), color="white", fontsize=20)

        # Desenha o ícone de coin e o contador de coins
        screen.blit('tile_0151', (WIDTH - 50, 40)) # Posição abaixo do diamante
        screen.draw.text(f"{score_coins}", topleft=(WIDTH - 25, 45), color="white", fontsize=20)

        if game_state == 'game_over':
            screen.draw.text("GAME OVER", center=(WIDTH / 2, HEIGHT / 2), fontsize=100, color="red", owidth=1, ocolor="white")

    elif game_state == 'win':
        screen.fill((0, 0, 0))
        screen.draw.text("YOU WIN", center=(WIDTH / 2, HEIGHT / 2 - 40), fontsize=80, color="green")
        screen.draw.text("Voce venceu", center=(WIDTH / 2, HEIGHT / 2 + 40), fontsize=40, color="white")

def on_mouse_down(pos):
    global game_state
    if game_state == 'menu':
        action = main_menu.handle_click(pos)
        if action == 'start_game':
            game_state = 'playing'

        elif action == 'toggle_music':
            if main_menu.is_music_on:
                music.unpause()
            else:
                music.pause()
        elif action == 'exit':
            exit()
# -----------------------------------------------
# Updates e verificações
# -----------------------------------------------
def update():
    global game_state, score_rewards, score_coins, game_over_timer, rewards, win_timer

    if game_state == 'playing':
        player.update(keyboard, WIDTH, ground, platforms, branches, jumps, main_menu.is_music_on)

        # Verifica colisão do jogador com as recompensas
        for reward in rewards[:]:  # Itera sobre uma cópia para permitir remoção
            if player.colliderect(reward):
                rewards.remove(reward)
                if main_menu.is_music_on: # Verifica se os sons estão ativados
                    coin_sound.play() # Play coin sound
                if reward.image == 'tile_0151':
                    score_coins += 1
                else:
                    score_rewards += 1

        # Verifica colisão com o objetivo
        for goal_tile in goal:
            if player.colliderect(goal_tile):
                game_state = 'win'
                win_timer = 0

        # Movimenta as plataformas
        for platform in platforms:
            platform.y += platform.move_direction * platform.move_speed
            if platform.y >= platform.initial_y + platform.move_range:
                platform.move_direction = -1
            elif platform.y <= platform.initial_y - platform.move_range:
                platform.move_direction = 1

        for platform in moving_platforms:
            platform.x += platform.move_direction_x * platform.move_speed_x
            if platform.x >= platform.initial_x + platform.move_range_x:
                platform.move_direction_x = -1
            elif platform.x <= platform.initial_x - platform.move_range_x:
                platform.move_direction_x = 1

        # Verifica colisão do jogador com as plataformas móveis
        for platform in moving_platforms:
            if player.colliderect(platform):
                if player.velocity_y > 0:
                    player.bottom = platform.top
                    player.velocity_y = 0
                    player.on_ground = True
                    player.x += platform.move_direction_x * platform.move_speed_x
                elif player.velocity_y < 0:
                    player.top = platform.bottom
                    player.velocity_y = 0

        # Atualiza os inimigos e verifica colisão
        for enemy in walking_enemies:
            enemy.update()
            if player.colliderect(enemy):
                game_state = 'game_over'
                game_over_timer = 0

        for fish_enemy in fish_enemies:
            fish_enemy.update()
            if player.colliderect(fish_enemy):
                game_state = 'game_over'
                game_over_timer = 0

    elif game_state == 'game_over':
        game_over_timer += 1
        if game_over_timer >= 120: # Wait for 2 seconds (at 60fps)
            reset_level()
    
    elif game_state == 'win':
        win_timer += 1
        if win_timer >= 180: # Wait for 3 seconds
            reset_level()
            game_state = 'menu'

def on_key_down(key):
    player.on_key_down(key, keys, main_menu.is_music_on)

pgzrun.go()