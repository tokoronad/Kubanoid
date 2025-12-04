import pygame
import math
import random
import os

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (122, 122, 122)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
FW, SW = (100, 200, 0), (200, 100, 0)
BG_COLOR = (66, 73, 69)
MAX_SPEED, BOOST_SPEED = 7.0, 12.0
GRAVITY = 1.0
BLOCK_SIZE = 80

level_map = [
    "* $                                      ***********                         ",
    " *********                                            **                     ",
    "                *********      ****                                 ******   ",
    "*******                                                                      ",
    "                                       *********       *************         ",
    "       *************         *****                                           ",
    "                                     *********                               ",
    "                                                   ******                    ",
    "      *********                                                              ",
    " *****              ********                    *********                    ",
    "                                                                             ",
    "     ***        *******          *******                      ******         ",
    "                                                                             ",
    "     ******************           *******          **********                ",
    "                                                                             ",
    "                                                                             ",
    "                                                                             ",
    "                                                                             ",
]

PARTICLE_COLORS = {
    'bullet_impact': [(221, 221, 221), (131, 131, 131), (34, 27, 25)],
    'jump': [(200, 230, 255), (150, 200, 255), (100, 170, 255)],
    'land': [(200, 200, 200), (150, 150, 150), (100, 100, 100)],
    'run': [(100, 100, 150), (70, 70, 120), (50, 50, 100)],
    'wall_jump': [(255, 100, 100), (200, 70, 70), (150, 50, 50)],
    'blood': [(200, 0, 0), (180, 0, 0), (160, 0, 0), (140, 0, 0)]
}

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Кубаноид")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_tracks = []
        self.current_music_index = 0
        self.music_volume = 0.5
        self.sound_volume = 0.7
        self.load_sounds()
        self.load_music()
        
    def load_sounds(self):
        try:
            self.sounds['shotgun'] = self.load_sound("shoot_shotgun.mp3")
            self.sounds['rifle'] = self.load_sound("shoot_rifle.mp3")
            
            self.sounds['running'] = self.load_sound("running.wav")
            self.sounds['walking'] = self.load_sound("running.wav")
            if self.sounds['walking']:
                self.sounds['walking'].set_playback_rate(0.66)
            
            self.sounds['jump'] = self.load_sound("jump.wav")
            self.sounds['dash'] = self.load_sound("dash.wav")
            
            self.sounds['reload'] = self.load_sound("rearmed.mp3")
            
            self.sounds['button'] = self.load_sound("menu_button.mp3")
                
        except Exception as e:
            print(f"Ошибка загрузки звуков: {e}")
    
    def load_sound(self, filename):
        try:
            filepath = os.path.join("sound", filename)
            if os.path.exists(filepath):
                return pygame.mixer.Sound(filepath)
            else:
                print(f"Файл звука не найден: {filepath}")
                return None
        except Exception as e:
            print(f"Ошибка загрузки звука {filename}: {e}")
            return None
    
    def load_music(self):
        try:
            possible_tracks = ["1_sound.wav", "2_sound.wav", "background_music.wav", "music.mp3"]
            self.music_tracks = []
            
            for track in possible_tracks:
                filepath = os.path.join("sound", track)
                if os.path.exists(filepath):
                    self.music_tracks.append(filepath)
                    print(f"Найден музыкальный файл: {filepath}")
            
            if not self.music_tracks:
                print("Музыкальные файлы не найдены. Создаем заглушку.")
                self.create_music_stub()
            else:
                self.play_next_music()
                
        except Exception as e:
            print(f"Ошибка загрузки музыки: {e}")
            self.create_music_stub()
    
    def create_music_stub(self):
        print("Создание заглушки для музыки...")
        try:
            import numpy as np
            
            sample_rate = 44100
            duration = 10
            frequency = 440
            
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio_data = np.sin(2 * np.pi * frequency * t)
            
            audio_data = (audio_data * 32767).astype(np.int16)
            
            stub_sound = pygame.mixer.Sound(buffer=audio_data.tobytes())
            self.sounds['music_stub'] = stub_sound
            stub_sound.set_volume(0.1)
            
        except Exception as e:
            print(f"Не удалось создать музыкальную заглушку: {e}")
    
    def play_next_music(self):
        if self.music_tracks:
            try:
                pygame.mixer.music.load(self.music_tracks[self.current_music_index])
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play()
                print(f"Воспроизведение музыки: {self.music_tracks[self.current_music_index]}")
                
                self.current_music_index = (self.current_music_index + 1) % len(self.music_tracks)
            except Exception as e:
                print(f"Ошибка воспроизведения музыки: {e}")
                if 'music_stub' in self.sounds:
                    self.sounds['music_stub'].play(loops=-1)
    
    def update_music(self):
        if self.music_tracks and not pygame.mixer.music.get_busy():
            self.play_next_music()
        elif not self.music_tracks and 'music_stub' in self.sounds:
            if not pygame.mixer.get_busy():
                self.sounds['music_stub'].play(loops=-1)
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Ошибка воспроизведения звука {sound_name}: {e}")
    
    def play_reload_sound(self):
        def play_with_delay(i):
            if i < 6:
                self.play_sound('reload')
                pygame.time.set_timer(pygame.USEREVENT + i, 100, 1)
        
        play_with_delay(0)

sound_manager = SoundManager()

