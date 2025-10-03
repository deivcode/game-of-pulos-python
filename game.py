import pgzrun
from platformer import *
from menu import Menu
from characters import Player, WalkingEnemy, FishEnemy
import pygame
import os

pygame.mixer.init()

# Manually load sounds
current_dir = os.path.dirname(__file__)
jump_sound_path = os.path.join(current_dir, "sounds", "jump_up.mp3")
coin_sound_path = os.path.join(current_dir, "sounds", "coin_received.mp3")
background_music_path = os.path.join(current_dir, "music", "background-music.mp3")

jump_sound = pygame.mixer.Sound(jump_sound_path)
coin_sound = pygame.mixer.Sound(coin_sound_path)

# -----------------------------------------------
# Constantes do Jogo
# -----------------------------------------------
TILE_SIZE = 18  # Tamanho de cada bloco em pixels
GRID_WIDTH = 45  # Largura da grade em blocos
GRID_HEIGHT = 33  # Altura da grade em blocos

WIDTH = TILE_SIZE * GRID_WIDTH  # Largura da janela
HEIGHT = TILE_SIZE * GRID_HEIGHT  # Altura da janela
TITLE = "Game Of Jumps"  # Título da janela

# -----------------------------------------------
# Construindo nosso mundo de jogo a partir de arquivos CSV
# -----------------------------------------------

ground = build("platformer_ground.csv", TILE_SIZE)
rewards = build("platformer_rewards.csv", TILE_SIZE)
jumps = build("platformer_jumps.csv", TILE_SIZE)
goal = build("platformer_goal.csv", TILE_SIZE)
platforms = build("platformer_platforms.csv", TILE_SIZE)
moving_platforms = build("platformer_moving_platforms.csv", TILE_SIZE)
branches = build("platformer_branches.csv", TILE_SIZE)
for branch in branches:
    branch._rect.inflate_ip(-10, -4)  # Diminui a hitbox dos galhos
tree = build("platformer_tree.csv", TILE_SIZE)

# Carrega os atores dos inimigos e os converte para as classes corretas
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


# Configura o movimento das plataformas
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
# Início do Jogo
# -----------------------------------------------

# -----------------------------------------------
# Inicialização do Jogo
# -----------------------------------------------

game_state = 'menu'  # O jogo começa no menu
is_music_on = True
pygame.mixer.music.set_volume(0.5)

main_menu = Menu(WIDTH, HEIGHT)
game_background = Actor('game_background.jpg')
game_background.pos = WIDTH // 2, HEIGHT // 2

player = Player(jump_sound=jump_sound)
player.bottomleft = (0, HEIGHT - TILE_SIZE * 2)

mouse_pos = (0, 0)

def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos

def draw():
    screen.clear()
    screen.fill((0, 0, 0))

    if game_state == 'menu':
        main_menu.draw(screen, mouse_pos)
    elif game_state == 'playing':
        game_background.draw()
        
        for ground_tile in ground:
            ground_tile.draw()

        for reward in rewards:
            reward.draw()
        
        for jump_pad in jumps:
            jump_pad.draw()

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
        screen.draw.text(f"X: {player.x}, Y: {player.y}", topleft=(10, 10), color="white", fontsize=20)

def on_mouse_down(pos):
    global game_state, is_music_on
    if game_state == 'menu':
        action = main_menu.handle_click(pos)
        if action == 'start_game':
            game_state = 'playing'
            if is_music_on:
                pygame.mixer.music.load(background_music_path)
                pygame.mixer.music.play(-1) # -1 means loop indefinitely
        elif action == 'toggle_music':
            is_music_on = not is_music_on
            if is_music_on:
                pygame.mixer.music.load(background_music_path)
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()
        elif action == 'exit':
            exit()

def update():
    global game_state, is_music_on

    if game_state == 'playing':
        player.update(keyboard, WIDTH, ground, platforms, branches, jumps)

        # Verifica colisão do jogador com as recompensas
        for reward in rewards[:]:  # Itera sobre uma cópia para permitir remoção
            if player.colliderect(reward):
                rewards.remove(reward)
                coin_sound.play() # Play coin sound

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
                player.bottomleft = (0, HEIGHT - TILE_SIZE * 2)

        for fish_enemy in fish_enemies:
            fish_enemy.update()
            if player.colliderect(fish_enemy):
                player.bottomleft = (0, HEIGHT - TILE_SIZE * 2)

def on_key_down(key):
    player.on_key_down(key, keys)

pgzrun.go()