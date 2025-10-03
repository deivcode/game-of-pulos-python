from pgzero.builtins import Actor

class Character(Actor):
    """
    Classe base para todos os personagens do jogo.
    """
    def __init__(self, image, **kwargs):
        super().__init__(image, **kwargs)
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False

class Player(Character):
    """
    O personagem do jogador.
    """
    def __init__(self, jump_sound, **kwargs):
        super().__init__('p_right', **kwargs)
        self.velocity_x = 3
        self.gravity = 0.5
        self.jump_velocity = -9
        self.double_jump_velocity = -15
        self.left_images = ['p_left', 'p_walk_left']
        self.right_images = ['p_right', 'p_walk_right']
        self.current_image_index = 0
        self.animation_counter = 0
        self.animation_speed = 10
        self.jump_sound = jump_sound

    def update(self, keyboard, width, ground, platforms, branches, jumps):
        # Gravidade
        self.velocity_y += self.gravity

        # Movimento horizontal
        original_x = self.x
        is_moving = False
        direction = 'right'
        if self.image in self.left_images:
            direction = 'left'

        if keyboard.left and self.midleft[0] > 0:
            self.x -= self.velocity_x
            is_moving = True
            direction = 'left'
        elif keyboard.right and self.midright[0] < width:
            self.x += self.velocity_x
            is_moving = True
            direction = 'right'

        # Colisão horizontal
        for ground_tile in ground:
            if self.colliderect(ground_tile):
                self.x = original_x
        for platform in platforms:
            if self.colliderect(platform):
                self.x = original_x

        # Movimento vertical
        self.y += self.velocity_y

        # Colisão vertical
        self.on_ground = False
        for ground_tile in ground:
            if self.colliderect(ground_tile):
                if self.velocity_y > 0:
                    self.bottom = ground_tile.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.top = ground_tile.bottom
                    self.velocity_y = 0
        
        for platform in platforms:
            if self.colliderect(platform):
                if self.velocity_y > 0:
                    self.bottom = platform.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.top = platform.bottom
                    self.velocity_y = 0
        
        for branch in branches:
            if self.colliderect(branch):
                if self.velocity_y > 0:
                    self.bottom = branch.top
                    self.velocity_y = 0
                    self.on_ground = True

        for jump_pad in jumps:
            if self.colliderect(jump_pad):
                if self.velocity_y >= 0:
                    self.velocity_y = self.double_jump_velocity
                    self.on_ground = False

        # Animação
        if is_moving:
            self.animation_speed = 6
        else:
            self.animation_speed = 10

        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            if direction == 'left':
                self.current_image_index = (self.current_image_index + 1) % len(self.left_images)
                self.image = self.left_images[self.current_image_index]
            else:
                self.current_image_index = (self.current_image_index + 1) % len(self.right_images)
                self.image = self.right_images[self.current_image_index]

    def on_key_down(self, key, keys):
        if key == keys.UP and self.on_ground:
            self.velocity_y = self.jump_velocity
            self.on_ground = False
            self.jump_sound.play()

class WalkingEnemy(Character):
    """
    Um inimigo que anda para a esquerda e para a direita.
    """
    def __init__(self, image='tile_0024', **kwargs):
        super().__init__(image, **kwargs)
        self.initial_x = 0
        self.move_direction_x = -1
        self.move_range_x = 138
        self.move_speed_x = 1
        self.images = ['tile_0024', 'tile_0025', 'tile_0026']
        self.current_image_index = 0
        self.animation_counter = 0
        self.animation_speed = 12

    def update(self):
        self.x += self.move_direction_x * self.move_speed_x
        if self.x >= self.initial_x:
            self.move_direction_x = -1
        elif self.x <= self.initial_x - self.move_range_x:
            self.move_direction_x = 1

        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.image = self.images[self.current_image_index]

class FishEnemy(Character):
    """
    Um inimigo que pula para cima e para baixo como um peixe.
    """
    def __init__(self, image='tile_fish-up', **kwargs):
        super().__init__(image, **kwargs)
        self.initial_y = 0
        self.move_direction_y = -1
        self.move_range_y = 219
        self.move_speed_y = 5
        self.up_images = ['tile_fish-up', 'tile_fish-up-closed']
        self.down_images = ['tile_down-open', 'tile_down-close']
        self.current_image_index = 0
        self.animation_counter = 0
        self.animation_speed = 6

    def update(self):
        self.y += self.move_direction_y * self.move_speed_y

        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            if self.move_direction_y == -1:
                self.current_image_index = (self.current_image_index + 1) % len(self.up_images)
                self.image = self.up_images[self.current_image_index]
            else:
                self.current_image_index = (self.current_image_index + 1) % len(self.down_images)
                self.image = self.down_images[self.current_image_index]

        if self.y <= self.initial_y - self.move_range_y:
            self.move_direction_y = 1
            self.current_image_index = 0
        elif self.y >= self.initial_y:
            self.move_direction_y = -1
            self.current_image_index = 0