class PlatformTextureManager:
    def __init__(self):
        try:
            self.tiles_sheet = pygame.image.load("images/tiles.png").convert_alpha()
        except:
            print("Ошибка загрузки images/tiles.png. Создаем заглушки.")
            self.create_fallback_tiles()
            return
        
        sheet_width, sheet_height = self.tiles_sheet.get_size()
        print(f"Размер tiles.png: {sheet_width}x{sheet_height}")
        
        if sheet_width >= 80 and sheet_height >= 80:
            self.tile_size = 80
            tiles_per_row = sheet_width // self.tile_size
            total_tiles = min(tiles_per_row * (sheet_height // self.tile_size), 19)
        else:
            self.tile_size = min(sheet_width, sheet_height)
            total_tiles = 1
        
        self.tile_count = total_tiles
        self.tiles = []
        
        print(f"Размер тайла: {self.tile_size}, всего тайлов: {self.tile_count}")
        
        tiles_created = 0
        for y in range(0, sheet_height, self.tile_size):
            for x in range(0, sheet_width, self.tile_size):
                if tiles_created >= self.tile_count:
                    break
                try:
                    tile = self.tiles_sheet.subsurface(pygame.Rect(x, y, self.tile_size, self.tile_size))
                    self.tiles.append(tile)
                    tiles_created += 1
                except:
                    print(f"Ошибка создания тайла {tiles_created} из позиции ({x}, {y})")
                    fallback = pygame.Surface((self.tile_size, self.tile_size))
                    color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
                    fallback.fill(color)
                    self.tiles.append(fallback)
                    tiles_created += 1
        
        while len(self.tiles) < 19:
            fallback = pygame.Surface((self.tile_size, self.tile_size))
            color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            fallback.fill(color)
            font = pygame.font.Font(None, 24)
            text = font.render(str(len(self.tiles)), True, (255, 255, 255))
            fallback.blit(text, (10, 10))
            self.tiles.append(fallback)
        
        self.platform_textures = {}
        self.platform_decorations = {}
        
    def create_fallback_tiles(self):
        self.tile_size = 80
        self.tile_count = 19
        self.tiles = []
        
        colors = [
            (100, 100, 100),
            (150, 100, 100),
            (120, 150, 100),
            (100, 100, 150),
            (120, 120, 150),
            (140, 140, 150), 
            (160, 160, 150),
            (180, 180, 150),
            (150, 100, 100),
            (150, 120, 100),
            (150, 140, 100),
            (150, 160, 100),
            (150, 180, 100),
            (200, 100, 100),
            (200, 150, 100),
            (100, 200, 100),
            (100, 200, 150),
            (100, 200, 200),
            (150, 200, 200)
        ]
        
        for i in range(self.tile_count):
            tile = pygame.Surface((self.tile_size, self.tile_size))
            color = colors[i] if i < len(colors) else (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            tile.fill(color)
            
            font = pygame.font.Font(None, 36)
            text = font.render(str(i), True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.tile_size//2, self.tile_size//2))
            tile.blit(text, text_rect)
            
            self.tiles.append(tile)
    
    def has_platform_at(self, x, y):
        for plat in platforms:
            if plat.x == x and plat.y == y:
                return True
        return False
    
    def get_surrounding_platforms(self, platform):
        x, y = platform.x, platform.y
        
        return {
            'top': self.has_platform_at(x, y - BLOCK_SIZE),
            'bottom': self.has_platform_at(x, y + BLOCK_SIZE),
            'left': self.has_platform_at(x - BLOCK_SIZE, y),
            'right': self.has_platform_at(x + BLOCK_SIZE, y),
            'top_left': self.has_platform_at(x - BLOCK_SIZE, y - BLOCK_SIZE),
            'top_right': self.has_platform_at(x + BLOCK_SIZE, y - BLOCK_SIZE),
            'bottom_left': self.has_platform_at(x - BLOCK_SIZE, y + BLOCK_SIZE),
            'bottom_right': self.has_platform_at(x + BLOCK_SIZE, y + BLOCK_SIZE)
        }
    
    def get_platform_key(self, platform):
        return (platform.x, platform.y)
    
    def assign_textures(self):
        self.platform_textures.clear()
        self.platform_decorations.clear()
        
        for platform in platforms:
            platform_key = self.get_platform_key(platform)
            neighbors = self.get_surrounding_platforms(platform)
            
            if (neighbors['top'] and neighbors['bottom'] and 
                neighbors['left'] and neighbors['right']):
                texture_index = 0
                
            elif (sum([neighbors['bottom'], neighbors['left'], neighbors['right']]) == 3 and 
                  not neighbors['top']):
                texture_index = random.choice([1, 2])
                
            elif neighbors['right'] and not neighbors['left']:
                texture_index = random.randint(3, 7)
                
            elif neighbors['left'] and not neighbors['right']:
                texture_index = random.randint(8, 12)
                
            elif not neighbors['left'] and not neighbors['right']:
                left_texture_idx = random.randint(3, 7)
                right_texture_idx = random.randint(8, 12)
                
                combined_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                
                left_part = self.tiles[left_texture_idx].subsurface(pygame.Rect(0, 0, 40, BLOCK_SIZE))
                right_part = self.tiles[right_texture_idx].subsurface(pygame.Rect(40, 0, 40, BLOCK_SIZE))
                
                combined_surface.blit(left_part, (0, 0))
                combined_surface.blit(right_part, (40, 0))
                
                self.platform_textures[platform_key] = combined_surface
                continue
                
            else:
                texture_index = 0
            
            if texture_index < len(self.tiles):
                self.platform_textures[platform_key] = self.tiles[texture_index]
            else:
                self.platform_textures[platform_key] = self.tiles[0]
            
            if random.random() < 0.1:
                if not neighbors['bottom'] and random.random() < 0.3:
                    decoration_index = 13 if 13 < len(self.tiles) else 0
                    self.platform_decorations[platform_key] = {
                        'type': 'ceiling',
                        'texture': self.tiles[decoration_index],
                        'offset_y': BLOCK_SIZE
                    }
                
                elif not neighbors['top'] and random.random() < 0.4:
                    decoration_index = min(15, len(self.tiles) - 1)
                    self.platform_decorations[platform_key] = {
                        'type': 'surface', 
                        'texture': self.tiles[decoration_index],
                        'offset_y': -BLOCK_SIZE
                    }
    
    def draw_platforms(self, camera_x, camera_y):
        for platform in platforms:
            platform_key = self.get_platform_key(platform)
            
            if platform_key in self.platform_textures:
                texture = self.platform_textures[platform_key]
                if texture.get_size() != (BLOCK_SIZE, BLOCK_SIZE):
                    texture = pygame.transform.scale(texture, (BLOCK_SIZE, BLOCK_SIZE))
                screen.blit(texture, (platform.x - camera_x, platform.y - camera_y))
            else:
                pygame.draw.rect(screen, WHITE, 
                               (platform.x - camera_x, platform.y - camera_y, 
                                platform.width, platform.height))
            
            if platform_key in self.platform_decorations:
                decoration = self.platform_decorations[platform_key]
                texture = decoration['texture']
                if texture.get_size() != (BLOCK_SIZE, BLOCK_SIZE):
                    texture = pygame.transform.scale(texture, (BLOCK_SIZE, BLOCK_SIZE))
                screen.blit(texture,
                           (platform.x - camera_x, 
                            platform.y - camera_y + decoration['offset_y']))

texture_manager = PlatformTextureManager()

class Particle:
    def __init__(self, x, y, particle_type, direction=None, count=10):
        self.particles = []
        self.type = particle_type
        
        if particle_type == 'bullet_impact':
            for _ in range(count):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(2, 8)
                size = random.randint(2, 6)
                lifetime = random.uniform(20, 40)
                color = random.choice(PARTICLE_COLORS['bullet_impact'])
                
                self.particles.append({
                    'x': x, 'y': y,
                    'vx': math.cos(angle) * speed,
                    'vy': math.sin(angle) * speed,
                    'size': size,
                    'lifetime': lifetime,
                    'max_lifetime': lifetime,
                    'color': color
                })
                
        elif particle_type == 'jump':
            for _ in range(count):
                angle = random.uniform(math.pi * 0.7, math.pi * 1.3)
                speed = random.uniform(3, 7)
                size = random.randint(3, 7)
                lifetime = random.uniform(15, 25)
                color = random.choice(PARTICLE_COLORS['jump'])
                
                self.particles.append({
                    'x': x, 'y': y,
                    'vx': math.cos(angle) * speed * random.choice([-1, 1]),
                    'vy': math.sin(angle) * speed,
                    'size': size,
                    'lifetime': lifetime,
                    'max_lifetime': lifetime,
                    'color': color
                })
                
        elif particle_type == 'land':
            for _ in range(count * 2):
                angle = random.uniform(0, math.pi)
                speed = random.uniform(2, 6)
                size = random.randint(2, 5)
                lifetime = random.uniform(20, 30)
                color = random.choice(PARTICLE_COLORS['land'])
                
                self.particles.append({
                    'x': x + random.uniform(-20, 20), 
                    'y': y,
                    'vx': random.uniform(-2, 2),
                    'vy': -math.sin(angle) * speed,
                    'size': size,
                    'lifetime': lifetime,
                    'max_lifetime': lifetime,
                    'color': color
                })
                
        elif particle_type == 'run':
            for _ in range(count // 2):
                size = random.randint(2, 4)
                lifetime = random.uniform(10, 20)
                color = random.choice(PARTICLE_COLORS['run'])
                
                self.particles.append({
                    'x': x + random.uniform(-15, 15), 
                    'y': y + 10,
                    'vx': random.uniform(-1, 1) + (direction * 2 if direction else 0),
                    'vy': random.uniform(1, 3),
                    'size': size,
                    'lifetime': lifetime,
                    'max_lifetime': lifetime,
                    'color': color
                })
                
        elif particle_type == 'wall_jump':
            wall_direction = direction if direction else 1
            for _ in range(count):
                angle = random.uniform(math.pi * 0.25, math.pi * 0.75) if wall_direction > 0 else \
                        random.uniform(math.pi * 1.25, math.pi * 1.75)
                speed = random.uniform(3, 8)
                size = random.randint(3, 6)
                lifetime = random.uniform(20, 30)
                color = random.choice(PARTICLE_COLORS['wall_jump'])
                
                self.particles.append({
                    'x': x, 'y': y,
                    'vx': math.cos(angle) * speed,
                    'vy': math.sin(angle) * speed,
                    'size': size,
                    'lifetime': lifetime,
                    'max_lifetime': lifetime,
                    'color': color
                })

        elif particle_type == 'blood':
            for _ in range(count):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(3, 10)
                size = random.randint(3, 7)
                lifetime = random.uniform(20, 40)
                color = random.choice(PARTICLE_COLORS['blood'])
                
                self.particles.append({
                    'x': x, 'y': y,
                    'vx': math.cos(angle) * speed,
                    'vy': math.sin(angle) * speed,
                    'size': size,
                    'lifetime': lifetime,
                    'max_lifetime': lifetime,
                    'color': color
                })
    
    def update(self):
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['lifetime'] -= 1
            
            if self.type in ['bullet_impact', 'land', 'run']:
                particle['vy'] += 0.2
                
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
                
        return len(self.particles) > 0
    
    def draw(self, camera_x, camera_y):
        for particle in self.particles:
            alpha = int(255 * (particle['lifetime'] / particle['max_lifetime']))
            color = (*particle['color'], alpha)
            
            surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (particle['size'], particle['size']), particle['size'])
            screen.blit(surf, (particle['x'] - camera_x - particle['size'], 
                             particle['y'] - camera_y - particle['size']))

class EffectManager:
    def __init__(self):
        self.effects = []
        
    def add_effect(self, x, y, effect_type, direction=None, count=10):
        self.effects.append(Particle(x, y, effect_type, direction, count))
        
    def update(self):
        for effect in self.effects[:]:
            if not effect.update():
                self.effects.remove(effect)
                
    def draw(self, camera_x, camera_y):
        for effect in self.effects:
            effect.draw(camera_x, camera_y)

effect_manager = EffectManager()

class InterfaceManager:
    def __init__(self):
        try:
            self.interface_sheet = pygame.image.load("images/interface.png").convert_alpha()
        except:
            print("Ошибка загрузки images/interface.png")
            self.interface_sheet = None
            return
            
        self.sheet_width = 17280
        self.sheet_height = 1080
        self.frame_width = 1920
        self.frame_height = 1080
        self.total_frames = 9
        
        self.frames = []
        for i in range(self.total_frames):
            frame_rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame = self.interface_sheet.subsurface(frame_rect)
            self.frames.append(frame)
            
        self.current_bullets = 0
        self.dash_available = False
        self.extra_jump_available = False
        
    def update_state(self, weapon_system, player):
        self.current_bullets = 6 - weapon_system.shot_count
        
        self.dash_available = player.dash_cooldown <= 0
        
        self.extra_jump_available = player.jump_count < 2
        
    def draw(self, screen):
        if not self.interface_sheet:
            return
            
        screen.blit(self.frames[0], (0, 0))
        
        if 1 <= self.current_bullets <= 6:
            bullet_frame_index = 7 - self.current_bullets
            if 1 <= bullet_frame_index <= 6:
                screen.blit(self.frames[bullet_frame_index], (0, 0))
        
        if self.dash_available:
            screen.blit(self.frames[7], (0, 0))
            
        if self.extra_jump_available:
            screen.blit(self.frames[8], (0, 0))

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 72, 60)
        self.vx = 0
        self.vy = 0
        self.jump_count = 0
        self.wall_jump_used = False
        self.on_ground = False
        self.on_wall = False
        self.wall_dir = 0
        self.time_scale = 1.0
        self.facing_right = True
        self.health = 1
        self.alive = True
        
        self.was_on_ground = False
        self.was_on_wall = False
        self.last_move_direction = 1
        
        self.animation_sheet = pygame.image.load("images/kubmove.png").convert_alpha()
        self.sprite_width = 72
        self.sprite_height = 72
        self.sprite_count = 8
        self.sprites = []
        self.current_sprite = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
        self.idle_timer = 0
        self.is_moving = False
        self.moving_backwards = False
        
        self.jump_sheet = pygame.image.load("images/jump_up.png").convert_alpha()
        self.jump_sprite_width = 81
        self.jump_sprite_height = 85
        self.jump_sprite_count = 3
        self.jump_sprites = []
        self.jump_animation_timer = 0
        self.jump_animation_speed = 0.15
        self.is_jumping = False
        self.jump_frame_repeat_count = 0
        self.current_jump_sprite = 0
        self.jump_started_from_ground = False

        for i in range(self.sprite_count):
            sprite_rect = pygame.Rect(i * self.sprite_width, 0, self.sprite_width, self.sprite_height)
            sprite = self.animation_sheet.subsurface(sprite_rect)
            self.sprites.append(sprite)
            
        for i in range(self.jump_sprite_count):
            sprite_rect = pygame.Rect(i * self.jump_sprite_width, 0, self.jump_sprite_width, self.jump_sprite_height)
            sprite = self.jump_sheet.subsurface(sprite_rect)
            self.jump_sprites.append(sprite)

        self.dash_cooldown = 0
        self.dash_duration = 0
        self.dash_speed = 40.0
        self.dash_direction = (0, 0)
        self.is_dashing = False
        self.is_invulnerable = False
        self.dash_invul_duration = 60
        self.dash_cooldown_max = 300
        
        self.dash_trails = []
        self.trail_timer = 0
        self.trail_interval = 2
        
        self.dash_trail_particles = []

    def update_facing_direction(self, black_circle_x):
        player_center_x = self.rect.centerx
        self.facing_right = black_circle_x > player_center_x
        
    def start_dash(self, target_angle):
        if (self.dash_cooldown <= 0 and not self.is_dashing and 
            not self.is_invulnerable and self.alive):
            
            sound_manager.play_sound('dash')
            
            dash_x = math.cos(target_angle)
            dash_y = math.sin(target_angle)
            
            length = math.sqrt(dash_x**2 + dash_y**2)
            if length > 0:
                self.dash_direction = (dash_x/length, dash_y/length)
            else:
                self.dash_direction = (1, 0)
            
            self.is_dashing = True
            self.is_invulnerable = True
            self.dash_duration = 10
            self.dash_invul_duration = 60
            self.dash_cooldown = self.dash_cooldown_max
            
            self.dash_trails = []
            self.trail_timer = 0
            
            effect_manager.add_effect(
                self.rect.centerx,
                self.rect.centery,
                'jump',
                direction=self.dash_direction[0],
                count=15
            )
            
    def create_dash_trail(self):
        if self.is_jumping:
            current_sprite = self.jump_sprites[self.current_jump_sprite]
            y_offset = -25
        else:
            current_sprite = self.sprites[self.current_sprite]
            y_offset = 0
            
        if not self.facing_right:
            current_sprite = pygame.transform.flip(current_sprite, True, False)
        
        trail_sprite = current_sprite.copy()
        trail_sprite.set_alpha(100)
        
        self.dash_trails.append({
            'sprite': trail_sprite,
            'x': self.rect.x,
            'y': self.rect.y + y_offset,
            'lifetime': 20,
            'facing_right': self.facing_right,
            'is_jumping': self.is_jumping,
            'current_sprite': self.current_sprite,
            'current_jump_sprite': self.current_jump_sprite
        })
            
    def update_dash_trails(self):
        for trail in self.dash_trails[:]:
            trail['lifetime'] -= 1
            if trail['lifetime'] > 0:
                alpha = int(100 * (trail['lifetime'] / 20))
                trail['sprite'].set_alpha(alpha)
            else:
                self.dash_trails.remove(trail)
                
    def draw_dash_trails(self, camera_x, camera_y):
        for trail in self.dash_trails:
            screen.blit(trail['sprite'], 
                       (trail['x'] - camera_x, 
                        trail['y'] - camera_y))
    
    def check_dash_collision_with_enemies(self, enemies):
        if not self.is_dashing:
            return
            
        dash_damage = 150
        
        for enemy in enemies:
            if enemy.alive and self.rect.colliderect(enemy.rect):
                if enemy.take_damage(dash_damage):
                    if hasattr(enemy, 'score_value'):
                        score[0] += enemy.score_value
                    
                    self.create_blood_effect(enemy.rect.centerx, enemy.rect.centery, 30)
                else:
                    self.create_blood_effect(enemy.rect.centerx, enemy.rect.centery, 15)
                
                dx = enemy.rect.centerx - self.rect.centerx
                dy = enemy.rect.centery - self.rect.centery
                length = max(math.sqrt(dx*dx + dy*dy), 0.1)
                
                push_force = 10
                enemy.vx += (dx / length) * push_force
                enemy.vy += (dy / length) * push_force * 0.5
                
    def create_blood_effect(self, x, y, count):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(3, 10)
            size = random.randint(3, 7)
            lifetime = random.uniform(20, 40)
            
            blood_colors = [(200, 0, 0), (180, 0, 0), (160, 0, 0), (140, 0, 0)]
            color = random.choice(blood_colors)
            
            effect_manager.add_effect(
                x, y, 'bullet_impact',
                count=1
            )
            
            if effect_manager.effects:
                last_effect = effect_manager.effects[-1]
                if last_effect.particles:
                    last_effect.particles[0]['color'] = color
                    last_effect.particles[0]['size'] = size
                    last_effect.particles[0]['vx'] = math.cos(angle) * speed
                    last_effect.particles[0]['vy'] = math.sin(angle) * speed
                    last_effect.particles[0]['lifetime'] = lifetime
                    last_effect.particles[0]['max_lifetime'] = lifetime
        effect_manager.add_effect(x, y, 'blood', count=count)
    
    def update_dash(self):
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
            
        if self.is_dashing:
            self.dash_duration -= 1
            
            self.trail_timer += 1
            if self.trail_timer >= self.trail_interval:
                self.create_dash_trail()
                self.trail_timer = 0
                
            if self.dash_duration <= 0:
                self.is_dashing = False
                self.vx = self.dash_direction[0] * 5
                self.vy = self.dash_direction[1] * 5
                
        if self.is_invulnerable:
            self.dash_invul_duration -= 1
            if self.dash_invul_duration <= 0:
                self.is_invulnerable = False
                
        self.update_dash_trails()

    def update_animation(self, dt):
        if not self.alive:
            return
            
        was_moving = self.is_moving
        self.is_moving = abs(self.vx) > 0.1
        
        if self.is_moving:
            if (self.vx > 0 and not self.facing_right) or (self.vx < 0 and self.facing_right):
                self.moving_backwards = True
            else:
                self.moving_backwards = False
        
        if self.is_jumping:
            self.jump_animation_timer += dt * self.jump_animation_speed
            
            if self.jump_animation_timer >= 1:
                if self.current_jump_sprite == 2:
                    self.jump_frame_repeat_count += 1
                    if self.jump_frame_repeat_count < 3:
                        self.jump_animation_timer = 0
                        return
                
                self.current_jump_sprite += 1
                if self.current_jump_sprite >= self.jump_sprite_count:
                    self.current_jump_sprite = 2
                self.jump_animation_timer = 0
                
        elif self.is_moving:
            self.idle_timer = 0
            self.animation_timer += dt * self.animation_speed
            
            if self.animation_timer >= 1:
                if self.moving_backwards:
                    self.current_sprite = (self.current_sprite - 1) % self.sprite_count
                else:
                    self.current_sprite = (self.current_sprite + 1) % self.sprite_count
                self.animation_timer = 0
        else:
            if was_moving:
                self.idle_timer = 0
            else:
                self.idle_timer += dt
            
            if self.idle_timer >= 0.2:
                self.current_sprite = 0
        
        if self.on_ground and self.is_jumping:
            self.is_jumping = False
            self.jump_frame_repeat_count = 0

    def move(self, keys, dt):
        if not self.alive:
            return
            
        self.update_dash()
            
        self.time_scale = 1.0

        self.was_on_ground = self.on_ground
        self.was_on_wall = self.on_wall
        old_vx = self.vx

        if self.is_dashing:
            self.vx = self.dash_direction[0] * self.dash_speed
            self.vy = self.dash_direction[1] * self.dash_speed
            
            all_enemies = enemy_spawner.ground_enemies + enemy_spawner.flying_enemies
            self.check_dash_collision_with_enemies(all_enemies)
        else:
            scaled_dt = dt * self.time_scale
            target_speed = 0
            acceleration = 0.1 * scaled_dt
            friction = 0.1 * scaled_dt

            if keys[pygame.K_a]:
                target_speed = -MAX_SPEED
                self.last_move_direction = -1
            if keys[pygame.K_d]:
                target_speed = MAX_SPEED
                self.last_move_direction = 1
            if keys[pygame.K_LSHIFT]:
                acceleration = 0.2 * scaled_dt
                friction = 0.2 * scaled_dt
                target_speed *= BOOST_SPEED / MAX_SPEED

            self.vx += (target_speed - self.vx) * acceleration
            if target_speed == 0:
                if self.vx > 0:
                    self.vx -= friction
                    if self.vx < 0:
                        self.vx = 0
                elif self.vx < 0:
                    self.vx += friction
                    if self.vx > 0:
                        self.vx = 0

            if abs(self.vx) < 0.1:
                self.vx = 0

        self.rect.x += self.vx * (dt * self.time_scale if not self.is_dashing else 1)
        self.on_wall = False
        self.wall_dir = 0
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vx > 0:
                    self.rect.right = plat.left
                    self.wall_dir = 1
                elif self.vx < 0:
                    self.rect.left = plat.right
                    self.wall_dir = -1
                self.vx = 0
                self.on_wall = True
                if self.is_dashing:
                    self.is_dashing = False
                    effect_manager.add_effect(
                        self.rect.centerx,
                        self.rect.centery,
                        'bullet_impact',
                        count=15
                    )

        if not self.is_dashing:
            self.vy += GRAVITY * dt * self.time_scale
            if self.on_wall and self.wall_jump_used:
                self.vy *= 0.7
                
        self.rect.y += self.vy * (dt * self.time_scale if not self.is_dashing else 1)
        self.on_ground = False

        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vy > 0:
                    self.rect.bottom = plat.top
                    self.vy = 0
                    self.on_ground = True
                    self.jump_count = 0
                    if self.is_dashing:
                        self.is_dashing = False
                        effect_manager.add_effect(
                            self.rect.centerx, 
                            self.rect.bottom, 
                            'land', 
                            count=20
                        )
                    else:
                        if not self.was_on_ground:
                            effect_manager.add_effect(
                                self.rect.centerx, 
                                self.rect.bottom, 
                                'land', 
                                count=15
                            )
                elif self.vy < 0:
                    self.rect.top = plat.bottom
                    self.vy = 0
                    if self.is_dashing:
                        self.is_dashing = False
                        effect_manager.add_effect(
                            self.rect.centerx,
                            self.rect.top,
                            'bullet_impact',
                            count=15
                        )

        if self.on_ground and self.is_moving and random.random() < 0.3 and not self.is_dashing:
            effect_manager.add_effect(
                self.rect.centerx, 
                self.rect.bottom,
                'run',
                direction=self.last_move_direction,
                count=3
            )

    def start_jump(self):
        if not self.alive:
            return
            
        if self.on_ground:
            self.is_jumping = True
            self.jump_started_from_ground = True
            self.current_jump_sprite = 0
            self.jump_frame_repeat_count = 0
            self.jump_animation_timer = 0
            
            effect_manager.add_effect(
                self.rect.centerx,
                self.rect.bottom,
                'jump',
                count=12
            )
        else:
            self.is_jumping = True
            self.current_jump_sprite = 1
            self.jump_frame_repeat_count = 0
            self.jump_animation_timer = 0
            
            effect_manager.add_effect(
                self.rect.centerx,
                self.rect.bottom,
                'jump',
                count=8
            )

    def jump(self):
        if not self.alive:
            return
            
        if self.on_ground:
            self.vy = -15.0
            self.jump_count += 1
            self.wall_jump_used = False
            sound_manager.play_sound('jump')
            self.start_jump()
        elif self.jump_count < 2:
            self.vy = -15.0
            self.jump_count += 1
            sound_manager.play_sound('jump')
            self.start_jump()
        elif self.on_wall and not self.wall_jump_used:
            self.vy = -20.0
            self.vx = -self.wall_dir * 25
            if self.jump_count == 2:
                self.jump_count = 1
            self.wall_jump_used = True
            
            effect_manager.add_effect(
                self.rect.centerx,
                self.rect.centery,
                'wall_jump',
                direction=self.wall_dir,
                count=15
            )
            
            sound_manager.play_sound('jump')
            self.start_jump()

    def take_damage(self):
        if not self.is_invulnerable:
            self.health -= 1
            if self.health <= 0:
                self.alive = False
                return True
        return False
    
    def draw(self, camera_x, camera_y):
        if not self.alive:
            return
            
        self.draw_dash_trails(camera_x, camera_y)
            
        if self.is_jumping:
            current_image = self.jump_sprites[self.current_jump_sprite]
            
            if not self.facing_right:
                current_image = pygame.transform.flip(current_image, True, False)
            
            y_offset = self.rect.y - (85 - 60)
            
            if self.is_invulnerable and pygame.time.get_ticks() % 200 < 100:
                current_image = current_image.copy()
                alpha_surface = pygame.Surface(current_image.get_size(), pygame.SRCALPHA)
                alpha_surface.fill((255, 255, 255, 128))
                current_image.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            screen.blit(current_image, (self.rect.x - camera_x, y_offset - camera_y))
        else:
            current_image = self.sprites[self.current_sprite]
            
            if not self.facing_right:
                current_image = pygame.transform.flip(current_image, True, False)
            
            if self.is_invulnerable and pygame.time.get_ticks() % 200 < 100:
                current_image = current_image.copy()
                alpha_surface = pygame.Surface(current_image.get_size(), pygame.SRCALPHA)
                alpha_surface.fill((255, 255, 255, 128))
                current_image.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            screen.blit(current_image, (self.rect.x - camera_x, self.rect.y - camera_y))

class FlyingEnemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 40)
        self.vx = 0.0
        self.vy = 0.0
        self.max_speed = 8.0
        self.acceleration = 0.3
        self.deceleration = 0.1
        self.health = 40
        self.max_health = 40
        self.score_value = 150
        self.alive = True
        self.avoid_timer = 0
        
        self.animation_sheet = pygame.image.load("images/enemy_fly.png").convert_alpha()
        self.sprite_width = 80
        self.sprite_height = 40
        self.sprite_count = 4
        self.sprites = []
        self.current_sprite = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
        self.facing_right = True
        
        for i in range(self.sprite_count):
            sprite_rect = pygame.Rect(i * self.sprite_width, 0, self.sprite_width, self.sprite_height)
            sprite = self.animation_sheet.subsurface(sprite_rect)
            sprite = pygame.transform.flip(sprite, True, False)
            self.sprites.append(sprite)
            
    def update_animation(self, dt):
        if not self.alive:
            return
            
        self.animation_timer += dt * self.animation_speed
        
        if self.animation_timer >= 1:
            self.current_sprite = (self.current_sprite + 1) % self.sprite_count
            self.animation_timer = 0
            
        if abs(self.vx) > 0.1:
            self.facing_right = self.vx > 0
            
    def update(self, player):
        if not self.alive or not player.alive:
            return
            
        if self.avoid_timer > 0:
            self.avoid_timer -= 1
            
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
        
        target_dx = dx / distance
        target_dy = dy / distance
        
        avoid_x, avoid_y = self.check_obstacles(target_dx, target_dy)
        
        final_dx = target_dx + avoid_x * 2.0
        final_dy = target_dy + avoid_y * 2.0
        
        final_length = max(math.sqrt(final_dx*final_dx + final_dy*final_dy), 0.1)
        final_dx /= final_length
        final_dy /= final_length
        
        self.vx += final_dx * self.acceleration
        self.vy += final_dy * self.acceleration
        
        speed = math.sqrt(self.vx*self.vx + self.vy*self.vy)
        if speed > self.max_speed:
            self.vx = (self.vx / speed) * self.max_speed
            self.vy = (self.vy / speed) * self.max_speed
            
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        self.update_animation(1)
        
        self.handle_collisions()
            
    def check_obstacles(self, target_dx, target_dy):
        avoid_x, avoid_y = 0, 0
        
        check_distance = 100
        check_points = [
            (self.rect.centerx + target_dx * check_distance, self.rect.centery + target_dy * check_distance),
            (self.rect.centerx + target_dx * check_distance * 0.7, self.rect.centery),
            (self.rect.centerx, self.rect.centery + target_dy * check_distance * 0.7)
        ]
        
        for point_x, point_y in check_points:
            check_rect = pygame.Rect(point_x - 20, point_y - 20, 40, 40)
            for plat in platforms:
                if check_rect.colliderect(plat):
                    dx_avoid = self.rect.centerx - plat.centerx
                    dy_avoid = self.rect.centery - plat.centery
                    avoid_length = max(math.sqrt(dx_avoid*dx_avoid + dy_avoid*dy_avoid), 0.1)
                    avoid_x += dx_avoid / avoid_length * 0.5
                    avoid_y += dy_avoid / avoid_length * 0.5
                    self.avoid_timer = 10
        
        if self.avoid_timer > 0:
            avoid_x += random.uniform(-0.5, 0.5)
            avoid_y += random.uniform(-0.5, 0.5)
            
        return avoid_x, avoid_y
        
    def handle_collisions(self):
        for plat in platforms:
            if self.rect.colliderect(plat):
                dx_collision = self.rect.centerx - plat.centerx
                dy_collision = self.rect.centery - plat.centery
        
                if abs(dx_collision) > abs(dy_collision):
                    if dx_collision > 0:
                        self.rect.left = plat.right
                    else:
                        self.rect.right = plat.left
                    self.vx *= -0.7
                else:
                    if dy_collision > 0:
                        self.rect.top = plat.bottom
                    else:
                        self.rect.bottom = plat.top
                    self.vy *= -0.7
                    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False
        
    def draw(self, camera_x, camera_y):
        if not self.alive:
            return
            
        current_image = self.sprites[self.current_sprite]
        
        if not self.facing_right:
            current_image = pygame.transform.flip(current_image, True, False)
        
        screen.blit(current_image, (self.rect.x - camera_x, self.rect.y - camera_y))
        
        health_width = (self.health / self.max_health) * self.rect.width
        pygame.draw.rect(screen, RED, (self.rect.x - camera_x, self.rect.y - camera_y - 10, 
                                     self.rect.width, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x - camera_x, self.rect.y - camera_y - 10, 
                                       health_width, 5))

class GroundEnemy:
    def __init__(self, x, y, platform):
        self.rect = pygame.Rect(x, y, 40, 80)
        self.platform = platform
        self.platform_group = self.find_platform_group(platform)
        self.vx = 2.0
        self.vy = 0.0
        self.health = 100
        self.max_health = 100
        self.patrol_speed = 2.0
        self.charge_speed = 6.0
        self.is_charging = False
        self.charge_direction = 0
        self.player_spotted = False
        self.score_value = 100
        self.alive = True
        self.charge_cooldown = 0
        self.on_ground = False
        self.patrol_direction = 1
        self.patrol_timer = 0
        self.idle_timer = 0
        self.last_player_x = 0
        self.attack_range = 800
        self.pursuit_range = 1000
        
        self.animation_sheet = pygame.image.load("images/enemy_ground.png").convert_alpha()
        self.sprite_width = 40
        self.sprite_height = 80
        self.sprite_count = 4
        self.sprites = []
        self.current_sprite = 0
        self.animation_speed = 0.15
        self.animation_timer = 0
        self.facing_right = True
        
        for i in range(self.sprite_count):
            sprite_rect = pygame.Rect(i * self.sprite_width, 0, self.sprite_width, self.sprite_height)
            sprite = self.animation_sheet.subsurface(sprite_rect)
            sprite = pygame.transform.flip(sprite, True, False)
            self.sprites.append(sprite)
            
    def update_animation(self, dt):
        if not self.alive:
            return
            
        if abs(self.vx) > 0.1:
            self.animation_timer += dt * self.animation_speed
            
            if self.animation_timer >= 1:
                self.current_sprite = (self.current_sprite + 1) % self.sprite_count
                self.animation_timer = 0
        else:
            self.current_sprite = 0
            
        if abs(self.vx) > 0.1:
            self.facing_right = self.vx > 0
    
    def find_platform_group(self, start_platform):
        visited = []
        stack = [start_platform]
        platform_group = []
        
        while stack:
            current = stack.pop()
            if current in visited:
                continue
                
            visited.append(current)
            platform_group.append(current)
            
            for plat in platforms:
                if plat not in visited:
                    if (abs(current.top - plat.top) < 10 and 
                        ((current.right >= plat.left - 5 and current.right <= plat.left + 5) or
                         (current.left >= plat.right - 5 and current.left <= plat.right + 5))):
                        stack.append(plat)
        
        return platform_group
    
    def get_platform_bounds(self):
        if not self.platform_group:
            return self.platform
            
        left = min(plat.left for plat in self.platform_group)
        right = max(plat.right for plat in self.platform_group)
        top = min(plat.top for plat in self.platform_group)
        
        return pygame.Rect(left, top, right - left, self.platform.height)
    
    def update(self, player):
        if not self.alive or not player.alive:
            return
            
        self.vy += GRAVITY * 0.5
        if self.vy > 10:
            self.vy = 10
            
        self.platform_group = self.find_platform_group(self.platform)
        platform_bounds = self.get_platform_bounds()
        
        self.last_player_x = player.rect.centerx
        
        player_visible, player_direction = self.check_player_visibility(player)
        
        if player_visible and self.charge_cooldown <= 0:
            self.player_spotted = True
            self.is_charging = True
            self.charge_direction = player_direction
            self.vx = self.charge_speed * self.charge_direction
            
        elif self.is_charging:
            if player_visible:
                self.charge_direction = player_direction
                self.vx = self.charge_speed * self.charge_direction
            else:
                self.is_charging = False
                self.player_spotted = False
                self.charge_cooldown = 60
                
        elif self.charge_cooldown > 0:
            self.charge_cooldown -= 1
            self.vx = 0
            
        else:
            self.patrol_timer += 1
            
            if self.patrol_timer >= 300 or self.at_platform_group_edge(platform_bounds):
                self.patrol_direction *= -1
                self.patrol_timer = 0
                self.idle_timer = 20
            
            if self.idle_timer > 0:
                self.idle_timer -= 1
                self.vx = 0
            else:
                self.vx = self.patrol_speed * self.patrol_direction
        
        self.update_animation(1)
        
        self.rect.x += self.vx
        
        for plat in platforms:
            if self.rect.colliderect(plat) and plat not in self.platform_group:
                if self.vx > 0:
                    self.rect.right = plat.left
                    if self.is_charging:
                        self.is_charging = False
                        self.charge_cooldown = 30
                    else:
                        self.patrol_direction = -1
                        self.patrol_timer = 0
                    break
                elif self.vx < 0:
                    self.rect.left = plat.right
                    if self.is_charging:
                        self.is_charging = False
                        self.charge_cooldown = 30
                    else:
                        self.patrol_direction = 1
                        self.patrol_timer = 0
                    break
        
        if self.rect.left < platform_bounds.left:
            self.rect.left = platform_bounds.left
            if self.is_charging:
                self.is_charging = False
                self.charge_cooldown = 30
            else:
                self.patrol_direction = 1
                self.patrol_timer = 0
                
        if self.rect.right > platform_bounds.right:
            self.rect.right = platform_bounds.right
            if self.is_charging:
                self.is_charging = False
                self.charge_cooldown = 30
            else:
                self.patrol_direction = -1
                self.patrol_timer = 0
            
        self.rect.y += self.vy
        self.on_ground = False
        
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vy > 0:
                    self.rect.bottom = plat.top
                    self.vy = 0
                    self.on_ground = True
                    if plat != self.platform:
                        self.platform = plat
                        self.platform_group = self.find_platform_group(plat)
                    break
                elif self.vy < 0:
                    self.rect.top = plat.bottom
                    self.vy = 0
                    break
    
    def at_platform_group_edge(self, platform_bounds):
        edge_margin = 15
        if self.patrol_direction > 0:
            return self.rect.right >= platform_bounds.right - edge_margin
        else:
            return self.rect.left <= platform_bounds.left + edge_margin
            
    def check_player_visibility(self, player):
        if not player.alive:
            return False, 0
            
        dx = player.rect.centerx - self.rect.centerx
        horizontal_distance = abs(dx)
        
        if horizontal_distance > self.attack_range:
            return False, 0
            
        if abs(player.rect.centery - self.rect.centery) > 150:
            return False, 0
            
        player_platform = self.find_player_platform(player)
        if not player_platform:
            return False, 0
            
        player_direction = 1 if dx > 0 else -1
        
        player_platform_group = self.find_platform_group(player_platform)
        
        if any(plat in player_platform_group for plat in self.platform_group):
            return True, player_direction
            
        return False, 0
    
    def find_player_platform(self, player):
        for plat in platforms:
            if (abs(player.rect.bottom - plat.top) < 20 and 
                plat.left <= player.rect.centerx <= plat.right):
                return plat
        return None
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False
        
    def draw(self, camera_x, camera_y):
        if not self.alive:
            return
            
        current_image = self.sprites[self.current_sprite]
        
        if not self.facing_right:
            current_image = pygame.transform.flip(current_image, True, False)
        
        screen.blit(current_image, (self.rect.x - camera_x, self.rect.y - camera_y))
        
        health_width = (self.health / self.max_health) * self.rect.width
        pygame.draw.rect(screen, RED, (self.rect.x - camera_x, self.rect.y - camera_y - 10, 
                                     self.rect.width, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x - camera_x, self.rect.y - camera_y - 10, 
                                       health_width, 5))

class EnemySpawner:
    def __init__(self):
        self.ground_enemies = []
        self.flying_enemies = []
        self.ground_spawn_timer = 0
        self.ground_spawn_interval = 2 * FPS
        self.max_ground_enemies_per_platform = 2
        self.max_flying_enemies = 2
        self.max_total_ground_enemies = 100
        self.spawn_safe_distance = 200

        self.last_ground_enemy_hp = 100
        self.last_flying_enemy_hp = 40

    def can_spawn_ground_enemy_on_platform(self, platform, player):
        if self.is_too_close_to_player(platform.centerx, platform.centery, player):
            return False
            
        platform_top = platform.top
        platform_mid_x = platform.centerx
        
        check_height = 200
        check_rect = pygame.Rect(platform_mid_x - 10, platform_top - check_height, 20, check_height)
        
        for plat in platforms:
            if plat != platform and check_rect.colliderect(plat):
                return False
        
        has_left_platform = False
        has_right_platform = False
        
        left_check_rect = pygame.Rect(platform.left - BLOCK_SIZE - 5, platform.top, 10, platform.height)
        right_check_rect = pygame.Rect(platform.right + 5, platform.top, 10, platform.height)
        
        for plat in platforms:
            if plat != platform:
                if left_check_rect.colliderect(plat):
                    has_left_platform = True
                if right_check_rect.colliderect(plat):
                    has_right_platform = True
                
                if has_left_platform and has_right_platform:
                    break
        
        return has_left_platform and has_right_platform

    def update(self, player):
        if not player.alive:
            return
            
        self.ground_spawn_timer += 1
        
        alive_ground = len([e for e in self.ground_enemies if e.alive])
        if (self.ground_spawn_timer >= self.ground_spawn_interval and 
            alive_ground < self.max_total_ground_enemies):
            self.spawn_ground_enemies(player)
            self.ground_spawn_timer = 0
            
        alive_flying = len([e for e in self.flying_enemies if e.alive])
        if alive_flying < self.max_flying_enemies and random.random() < 0.02:
            self.spawn_flying_enemy(player)
            
        self.ground_enemies = [enemy for enemy in self.ground_enemies if enemy.alive]
        self.flying_enemies = [enemy for enemy in self.flying_enemies if enemy.alive]
            
        for enemy in self.ground_enemies:
            enemy.update(player)
            
        for enemy in self.flying_enemies:
            enemy.update(player)
            
        for enemy in self.ground_enemies + self.flying_enemies:
            if enemy.alive and player.rect.colliderect(enemy.rect):
                player.take_damage()
                break
    
    def is_too_close_to_player(self, x, y, player):
        if not player.alive:
            return False
            
        dx = abs(x - player.rect.centerx)
        dy = abs(y - player.rect.centery)
        
        return dx < self.spawn_safe_distance and dy < self.spawn_safe_distance
    
    def spawn_ground_enemies(self, player):
        suitable_platforms = []
        
        for plat in platforms:
            if self.can_spawn_ground_enemy_on_platform(plat, player):
                suitable_platforms.append(plat)
        
        if not suitable_platforms:
            return
            
        platform = random.choice(suitable_platforms)
        
        attempts = 0
        while attempts < 20:
            x = random.randint(platform.left, platform.right)
            y = platform.top - 80
            
            if not self.is_too_close_to_player(x, y, player):
                enemy = GroundEnemy(x, y, platform)
                enemy.health = self.last_ground_enemy_hp
                enemy.max_health = self.last_ground_enemy_hp
                self.ground_enemies.append(enemy)
                break
                
            attempts += 1
    
    def spawn_flying_enemy(self, player):
        attempts = 0
        while attempts < 50:
            x = random.randint(100, SCREEN_WIDTH * 2 - 100)
            y = random.randint(100, SCREEN_HEIGHT - 200)
            
            if self.is_too_close_to_player(x, y, player):
                attempts += 1
                continue
            
            spawn_rect = pygame.Rect(x, y, 80, 40)
            
            collision = False
            for plat in platforms:
                if spawn_rect.colliderect(plat):
                    collision = True
                    break
                    
            for enemy in self.flying_enemies:
                if enemy.alive and spawn_rect.colliderect(enemy.rect):
                    collision = True
                    break
                    
            if not collision:
                enemy = FlyingEnemy(x, y)
                enemy.health = self.last_flying_enemy_hp
                enemy.max_health = self.last_flying_enemy_hp
                self.flying_enemies.append(enemy)
                break
                
            attempts += 1
    
    def draw(self, camera_x, camera_y):
        for enemy in self.ground_enemies:
            enemy.draw(camera_x, camera_y)
            
        for enemy in self.flying_enemies:
            enemy.draw(camera_x, camera_y)

class Bullet:
    def __init__(self, x, y, direction, weapon_type):
        self.x = x
        self.y = y
        self.direction = direction
        self.weapon_type = weapon_type
        self.damage = 15
        self.initial_damage = 15
        
        self.lifetime = 0
        self.slowdown_start = 60
        self.damage_reduction_start = 90
        self.is_slowing_down = False
        
        if weapon_type == 1:
            self.speed = 15.0
            self.width = 18
            self.height = 6
        else:
            self.speed = 30.0
            self.width = 12
            self.height = 4
            
        self.dx = direction[0] * self.speed
        self.dy = direction[1] * self.speed
        self.initial_dx = self.dx
        self.initial_dy = self.dy
        
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)
        
    def update(self, camera_x, camera_y, time_scale):
        self.lifetime += 1
        
        if self.lifetime >= self.slowdown_start and not self.is_slowing_down:
            self.is_slowing_down = True
            self.dx *= 0.98
            self.dy *= 0.95
        
        if self.is_slowing_down:
            self.dx *= 0.98
            self.dy *= 0.98
            self.dy += 0.2
            
        if self.lifetime >= self.damage_reduction_start:
            self.damage = max(0, self.damage * 0.9)
        
        self.x += self.dx * time_scale
        self.y += self.dy * time_scale
        
        self.rect.x = self.x - self.width//2
        self.rect.y = self.y - self.height//2
        
        for plat in platforms:
            if self.rect.colliderect(plat):
                effect_manager.add_effect(
                    self.rect.centerx,
                    self.rect.centery,
                    'bullet_impact',
                    count=8 if self.weapon_type == 1 else 12
                )
                return False
                
        screen_left = camera_x
        screen_right = camera_x + SCREEN_WIDTH
        screen_top = camera_y
        screen_bottom = camera_y + SCREEN_HEIGHT
        
        if (self.rect.right < screen_left or self.rect.left > screen_right or 
            self.rect.bottom < screen_top or self.rect.top > screen_bottom):
            return False
            
        return True
        
    def draw(self, camera_x, camera_y):
        angle = math.atan2(self.dy, self.dx)
        angle_degrees = math.degrees(angle)
        
        if self.weapon_type == 1:
            bullet_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.ellipse(bullet_surface, BLACK, (0, 0, self.width, self.height))
            
            glow_surface = pygame.Surface((self.width + 4, self.height + 4), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surface, (100, 100, 100, 100), (0, 0, self.width + 4, self.height + 4))
            
            rotated_glow = pygame.transform.rotate(glow_surface, -angle_degrees)
            rotated_bullet = pygame.transform.rotate(bullet_surface, -angle_degrees)
            
            glow_rect = rotated_glow.get_rect(center=(self.x - camera_x, self.y - camera_y))
            bullet_rect = rotated_bullet.get_rect(center=(self.x - camera_x, self.y - camera_y))
            
            screen.blit(rotated_glow, glow_rect)
            screen.blit(rotated_bullet, bullet_rect)
            
        else:
            bullet_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(bullet_surface, BLACK, (0, 0, self.width, self.height))
            
            tip_color = (255, 0, 0)
            if self.direction[0] > 0:
                pygame.draw.rect(bullet_surface, tip_color, (self.width - 3, 0, 3, self.height))
            elif self.direction[0] < 0:
                pygame.draw.rect(bullet_surface, tip_color, (0, 0, 3, self.height))
            elif self.direction[1] > 0:
                pygame.draw.rect(bullet_surface, tip_color, (0, self.height - 3, self.width, 3))
            else:
                pygame.draw.rect(bullet_surface, tip_color, (0, 0, self.width, 3))
            
            rotated_bullet = pygame.transform.rotate(bullet_surface, -angle_degrees)
            bullet_rect = rotated_bullet.get_rect(center=(self.x - camera_x, self.y - camera_y))
            
            screen.blit(rotated_bullet, bullet_rect)

class Weapon:
    def __init__(self, x, y, weapon_type, is_front):
        self.weapon_type = weapon_type
        self.is_front = is_front
        self.sheet_name = f"images/{weapon_type}{'l' if is_front else 'r'}.png"
        self.sheet = pygame.image.load(self.sheet_name).convert_alpha()
        self.sprite_size = 128
        self.sprites = []
        
        for i in range(5):
            sprite_rect = pygame.Rect(i * self.sprite_size, 0, self.sprite_size, self.sprite_size)
            sprite = self.sheet.subsurface(sprite_rect)
            self.sprites.append(sprite)
            
        self.current_sprite = 2
        self.rect = pygame.Rect(x - 64, y - 64, self.sprite_size, self.sprite_size)
    
    def update_weapon_type(self, weapon_type, is_front):
        if self.weapon_type != weapon_type:
            self.weapon_type = weapon_type
            self.sheet_name = f"images/{weapon_type}{'l' if is_front else 'r'}.png"
            self.sheet = pygame.image.load(self.sheet_name).convert_alpha()
            self.sprites = []
            for i in range(5):
                sprite_rect = pygame.Rect(i * self.sprite_size, 0, self.sprite_size, self.sprite_size)
                sprite = self.sheet.subsurface(sprite_rect)
                self.sprites.append(sprite)
    
    def update_position(self, player_x, player_y, angle, facing_right):
        self.rect.centerx = player_x
        self.rect.centery = player_y
        
        normalized_angle = angle % (2 * math.pi)
        if normalized_angle < 0:
            normalized_angle += 2 * math.pi
        
        if normalized_angle >= math.pi/8 and normalized_angle < 3*math.pi/8:
            self.current_sprite = 1
        elif normalized_angle >= 3*math.pi/8 and normalized_angle < 5*math.pi/8:
            self.current_sprite = 0
        elif normalized_angle >= 5*math.pi/8 and normalized_angle < 7*math.pi/8:
            self.current_sprite = 1
        elif normalized_angle >= 7*math.pi/8 and normalized_angle < 9*math.pi/8:
            self.current_sprite = 2
        elif normalized_angle >= 9*math.pi/8 and normalized_angle < 11*math.pi/8:
            self.current_sprite = 3
        elif normalized_angle >= 11*math.pi/8 and normalized_angle < 13*math.pi/8:
            self.current_sprite = 4
        elif normalized_angle >= 13*math.pi/8 and normalized_angle < 15*math.pi/8:
            self.current_sprite = 3
        else:
            self.current_sprite = 2
    
    def draw(self, camera_x, camera_y, facing_right):
        current_sprite = self.sprites[self.current_sprite]
        
        flip_x = False
        if not facing_right and self.current_sprite in [0, 1, 2, 3, 4]:
            flip_x = True
        elif facing_right and self.current_sprite in [1, 3] and self.current_sprite == 1:
            flip_x = False
        
        if flip_x:
            current_sprite = pygame.transform.flip(current_sprite, True, False)
        
        screen.blit(current_sprite, (self.rect.x - camera_x, self.rect.y - camera_y))

class Mouseusing:
    def __init__(self):
        self.leftweapon, self.rightweapon = 1, 1
        self.front_weapon = None
        self.back_weapon = None
        self.bullets = []
        
        self.shot_count = 0
        self.cooldown_timer = 0
        self.cooldown_active = False
        
        self.l_shot_count = 0
        self.l_cooldown_active = False
        self.l_cooldown_timer = 0
        self.l_cooldown_frames = 5
        
        self.r_shot_count = 0
        self.r_cooldown_active = False
        self.r_cooldown_timer = 0
        self.r_cooldown_frames = 5
    
    def can_shoot(self):
        return not self.cooldown_active and self.shot_count < 6
    
    def can_left_shoot(self):
        return self.can_shoot() and not self.l_cooldown_active
    
    def can_right_shoot(self):
        return self.can_shoot() and not self.r_cooldown_active
    
    def left_click(self, player_x, player_y, target_angle):
        if self.can_left_shoot():
            self.l_shot_count += 1
            self.shot_count += 1
            weapon_type = self.leftweapon
            
            if weapon_type == 1:
                sound_manager.play_sound('shotgun')
            else:
                sound_manager.play_sound('rifle')
            
            if weapon_type == 1:
                menu_manager.add_screen_shake(8, 10)
            elif weapon_type == 2:
                menu_manager.add_screen_shake(3, 5)
            
            self.l_cooldown_active = True
            self.l_cooldown_timer = self.l_cooldown_frames
            self.shoot(player_x, player_y, target_angle, weapon_type)
            
            if self.shot_count >= 6:
                self.cooldown_active = True
                self.cooldown_timer = 40
                sound_manager.play_reload_sound()
    
    def right_click(self, player_x, player_y, target_angle):
        if self.can_right_shoot():
            self.r_shot_count += 1
            self.shot_count += 1
            weapon_type = self.rightweapon
            
            if weapon_type == 1:
                sound_manager.play_sound('shotgun')
            else:
                sound_manager.play_sound('rifle')
            
            if weapon_type == 1:
                menu_manager.add_screen_shake(8, 10)
            elif weapon_type == 2:
                menu_manager.add_screen_shake(3, 5)
            
            self.r_cooldown_active = True
            self.r_cooldown_timer = self.r_cooldown_frames
            self.shoot(player_x, player_y, target_angle, weapon_type)
            
            if self.shot_count >= 6:
                self.cooldown_active = True
                self.cooldown_timer = 40
                sound_manager.play_reload_sound()
    
    def switch_weapon(self, weapon_num):
        if weapon_num == 1:
            self.leftweapon, self.rightweapon = 1, 2
        else:
            self.leftweapon, self.rightweapon = 2, 1
        
        if self.front_weapon:
            self.front_weapon.update_weapon_type(self.leftweapon, True)
        if self.back_weapon:
            self.back_weapon.update_weapon_type(self.rightweapon, False)
    
    def update_weapons_position(self, player_x, player_y, angle, facing_right):
        if self.front_weapon:
            self.front_weapon.update_position(player_x, player_y, angle, facing_right)
        if self.back_weapon:
            self.back_weapon.update_position(player_x, player_y, angle, facing_right)
    
    def create_weapons(self, player_x, player_y):
        if not self.front_weapon:
            self.front_weapon = Weapon(player_x, player_y, self.leftweapon, True)
        if not self.back_weapon:
            self.back_weapon = Weapon(player_x, player_y, self.rightweapon, False)
    
    def get_direction_from_angle(self, angle):
        directions = [
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1)
        ]
        
        normalized_angle = angle % (2 * math.pi)
        if normalized_angle < 0:
            normalized_angle += 2 * math.pi
        
        sector = int((normalized_angle + math.pi/8) / (math.pi/4)) % 8
        
        return directions[sector]
    
    def shoot(self, player_x, player_y, target_angle, weapon_type):
        main_direction = self.get_direction_from_angle(target_angle)
        
        if weapon_type == 1:
            bullet_count = 16
        else:
            bullet_count = 8
            
        for i in range(bullet_count):
            if weapon_type == 1:
                direction_variation = (
                    main_direction[0] + random.uniform(-0.3, 0.3),
                    main_direction[1] + random.uniform(-0.3, 0.3)
                )
                length = math.sqrt(direction_variation[0]**2 + direction_variation[1]**2)
                if length > 0:
                    direction = (direction_variation[0]/length, direction_variation[1]/length)
                else:
                    direction = main_direction
            else:
                direction_variation = (
                    main_direction[0] + random.uniform(-0.05, 0.05),
                    main_direction[1] + random.uniform(-0.05, 0.05)
                )
                length = math.sqrt(direction_variation[0]**2 + direction_variation[1]**2)
                if length > 0:
                    direction = (direction_variation[0]/length, direction_variation[1]/length)
                else:
                    direction = main_direction
            
            self.bullets.append(Bullet(player_x, player_y, direction, weapon_type))
    
    def update_cooldown(self):
        if self.l_cooldown_active:
            self.l_cooldown_timer -= 1
            if self.l_cooldown_timer <= 0:
                self.l_cooldown_active = False
        
        if self.r_cooldown_active:
            self.r_cooldown_timer -= 1
            if self.r_cooldown_timer <= 0:
                self.r_cooldown_active = False
        
        if self.cooldown_active:
            self.cooldown_timer -= 1
            if self.cooldown_timer <= 0:
                self.cooldown_active = False
                self.shot_count = 0
                self.l_shot_count = 0
                self.r_shot_count = 0
    
    def update_bullets(self, camera_x, camera_y, enemies, score):
        time_scale = 1.0
        
        bullets_to_remove = []
        enemies_to_remove = []
        
        for i, bullet in enumerate(self.bullets):
            if not bullet.update(camera_x, camera_y, time_scale):
                bullets_to_remove.append(i)
                continue
                
            for j, enemy in enumerate(enemies):
                if bullet.rect.colliderect(enemy.rect):
                    effect_manager.add_effect(
                        bullet.rect.centerx,
                        bullet.rect.centery,
                        'bullet_impact',
                        count=10 if bullet.weapon_type == 1 else 15
                    )
                    
                    if enemy.take_damage(bullet.damage):
                        enemies_to_remove.append(j)
                        score[0] += enemy.score_value
                        
                        if isinstance(enemy, GroundEnemy):
                            enemy_spawner.last_ground_enemy_hp = int(enemy_spawner.last_ground_enemy_hp * 1.05)
                            print(f"GroundEnemy HP increased to: {enemy_spawner.last_ground_enemy_hp}")
                        elif isinstance(enemy, FlyingEnemy):
                            enemy_spawner.last_flying_enemy_hp = int(enemy_spawner.last_flying_enemy_hp * 1.05)
                            print(f"FlyingEnemy HP increased to: {enemy_spawner.last_flying_enemy_hp}")
                    
                    bullets_to_remove.append(i)
                    break
        
        for i in sorted(bullets_to_remove, reverse=True):
            if i < len(self.bullets):
                self.bullets.pop(i)
                
        for j in sorted(enemies_to_remove, reverse=True):
            if j < len(enemies):
                enemies.pop(j)
    
    def draw_weapons(self, camera_x, camera_y, facing_right):
        if self.back_weapon:
            self.back_weapon.draw(camera_x, camera_y, facing_right)
    
    def draw_front_weapon(self, camera_x, camera_y, facing_right):
        if self.front_weapon:
            self.front_weapon.draw(camera_x, camera_y, facing_right)
    
    def draw_bullets(self, camera_x, camera_y):
        for bullet in self.bullets:
            bullet.draw(camera_x, camera_y)

class MenuManager:
    def __init__(self):
        try:
            self.menu_sheet = pygame.image.load("images/menu.png").convert_alpha()
        except:
            print("Ошибка загрузки images/menu.png")
            self.menu_sheet = None
            return
            
        self.sheet_width = 7760
        self.sheet_height = 1080
        self.frame_width = 1920
        self.frame_height = 1080
        self.total_frames = 4
        self.screen_shake = 0
        self.shake_intensity = 0
        
        self.frames = []
        for i in range(self.total_frames):
            frame_rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame = self.menu_sheet.subsurface(frame_rect)
            self.frames.append(frame)
            
        self.menu_open = False
        
        self.weapon1_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2 + 100, 200, 80)
        self.weapon2_button_rect = pygame.Rect(SCREEN_WIDTH//2 + 100, SCREEN_HEIGHT//2 + 100, 200, 80)
        self.close_button_rect = pygame.Rect(SCREEN_WIDTH - 220, 50, 170, 60)
        
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.weapon_descriptions = {
            1: {
                "name": "ДРОБОВИК",
                "damage": "15 урона за пулю",
                "bullets": "16 пуль за выстрел", 
                "speed": "Средняя скорость",
                "spread": "Высокий разброс",
                "description": "Мощное оружие ближнего боя"
            },
            2: {
                "name": "ВИНТОВКА", 
                "damage": "15 урона за пулю",
                "bullets": "8 пуль за выстрел",
                "speed": "Высокая скорость",
                "spread": "Низкий разброс",
                "description": "Точное оружие дальнего боя"
            }
        }
        self.death_restart_button = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 50, 300, 80)
        self.death_menu_button = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 150, 300, 80)
        self.death_quit_button = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 250, 300, 80)

    def draw_death_screen(self, screen, score):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        container_rect = pygame.Rect(SCREEN_WIDTH//2 - 400, SCREEN_HEIGHT//2 - 300, 800, 600)
        pygame.draw.rect(screen, (40, 40, 40), container_rect)
        pygame.draw.rect(screen, WHITE, container_rect, 4)
        
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("ВЫ ПОГИБЛИ", True, RED)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//2 - 250))
        
        stats_font = pygame.font.Font(None, 48)
        score_text = stats_font.render(f"Счёт: {score[0]}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 - 150))
        
        self.draw_death_button(screen, self.death_restart_button, "Попробовать снова", GREEN)
        self.draw_death_button(screen, self.death_menu_button, "Вернуться в меню", BLUE)
        self.draw_death_button(screen, self.death_quit_button, "Выйти из игры", RED)
        
        hint_font = pygame.font.Font(None, 36)
        hint_text = hint_font.render("R - Быстрый рестарт", True, YELLOW)
        screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, SCREEN_HEIGHT//2 + 350))
    
    def draw_death_button(self, screen, rect, text, color):
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, WHITE, rect, 3)
        
        text_surf = self.font_large.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            highlight = pygame.Surface(rect.size, pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 50))
            screen.blit(highlight, rect)

    def handle_death_screen_events(self, event, player, weapon_system, enemy_spawner, score, main_menu):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            sound_manager.play_sound('button')
            
            if self.death_restart_button.collidepoint(event.pos):
                pygame.mouse.set_visible(False)
                return self.restart_game(player, weapon_system, enemy_spawner, score)
            elif self.death_menu_button.collidepoint(event.pos):
                main_menu.active = True
                pygame.mouse.set_visible(True)
                return "main_menu"
            elif self.death_quit_button.collidepoint(event.pos):
                return "quit"
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                pygame.mouse.set_visible(False)
                return self.restart_game(player, weapon_system, enemy_spawner, score)
            elif event.key == pygame.K_ESCAPE:
                return "quit"
            elif event.key == pygame.K_m:
                main_menu.active = True
                pygame.mouse.set_visible(True)
                return "main_menu"
        
        return False
    
    def restart_game(self, player, weapon_system, enemy_spawner, score):
        player = Player(px, py)
        weapon_system = Mouseusing()
        enemy_spawner = EnemySpawner()
        score[0] = 0
        weapon_system.create_weapons(player.rect.centerx, player.rect.centery)
        texture_manager.assign_textures()
        return player, weapon_system, enemy_spawner
    
    def add_screen_shake(self, intensity, duration):
        self.screen_shake = duration
        self.shake_intensity = intensity
    
    def update_screen_shake(self):
        if self.screen_shake > 0:
            self.screen_shake -= 1
            return True
        return False
    
    def get_screen_offset(self):
        if self.screen_shake > 0:
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            return offset_x, offset_y
        return 0, 0
    
    def handle_event(self, event, weapon_system):
        if not self.menu_open:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            sound_manager.play_sound('button')
            
            if self.weapon1_button_rect.collidepoint(event.pos):
                weapon_system.leftweapon = 3 - weapon_system.leftweapon
                if weapon_system.front_weapon:
                    weapon_system.front_weapon.update_weapon_type(weapon_system.leftweapon, True)
                return True
                
            elif self.weapon2_button_rect.collidepoint(event.pos):
                weapon_system.rightweapon = 3 - weapon_system.rightweapon
                if weapon_system.back_weapon:
                    weapon_system.back_weapon.update_weapon_type(weapon_system.rightweapon, False)
                return True
                
            elif self.close_button_rect.collidepoint(event.pos):
                pygame.mouse.set_visible(False)
                self.menu_open = False
                return True
                
        return False
    
    def toggle_menu(self):
        self.menu_open = not self.menu_open
        pygame.mouse.set_visible(self.menu_open)
        sound_manager.play_sound('button')
        return self.menu_open
    
    def draw_weapon_info(self, screen, weapon_type, x, y):
        desc = self.weapon_descriptions[weapon_type]
        
        info_rect = pygame.Rect(x - 150, y + 120, 300, 220)
        bg_surface = pygame.Surface((300, 220), pygame.SRCALPHA)
        bg_surface.fill((80, 80, 80, 220))
        screen.blit(bg_surface, info_rect)
        
        pygame.draw.rect(screen, WHITE, info_rect, 2)
        
        name_text = self.font_medium.render(desc["name"], True, YELLOW)
        damage_text = self.font_small.render(desc["damage"], True, WHITE)
        bullets_text = self.font_small.render(desc["bullets"], True, WHITE)
        speed_text = self.font_small.render(desc["speed"], True, WHITE)
        spread_text = self.font_small.render(desc["spread"], True, WHITE)
        desc_text = self.font_small.render(desc["description"], True, WHITE)
        
        screen.blit(name_text, (x - name_text.get_width()//2, y + 140))
        screen.blit(damage_text, (x - 140, y + 180))
        screen.blit(bullets_text, (x - 140, y + 200))
        screen.blit(speed_text, (x - 140, y + 220))
        screen.blit(spread_text, (x - 140, y + 240))
        screen.blit(desc_text, (x - 140, y + 270))
    
    def draw_button(self, screen, rect, text, is_close_button=False):
        button_color = (120, 120, 120) if not is_close_button else (180, 60, 60)
        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, WHITE, rect, 2)
        
        if is_close_button:
            text_surf = self.font_medium.render(text, True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
        else:
            arrow_points = [
                (rect.centerx, rect.top + 20),
                (rect.centerx - 15, rect.top + 50),
                (rect.centerx + 15, rect.top + 50)
            ]
            pygame.draw.polygon(screen, WHITE, arrow_points)
            
            text_surf = self.font_small.render(text, True, WHITE)
            text_rect = text_surf.get_rect(center=(rect.centerx, rect.bottom - 20))
            screen.blit(text_surf, text_rect)
    
    def draw(self, screen, weapon_system):
        if not self.menu_open or not self.menu_sheet:
            return
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        if weapon_system.leftweapon == 1:
            left_half = self.frames[0].subsurface(pygame.Rect(0, 0, self.frame_width//2, self.frame_height))
        else:
            left_half = self.frames[2].subsurface(pygame.Rect(0, 0, self.frame_width//2, self.frame_height))
            
        if weapon_system.rightweapon == 1:
            right_half = self.frames[1].subsurface(pygame.Rect(self.frame_width//2, 0, self.frame_width//2, self.frame_height))
        else:
            right_half = self.frames[3].subsurface(pygame.Rect(self.frame_width//2, 0, self.frame_width//2, self.frame_height))
        
        full_menu = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        full_menu.blit(left_half, (0, 0))
        full_menu.blit(right_half, (self.frame_width//2, 0))
        
        screen.blit(full_menu, (0, 0))
        
        self.draw_button(screen, self.weapon1_button_rect, "Сменить LMB")
        self.draw_button(screen, self.weapon2_button_rect, "Сменить RMB")
        
        self.draw_button(screen, self.close_button_rect, "Закрыть (I)", True)
        
        self.draw_weapon_info(screen, weapon_system.leftweapon, 
                            self.weapon1_button_rect.centerx, 
                            self.weapon1_button_rect.top)
        self.draw_weapon_info(screen, weapon_system.rightweapon,
                            self.weapon2_button_rect.centerx,
                            self.weapon2_button_rect.top)
        
        esc_text = self.font_medium.render("ESC - Выйти из игры", True, WHITE)
        r_text = self.font_medium.render("R - Перезапустить уровень", True, WHITE)
        close_text = self.font_medium.render("I - Закрыть меню", True, WHITE)
        
        screen.blit(esc_text, (20, SCREEN_HEIGHT - 120))
        screen.blit(r_text, (20, SCREEN_HEIGHT - 80))
        screen.blit(close_text, (20, SCREEN_HEIGHT - 40))

class MainMenu:
    def __init__(self):
        self.active = True
        self.buttons = {
            'start': pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50, 300, 80),
            'quit': pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 100, 300, 80)
        }
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        
    def handle_event(self, event, player, weapon_system, enemy_spawner, score):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            sound_manager.play_sound('button')
            
            if self.buttons['start'].collidepoint(event.pos):
                player, weapon_system, enemy_spawner = menu_manager.restart_game(player, weapon_system, enemy_spawner, score)
                self.active = False
                pygame.mouse.set_visible(False)
                return player, weapon_system, enemy_spawner
            elif self.buttons['quit'].collidepoint(event.pos):
                return "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                player, weapon_system, enemy_spawner = menu_manager.restart_game(player, weapon_system, enemy_spawner, score)
                self.active = False
                pygame.mouse.set_visible(False)
                return player, weapon_system, enemy_spawner
            elif event.key == pygame.K_ESCAPE:
                return "quit"
        return False
    
    def draw(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        title_text = self.font_large.render("КУБАНОИД", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//4))
        
        self.draw_button(screen, self.buttons['start'], "НАЧАТЬ ИГРУ", GREEN)
        self.draw_button(screen, self.buttons['quit'], "ВЫЙТИ", RED)
        
        hint_font = pygame.font.Font(None, 36)
        hint_text = hint_font.render("ENTER - Начать игру, ESC - Выйти", True, YELLOW)
        screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, SCREEN_HEIGHT - 100))
    
    def draw_button(self, screen, rect, text, color):
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, WHITE, rect, 3)
        
        text_surf = self.font_medium.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            highlight = pygame.Surface(rect.size, pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 50))
            screen.blit(highlight, rect)

menu_manager = MenuManager()
main_menu = MainMenu()

platforms = []
px, py = 0, 0
for ri, row in enumerate(level_map):
    for ci, c in enumerate(row):
        if c == "*":
            platforms.append(pygame.Rect(ci * BLOCK_SIZE, ri * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        elif c == "$":
            px, py = ci * BLOCK_SIZE, ri * BLOCK_SIZE

player = Player(px, py)
weapon_system = Mouseusing()
enemy_spawner = EnemySpawner()
interface_manager = InterfaceManager()
running = True
camera_x, camera_y = 0, 0
current_angle = 0.0
smoothness = 0.1
score = [0]

def normalize_angle(angle):
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle

weapon_system.create_weapons(player.rect.centerx, player.rect.centery)

texture_manager.assign_textures()

def draw_all(camera_x, camera_y, score):
    global current_angle, mouse_x, mouse_y
    
    screen.fill(BG_COLOR)
    
    texture_manager.draw_platforms(camera_x, camera_y)
    
    weapon_system.draw_weapons(camera_x, camera_y, player.facing_right)
    
    player.draw(camera_x, camera_y)
    
    weapon_system.draw_front_weapon(camera_x, camera_y, player.facing_right)
    
    enemy_spawner.draw(camera_x, camera_y)
    
    weapon_system.draw_bullets(camera_x, camera_y)
    
    effect_manager.draw(camera_x, camera_y)
    
    if not menu_manager.menu_open and player.alive and not main_menu.active:
        player_screen_x = player.rect.centerx - camera_x
        player_screen_y = player.rect.centery - camera_y
        green_circle_center = (player_screen_x, player_screen_y)
        
        dx = mouse_x - green_circle_center[0]
        dy = mouse_y - green_circle_center[1]
        
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 350:
            dx = dx * 350 / distance
            dy = dy * 350 / distance
        
        target_angle = math.atan2(dy, dx)
        
        current_angle_normalized = normalize_angle(current_angle)
        target_angle_normalized = normalize_angle(target_angle)
        
        angle_diff = target_angle_normalized - current_angle_normalized
        
        if angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        elif angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        current_angle += angle_diff * smoothness * player.time_scale
        current_angle = normalize_angle(current_angle)
        
        white_circle_x = green_circle_center[0] + 350 * math.cos(current_angle)
        white_circle_y = green_circle_center[1] + 350 * math.sin(current_angle)
        
        black_circle_world_x = white_circle_x + camera_x
        player.update_facing_direction(black_circle_world_x)
        
        pygame.draw.circle(screen, BLACK, (int(white_circle_x), int(white_circle_y)), 20)
        
def draw_interface(score, weapon_system):
    score_text = font.render(f"Очки: {score[0]}", True, WHITE)
    screen.blit(score_text, (20, 20))
    
    if not player.alive:
        pygame.mouse.set_visible(True)
        menu_manager.draw_death_screen(screen, score)

def draw_crosshair(camera_x, camera_y, mouse_x, mouse_y):
    global current_angle
    
    player_screen_x = player.rect.centerx - camera_x
    player_screen_y = player.rect.centery - camera_y
    green_circle_center = (player_screen_x, player_screen_y)
    
    dx = mouse_x - green_circle_center[0]
    dy = mouse_y - green_circle_center[1]
    
    distance = math.sqrt(dx*dx + dy*dy)
    if distance > 350:
        dx = dx * 350 / distance
        dy = dy * 350 / distance
    
    target_angle = math.atan2(dy, dx)
    
    current_angle_normalized = normalize_angle(current_angle)
    target_angle_normalized = normalize_angle(target_angle)
    
    angle_diff = target_angle_normalized - current_angle_normalized
    
    if angle_diff > math.pi:
        angle_diff -= 2 * math.pi
    elif angle_diff < -math.pi:
        angle_diff += 2 * math.pi

    current_angle += angle_diff * smoothness * player.time_scale
    current_angle = normalize_angle(current_angle)
    
    white_circle_x = green_circle_center[0] + 350 * math.cos(current_angle)
    white_circle_y = green_circle_center[1] + 350 * math.sin(current_angle)
    
    black_circle_world_x = white_circle_x + camera_x
    player.update_facing_direction(black_circle_world_x)
    
    pygame.draw.circle(screen, BLACK, (int(white_circle_x), int(white_circle_y)), 20)

while running:
    dt = clock.tick(FPS) / 16.6
    keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    menu_manager.update_screen_shake()
    shake_offset_x, shake_offset_y = menu_manager.get_screen_offset()
    
    sound_manager.update_music()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        
        if main_menu.active:
            result = main_menu.handle_event(event, player, weapon_system, enemy_spawner, score)
            if result == "quit":
                running = False
            elif result:
                player, weapon_system, enemy_spawner = result
                continue
        
        elif not player.alive:
            result = menu_manager.handle_death_screen_events(event, player, weapon_system, enemy_spawner, score, main_menu)
            if result == "quit":
                running = False
            elif result == "main_menu":
                continue
            elif result:
                if result[0]:
                    player, weapon_system, enemy_spawner = result
            continue
        
        elif menu_manager.menu_open:
            if menu_manager.handle_event(event, weapon_system):
                continue
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                    menu_manager.menu_open = False
                    pygame.mouse.set_visible(False)
                elif event.key == pygame.K_r:
                    player, weapon_system, enemy_spawner = menu_manager.restart_game(player, weapon_system, enemy_spawner, score)
                    menu_manager.menu_open = False
                    pygame.mouse.set_visible(False)
            continue
        
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(True)
                    menu_manager.menu_open = True
                elif event.key == pygame.K_i:
                    menu_manager.toggle_menu()
                elif event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_1:
                    weapon_system.switch_weapon(1)
                    weapon_system.create_weapons(player.rect.centerx, player.rect.centery)
                elif event.key == pygame.K_2:
                    weapon_system.switch_weapon(2)
                    weapon_system.create_weapons(player.rect.centerx, player.rect.centery)
                elif event.key == pygame.K_q:
                    player.start_dash(current_angle)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    weapon_system.left_click(player.rect.centerx, player.rect.centery, current_angle)
                elif event.button == 3:
                    weapon_system.right_click(player.rect.centerx, player.rect.centery, current_angle)
    
    if not main_menu.active and player.alive and not menu_manager.menu_open:
        player.move(keys, dt)
        player.update_animation(dt)
        
        weapon_system.update_weapons_position(player.rect.centerx, player.rect.centery, current_angle, player.facing_right)
        weapon_system.update_bullets(camera_x, camera_y, enemy_spawner.ground_enemies + enemy_spawner.flying_enemies, score)
        weapon_system.update_cooldown()
        
        enemy_spawner.update(player)
        
        target_camera_x = player.rect.centerx - SCREEN_WIDTH // 2
        target_camera_y = player.rect.centery - SCREEN_HEIGHT // 2
        
        camera_x += ((target_camera_x + shake_offset_x) - camera_x) * 0.1 * player.time_scale
        camera_y += ((target_camera_y + shake_offset_y) - camera_y) * 0.1 * player.time_scale
    
    effect_manager.update()
    
    interface_manager.update_state(weapon_system, player)
    
    screen.fill(BG_COLOR)
    
    if main_menu.active:
        main_menu.draw(screen)
    
    else:
        texture_manager.draw_platforms(camera_x - shake_offset_x, camera_y - shake_offset_y)
        weapon_system.draw_weapons(camera_x - shake_offset_x, camera_y - shake_offset_y, player.facing_right)
        player.draw(camera_x - shake_offset_x, camera_y - shake_offset_y)
        weapon_system.draw_front_weapon(camera_x - shake_offset_x, camera_y - shake_offset_y, player.facing_right)
        enemy_spawner.draw(camera_x - shake_offset_x, camera_y - shake_offset_y)
        weapon_system.draw_bullets(camera_x - shake_offset_x, camera_y - shake_offset_y)
        effect_manager.draw(camera_x - shake_offset_x, camera_y - shake_offset_y)
        
        if player.alive and not menu_manager.menu_open:
            draw_crosshair(camera_x - shake_offset_x, camera_y - shake_offset_y, mouse_x, mouse_y)
        
        interface_manager.draw(screen)
        draw_interface(score, weapon_system)
        
        if not player.alive:
            menu_manager.draw_death_screen(screen, score)
        
        menu_manager.draw(screen, weapon_system)
    
    pygame.display.flip()

pygame.quit()