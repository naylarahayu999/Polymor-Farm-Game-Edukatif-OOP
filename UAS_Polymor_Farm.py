import pygame
import sys
import random
from abc import ABC, abstractmethod

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 1200, 800
FPS = 60

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
BROWN = (139, 90, 43)
BLUE = (135, 206, 250)
YELLOW = (255, 215, 0)
RED = (220, 20, 60)
PINK = (255, 192, 203)
GOLD = YELLOW
LIGHT_BLUE = (173, 216, 230)
GRASS_GREEN = (124, 252, 0)
DARK_GREEN = (0, 100, 0)
GRAY = (160, 160, 160)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Polymor-Farm: The Shape-Shifting Farm")
clock = pygame.time.Clock()
font_small = pygame.font.Font(None, 28)
font_medium = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 56)
font_title = pygame.font.Font(None, 72)


# ==================== ENCAPSULATION ====================
# Base class dengan private attributes untuk protect internal state
class FarmEntity:
    """
    Base class untuk semua entity di farm.
    Implementasi ENCAPSULATION dengan private attributes.
    """
    def __init__(self, name, x, y):
        self.__name = name  # Private - tidak bisa diakses langsung
        self.__age = 0  # Private
        self.__happiness = 50  # Private - hidden mood (0-100)
        self.__health = 100  # Private
        self._x = x  # Protected
        self._y = y  # Protected
        self._size = 60
        self.__last_interaction = 0
        self.__is_selected = False
    
    # Getter methods - cara aman akses private data (ENCAPSULATION)
    def get_name(self):
        return self.__name
    
    def get_age(self):
        return self.__age
    
    def get_happiness(self):
        return self.__happiness
    
    def get_health(self):
        return self.__health
    
    def get_position(self):
        return (self._x, self._y)
    
    def is_selected(self):
        return self.__is_selected
    
    # Setter methods dengan VALIDASI (ENCAPSULATION)
    def set_happiness(self, value):
        """Setter dengan validasi - happiness harus 0-100"""
        self.__happiness = max(0, min(100, value))
        
    def set_health(self, value):
        """Setter dengan validasi - health harus 0-100"""
        self.__health = max(0, min(100, value))
    
    def select(self):
        """Select entity"""
        self.__is_selected = True
        
    def deselect(self):
        """Deselect entity"""
        self.__is_selected = False
    
    def age_up(self):
        """Tambah umur - private method untuk internal use"""
        self.__age += 1
    
    def interact(self):
        """Interaksi dengan entity"""
        self.__last_interaction = pygame.time.get_ticks()
    
    def update(self):
        """happiness - LEBIH LAMBAT"""
        current_time = pygame.time.get_ticks()
        if current_time - self.__last_interaction > 15000: 
            self.set_happiness(self.__happiness - 0.5)  
    
    def check_click(self, mouse_pos):
        """Check if entity clicked"""
        rect = pygame.Rect(self._x - self._size//2, self._y - self._size//2, 
                          self._size, self._size)
        return rect.collidepoint(mouse_pos)
    
    @abstractmethod
    def draw(self, surface):
        """Abstract method - harus diimplementasi child class"""
        pass


# ==================== INHERITANCE ====================
# Animal base class mewarisi FarmEntity
class Animal(FarmEntity):
    """
    Animal class - inherit dari FarmEntity (INHERITANCE).
    Menambah functionality khusus untuk hewan.
    """
    def __init__(self, name, x, y, base_color, species):
        super().__init__(name, x, y)  # Panggil parent constructor
        self._base_color = base_color
        self._current_color = base_color
        self._species = species
        self.__hunger = 100  # Private - 0 = lapar, 100 = kenyang
        self.__is_transformed = False  # Untuk polymorphism
        self.__products = []  # Produk yang dihasilkan (telur, susu, dll)
        self.__product_timer = 0
        self._movement_timer = 0
        self._target_x = x
        self._target_y = y
        self.__energy = 100  # Private
    
    def get_hunger(self):
        return self.__hunger
    
    def get_species(self):
        return self._species
    
    def is_transformed(self):
        return self.__is_transformed
    
    def get_products(self):
        """Return copy untuk protect internal list (ENCAPSULATION)"""
        return self.__products.copy()
    
    def get_energy(self):
        return self.__energy
    
    def feed(self, food_value):
        """
        Method untuk memberi makan (PUBLIC interface).
        Mengubah PRIVATE attribute dengan validasi.
        """
        self.__hunger = min(100, self.__hunger + food_value)
        self.set_happiness(self.get_happiness() + 10)
        self.__energy = min(100, self.__energy + 20)
        
        # Cek transformasi (POLYMORPHISM akan terjadi!)
        self._check_transformation()
    
    def pet(self):
        """Elus hewan untuk tambah happiness"""
        self.set_happiness(self.get_happiness() + 15)
        self.__energy = min(100, self.__energy + 5)
    
    def _check_transformation(self):
        """
        Protected method - cek apakah hewan harus transform.
        Ini akan trigger POLYMORPHISM di child class!
        LEBIH MUDAH: happiness > 70 dan hunger > 70
        """
        if self.get_happiness() > 70 and self.__hunger > 70:  # Dari 80 jadi 70
            if not self.__is_transformed:  # Baru transform
                self.__is_transformed = True
                self.transform()  # Polymorphism! Setiap hewan transform beda
        else:
            if self.__is_transformed:  # Baru kembali normal
                self.__is_transformed = False
                self.reset_form()
    
    @abstractmethod
    def transform(self):
        """Abstract - setiap hewan punya transformasi berbeda (POLYMORPHISM)"""
        pass
    
    @abstractmethod
    def reset_form(self):
        """Abstract - reset ke bentuk normal"""
        pass
    
    @abstractmethod
    def produce(self):
        """Abstract - setiap hewan produce produk berbeda"""
        pass
    
    def update(self):
        """Override parent update, tambah logic untuk animal"""
        super().update()  # Panggil parent update
        
        # Hunger berkurang over time - LEBIH LAMBAT
        self.__hunger = max(0, self.__hunger - 0.05)  # Dari 0.1 jadi 0.05
        self.__energy = max(0, self.__energy - 0.02)  # Dari 0.05 jadi 0.02
        
        # Happiness turun kalau lapar
        if self.__hunger < 30:
            self.set_happiness(self.get_happiness() - 0.2)  # Lebih lambat
        
        # Random movement (hewan bergerak sendiri) - LEBIH JARANG
        self._movement_timer -= 1
        if self._movement_timer <= 0:
            self._target_x = random.randint(150, WIDTH - 150)
            self._target_y = random.randint(250, HEIGHT - 200)
            self._movement_timer = random.randint(180, 400)  # Lebih lama diam
        
        # Move towards target - LEBIH LAMBAT
        dx = self._target_x - self._x
        dy = self._target_y - self._y
        distance = (dx**2 + dy**2)**0.5
        if distance > 2:
            speed = 1.0  # Dari 1.5 jadi 1.0
            self._x += (dx / distance) * speed
            self._y += (dy / distance) * speed
        
        # Production timer - LEBIH CEPAT!
        self.__product_timer += 1
        if self.__product_timer >= 300: 
            self.produce()
            self.__product_timer = 0
        
        # Update transformation
        self._check_transformation()
    
    def draw_base(self, surface):
        """Base drawing untuk semua animal"""
        # Shadow
        shadow_rect = pygame.Rect(self._x - self._size//2 + 5, 
                                 self._y + self._size//3, 
                                 self._size - 10, 15)
        pygame.draw.ellipse(surface, (0, 0, 0, 50), shadow_rect)
        
        # Selection indicator
        if self.is_selected():
            pygame.draw.circle(surface, YELLOW, (int(self._x), int(self._y)), 
                             self._size//2 + 5, 3)
        
        # Status bars di atas hewan
        bar_width = self._size
        bar_height = 6
        bar_y = self._y - self._size//2 - 25
        
        # Health bar (RED)
        pygame.draw.rect(surface, BROWN, 
                        (self._x - bar_width//2, bar_y, bar_width, bar_height))
        health_width = (self.get_health() / 100) * bar_width
        pygame.draw.rect(surface, RED, 
                        (self._x - bar_width//2, bar_y, health_width, bar_height))
        
        # Happiness bar (PINK)
        bar_y += bar_height + 2
        pygame.draw.rect(surface, BROWN, 
                        (self._x - bar_width//2, bar_y, bar_width, bar_height))
        happiness_width = (self.get_happiness() / 100) * bar_width
        pygame.draw.rect(surface, PINK, 
                        (self._x - bar_width//2, bar_y, happiness_width, bar_height))
        
        # Hunger bar (GREEN)
        bar_y += bar_height + 2
        pygame.draw.rect(surface, BROWN, 
                        (self._x - bar_width//2, bar_y, bar_width, bar_height))
        hunger_width = (self.__hunger / 100) * bar_width
        pygame.draw.rect(surface, GREEN, 
                        (self._x - bar_width//2, bar_y, hunger_width, bar_height))

# ==================== POLYMORPHISM - Chicken ====================
class Chicken(Animal):
    """
    Chicken class - inherit dari Animal (INHERITANCE).
    Implementasi POLYMORPHISM lewat transform() yang berbeda.
    """
    def __init__(self, x, y):
        super().__init__("Ayam", x, y, WHITE, "chicken")
        self._size = 50
        self.__egg_count = 0  # Private counter
    
    def get_egg_count(self):
        return self.__egg_count
    
    def transform(self):
        """
        POLYMORPHISM! Chicken transform jadi GOLDEN CHICKEN.
        Override method dari parent dengan behavior berbeda.
        """
        self._current_color = GOLD
        self._size = 60
    
    def reset_form(self):
        """Reset ke bentuk normal"""
        self._current_color = self._base_color
        self._size = 50
    
    def produce(self):
        """
        POLYMORPHISM! Chicken produce telur.
        Setiap animal produce berbeda.
        """
        if self.get_hunger() > 50 and self.get_energy() > 30:
            if self.is_transformed():
                self.__egg_count += 2  # Golden chicken produce lebih banyak!
            else:
                self.__egg_count += 1
    
    def collect_eggs(self):
        """Ambil telur dan reset counter"""
        count = self.__egg_count
        self.__egg_count = 0
        return count
    
    def draw(self, surface):
        """
        POLYMORPHISM! Setiap animal punya cara draw berbeda.
        Override abstract method dari parent.
        """
        self.draw_base(surface)
        
        # Body (bulat)
        pygame.draw.circle(surface, self._current_color, 
                          (int(self._x), int(self._y)), self._size//2)
        
        # Head (bulat kecil)
        head_x = int(self._x - self._size//4)
        head_y = int(self._y - self._size//3)
        pygame.draw.circle(surface, self._current_color, 
                          (head_x, head_y), self._size//3)
        
        # Mata
        eye_size = 4
        pygame.draw.circle(surface, BLACK, 
                          (head_x - 5, head_y - 3), eye_size)
        pygame.draw.circle(surface, BLACK, 
                          (head_x + 5, head_y - 3), eye_size)
        
        # Paruh
        beak_color = YELLOW if not self.is_transformed() else GOLD
        pygame.draw.polygon(surface, beak_color, [
            (head_x - 10, head_y + 5),
            (head_x - 15, head_y + 8),
            (head_x - 10, head_y + 10)
        ])
        
        # Jengger (merah)
        if not self.is_transformed():
            crest_color = RED
        else:
            crest_color = GOLD
        pygame.draw.circle(surface, crest_color, (head_x, head_y - 10), 5)
        
        # Telur icon kalau ada
        if self.__egg_count > 0:
            text = font_small.render(f"TELUR ×{self.__egg_count}", True, WHITE)
            surface.blit(text, (self._x + 20, self._y - 30))
        
        # Transform indicator
        if self.is_transformed():
            star_text = font_small.render("[GOLD]", True, GOLD)
            surface.blit(star_text, (self._x - 40, self._y - 50))


# ==================== POLYMORPHISM - Cow ====================
class Cow(Animal):
    """
    Cow class - POLYMORPHISM dengan transformation berbeda dari Chicken.
    """
    def __init__(self, x, y):
        super().__init__("Sapi", x, y, (139, 90, 43), "cow")
        self._size = 80
        self.__milk_amount = 0  # Private
        self._spots_color = BLACK
    
    def get_milk_amount(self):
        return self.__milk_amount
    
    def transform(self):
        """
        POLYMORPHISM! Cow transform jadi SUPER COW (Pink).
        Implementation berbeda dari Chicken!
        """
        self._current_color = PINK
        self._spots_color = RED
        self._size = 95
    
    def reset_form(self):
        """Reset"""
        self._current_color = self._base_color
        self._spots_color = BLACK
        self._size = 80
    
    def produce(self):
        """
        POLYMORPHISM! Cow produce susu, bukan telur.
        Implementation berbeda dari Chicken.produce()!
        """
        if self.get_hunger() > 50 and self.get_energy() > 30:
            if self.is_transformed():
                self.__milk_amount += 3  # Super cow produce lebih banyak!
            else:
                self.__milk_amount += 1
    
    def collect_milk(self):
        """Ambil susu"""
        amount = self.__milk_amount
        self.__milk_amount = 0
        return amount
    
    def draw(self, surface):
        """
        POLYMORPHISM! Cow punya visual berbeda dari Chicken.
        """
        self.draw_base(surface)
        
        # Body (oval besar)
        body_rect = pygame.Rect(
            int(self._x - self._size//2),
            int(self._y - self._size//3),
            self._size,
            int(self._size * 0.7)
        )
        pygame.draw.ellipse(surface, self._current_color, body_rect)
        
        # Spots (totol-totol)
        spot_positions = [
            (self._x - 15, self._y - 10),
            (self._x + 10, self._y - 5),
            (self._x - 5, self._y + 10)
        ]
        for pos in spot_positions:
            pygame.draw.circle(surface, self._spots_color, pos, 8)
        
        # Head
        head_x = int(self._x - self._size//2 - 15)
        head_y = int(self._y)
        pygame.draw.circle(surface, self._current_color, (head_x, head_y), 25)
        
        # Mata
        eye_size = 5
        pygame.draw.circle(surface, BLACK, (head_x - 8, head_y - 5), eye_size)
        pygame.draw.circle(surface, BLACK, (head_x + 8, head_y - 5), eye_size)
        
        # Hidung
        pygame.draw.circle(surface, PINK, (head_x, head_y + 10), 8)
        pygame.draw.circle(surface, BLACK, (head_x - 3, head_y + 10), 2)
        pygame.draw.circle(surface, BLACK, (head_x + 3, head_y + 10), 2)
        
        # Tanduk
        horn_color = WHITE if not self.is_transformed() else GOLD
        pygame.draw.polygon(surface, horn_color, [
            (head_x - 15, head_y - 20),
            (head_x - 20, head_y - 30),
            (head_x - 12, head_y - 18)
        ])
        pygame.draw.polygon(surface, horn_color, [
            (head_x + 15, head_y - 20),
            (head_x + 20, head_y - 30),
            (head_x + 12, head_y - 18)
        ])
        
        # Milk icon
        if self.__milk_amount > 0:
            text = font_small.render(f"SUSU ×{self.__milk_amount}", True, WHITE)
            surface.blit(text, (self._x + 30, self._y - 30))
        
        # Transform indicator
        if self.is_transformed():
            heart_text = font_small.render("[SUPER]", True, RED)
            surface.blit(heart_text, (self._x - 50, self._y - 60))


# ==================== POLYMORPHISM - Sheep ====================
class Sheep(Animal):
    """
    Sheep class - POLYMORPHISM lagi dengan transformation unik!
    """
    def __init__(self, x, y):
        super().__init__("Domba", x, y, WHITE, "sheep")
        self._size = 70
        self.__wool_amount = 0  # Private
        self._wool_color = WHITE
    
    def get_wool_amount(self):
        return self.__wool_amount
    
    def transform(self):
        """
        POLYMORPHISM! Sheep transform jadi RAINBOW SHEEP.
        Setiap animal transformasi BERBEDA!
        """
        self._wool_color = (random.randint(100, 255), 
                           random.randint(100, 255), 
                           random.randint(100, 255))
        self._size = 85
    
    def reset_form(self):
        """Reset"""
        self._wool_color = WHITE
        self._size = 70
    
    def produce(self):
        """
        POLYMORPHISM! Sheep produce wool.
        Berbeda dari Chicken (telur) dan Cow (susu)!
        """
        if self.get_hunger() > 50 and self.get_energy() > 30:
            if self.is_transformed():
                self.__wool_amount += 2
            else:
                self.__wool_amount += 1
    
    def collect_wool(self):
        """Ambil wool"""
        amount = self.__wool_amount
        self.__wool_amount = 0
        return amount
    
    def draw(self, surface):
        """
        POLYMORPHISM! Sheep visual berbeda dari Chicken dan Cow.
        """
        self.draw_base(surface)
        
        # Body (fluffy circles untuk wool effect)
        circles = [
            (self._x, self._y, self._size//2),
            (self._x - 20, self._y - 5, self._size//3),
            (self._x + 20, self._y - 5, self._size//3),
            (self._x, self._y + 15, self._size//3)
        ]
        for cx, cy, radius in circles:
            pygame.draw.circle(surface, self._wool_color, (int(cx), int(cy)), radius)
        
        # Head (hitam)
        head_x = int(self._x - self._size//2 - 10)
        head_y = int(self._y - 5)
        pygame.draw.circle(surface, BLACK, (head_x, head_y), 20)
        
        # Mata
        eye_size = 4
        pygame.draw.circle(surface, WHITE, (head_x - 6, head_y - 3), eye_size)
        pygame.draw.circle(surface, WHITE, (head_x + 6, head_y - 3), eye_size)
        
        # Wool icon
        if self.__wool_amount > 0:
            text = font_small.render(f"WOOL ×{self.__wool_amount}", True, WHITE)
            surface.blit(text, (self._x + 25, self._y - 30))
        
        # Transform indicator
        if self.is_transformed():
            rainbow_text = font_small.render("RAINBOW", True, WHITE)
            surface.blit(rainbow_text, (self._x - 45, self._y - 55))


# ==================== GAME MANAGER ====================
class Farm:
    """Main game class dengan composition"""
    def __init__(self):
        self.animals = []
        self.selected_animal = None
        self.money = 500  # Lebih banyak uang awal!
        self.total_eggs = 0
        self.total_milk = 0
        self.total_wool = 0
        self.day = 1
        self.time_of_day = 0  # 0-1000 (morning to night)
        self.missions = self._create_missions()
        self.tutorial_step = 0
        self.show_tutorial = True
        
        # Spawn initial animals - lebih rapi
        self.animals.append(Chicken(250, 400))
        self.animals.append(Cow(500, 400))
        self.animals.append(Sheep(750, 400))
        
        # UI state
        self.show_shop = False
        self.messages = []
        
    def _create_missions(self):
        """Create mission list"""
        return [
            {"text": "Kumpulkan 3 telur!", "type": "eggs", "target": 3, "reward": 100, "completed": False},
            {"text": "Kumpulkan 2 susu!", "type": "milk", "target": 2, "reward": 80, "completed": False},
            {"text": "Transform 1 hewan!", "type": "transform", "target": 1, "reward": 150, "completed": False},
            {"text": "Kumpulkan 2 wol!", "type": "wool", "target": 2, "reward": 80, "completed": False},
            {"text": "Beli 1 hewan!", "type": "buy", "target": 1, "reward": 50, "completed": False},
        ]
    
    def add_message(self, text, color=YELLOW):
        """Tambah notifikasi message"""
        self.messages.append({"text": text, "color": color, "timer": 180})
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self._handle_click(event.pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.show_tutorial = False
                elif event.key == pygame.K_s:
                    self.show_shop = not self.show_shop
                elif event.key == pygame.K_f:
                    self._feed_selected()
                elif event.key == pygame.K_p:
                    self._pet_selected()
                elif event.key == pygame.K_c:
                    self._collect_products()
        return True
    
    def _handle_click(self, pos):
        """Handle mouse click"""
        # Check shop buttons
        if self.show_shop:
            self._check_shop_click(pos)
            return
        
        # Check animal selection
        for animal in self.animals:
            if animal.check_click(pos):
                if self.selected_animal:
                    self.selected_animal.deselect()
                self.selected_animal = animal
                animal.select()
                self.add_message(f"Dipilih: {animal.get_name()}")
                return
        
        # Deselect if click empty space
        if self.selected_animal:
            self.selected_animal.deselect()
            self.selected_animal = None
    
    def _feed_selected(self):
        """Feed selected animal - LEBIH MURAH!"""
        if self.selected_animal and self.money >= 5:  # Dari $10 jadi $5
            self.selected_animal.feed(40)  # Lebih kenyang
            self.money -= 5
            self.add_message("Dikasih makan!", GREEN)
        elif self.money < 5:
            self.add_message("Uang tidak cukup!", RED)
    
    def _pet_selected(self):
        """Pet selected animal"""
        if self.selected_animal:
            self.selected_animal.pet()
            self.add_message("Dielus-elus!", PINK)
    
    def _collect_products(self):
        """Collect products from selected animal - HARGA LEBIH TINGGI!"""
        if not self.selected_animal:
            return
        
        animal = self.selected_animal
        collected = False
        
        if isinstance(animal, Chicken):
            eggs = animal.collect_eggs()
            if eggs > 0:
                self.total_eggs += eggs
                self.money += eggs * 15  # Dari $5 jadi $15!
                self.add_message(f"Dapat {eggs} telur! +${eggs*15}", YELLOW)
                collected = True
        
        elif isinstance(animal, Cow):
            milk = animal.collect_milk()
            if milk > 0:
                self.total_milk += milk
                self.money += milk * 25  # Dari $10 jadi $25!
                self.add_message(f"Dapat {milk} susu! +${milk*25}", BLUE)
                collected = True
        
        elif isinstance(animal, Sheep):
            wool = animal.collect_wool()
            if wool > 0:
                self.total_wool += wool
                self.money += wool * 20  # Dari $8 jadi $20!
                self.add_message(f"Dapat {wool} wol! +${wool*20}", WHITE)
                collected = True
        
        if collected:
            self._check_missions()
    
    def _check_shop_click(self, pos):
        """Check shop button clicks"""
        button_rects = [
            pygame.Rect(WIDTH - 250, 120, 230, 50),  # Buy Chicken
            pygame.Rect(WIDTH - 250, 180, 230, 50),  # Buy Cow
            pygame.Rect(WIDTH - 250, 240, 230, 50),  # Buy Sheep
        ]
        
        prices = [50, 100, 80]
        animals_to_add = [Chicken, Cow, Sheep]
        names = ["Ayam", "Sapi", "Domba"]
        
        for i, rect in enumerate(button_rects):
            if rect.collidepoint(pos):
                if self.money >= prices[i]:
                    x = random.randint(200, WIDTH - 200)
                    y = random.randint(300, HEIGHT - 200)
                    new_animal = animals_to_add[i](x, y)
                    self.animals.append(new_animal)
                    self.money -= prices[i]
                    self.add_message(f"Beli {names[i]}! -${prices[i]}", GREEN)
                    self._check_missions()
                else:
                    self.add_message("Uang tidak cukup!", RED)
    
    def _check_missions(self):
        """Check if any mission completed"""
        for mission in self.missions:
            if mission["completed"]:
                continue
            
            if mission["type"] == "eggs" and self.total_eggs >= mission["target"]:
                mission["completed"] = True
                self.money += mission["reward"]
                self.add_message(f"Misi Selesai! +${mission['reward']}", GOLD)
            
            elif mission["type"] == "milk" and self.total_milk >= mission["target"]:
                mission["completed"] = True
                self.money += mission["reward"]
                self.add_message(f"Misi Selesai! +${mission['reward']}", GOLD)
            
            elif mission["type"] == "wool" and self.total_wool >= mission["target"]:
                mission["completed"] = True
                self.money += mission["reward"]
                self.add_message(f"Misi Selesai! +${mission['reward']}", GOLD)
            
            elif mission["type"] == "transform":
                transform_count = sum(1 for a in self.animals if a.is_transformed())
                if transform_count >= mission["target"]:
                    mission["completed"] = True
                    self.money += mission["reward"]
                    self.add_message(f"TRANSFORMASI BERHASIL! +${mission['reward']}", GOLD)
            
            elif mission["type"] == "buy" and len(self.animals) >= mission["target"] + 3:
                mission["completed"] = True
                self.money += mission["reward"]
                self.add_message(f"Misi Beli Selesai! +${mission['reward']}", GOLD)
    
    def update(self):
        """Update game state"""
        # Update all animals
        for animal in self.animals[:]:
            animal.update()
        
        # Update time - LEBIH LAMBAT
        self.time_of_day += 0.2  # Dari 0.5 jadi 0.2
        if self.time_of_day >= 1000:
            self.time_of_day = 0
            self.day += 1
            self.add_message(f"Hari ke-{self.day}!", BLUE)
        
        # Update messages
        for msg in self.messages[:]:
            msg["timer"] -= 1
            if msg["timer"] <= 0:
                self.messages.remove(msg)
        
        # Check missions (termasuk transform check)
        self._check_missions()
        
        # Transform notification
        for animal in self.animals:
            if animal.is_transformed():
                # Check kalau baru transform (belum ada notifikasi sebelumnya)
                if not hasattr(animal, '_transform_notified'):
                    animal._transform_notified = True
                    species_name = animal.get_name()
                    if "Ayam" in species_name:
                        self.add_message("GOLDEN CHICKEN! Produce 2x lipat!", GOLD)
                    elif "Sapi" in species_name:
                        self.add_message("SUPER COW! Pink power!", PINK)
                    elif "Domba" in species_name:
                        self.add_message("RAINBOW SHEEP! Warna ajaib!", (255, 100, 255))
            else:
                if hasattr(animal, '_transform_notified'):
                    delattr(animal, '_transform_notified')
    
    def draw(self):
        """Draw everything"""
        # Sky gradient (day/night cycle)
        time_ratio = self.time_of_day / 1000
        if time_ratio < 0.5:  # Morning to afternoon
            sky_color = (135, 206, 250)  # Light blue
        else:  # Evening to night
            night_progress = (time_ratio - 0.5) * 2
            sky_color = (
                int(135 - 105 * night_progress),
                int(206 - 176 * night_progress),
                int(250 - 180 * night_progress)
            )
        screen.fill(sky_color)
        
        # Ground
        ground_rect = pygame.Rect(0, HEIGHT - 150, WIDTH, 150)
        pygame.draw.rect(screen, GRASS_GREEN, ground_rect)
        
        # Grass details
        for i in range(0, WIDTH, 30):
            pygame.draw.line(screen, DARK_GREEN, (i, HEIGHT - 150), 
                           (i + 10, HEIGHT - 140), 2)
        
        # Draw animals
        for animal in self.animals:
            animal.draw(screen)
        
        # UI Panel
        self._draw_ui()
        
        # Shop
        if self.show_shop:
            self._draw_shop()
        
        # Tutorial
        if self.show_tutorial:
            self._draw_tutorial()
        
        # Messages
        y_offset = HEIGHT - 180
        for msg in self.messages:
            text_surf = font_small.render(msg["text"], True, msg["color"])
            text_rect = text_surf.get_rect(center=(WIDTH // 2, y_offset))
            # Background
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(screen, (0, 0, 0, 150), bg_rect, border_radius=10)
            screen.blit(text_surf, text_rect)
            y_offset -= 35
        
        pygame.display.flip()

    def _draw_ui(self):
        """Draw UI elements"""
        # Top bar background
        pygame.draw.rect(screen, (30, 30, 30, 230), (0, 0, WIDTH, 100))
        
        # Money - LEBIH BESAR
        money_text = font_title.render(f"Uang ${self.money}", True, GOLD)
        screen.blit(money_text, (20, 15))
        
        # Day
        day_text = font_large.render(f"Hari {self.day}", True, WHITE)
        screen.blit(day_text, (20, 65))
        
        # Stats - KANAN ATAS
        stats_x = WIDTH - 450
        stats_y = 20
        
        # Background untuk stats
        stats_bg = pygame.Rect(stats_x - 10, stats_y - 10, 500, 80)
        pygame.draw.rect(screen, (50, 50, 50, 200), stats_bg, border_radius=10)
        
        # Telur
        egg_label = font_medium.render("TELUR:", True, YELLOW)
        screen.blit(egg_label, (stats_x, stats_y))
        egg_count = font_large.render(str(self.total_eggs), True, WHITE)
        screen.blit(egg_count, (stats_x, stats_y + 30))
        
        # Susu
        milk_label = font_medium.render("SUSU:", True, LIGHT_BLUE)
        screen.blit(milk_label, (stats_x + 130, stats_y))
        milk_count = font_large.render(str(self.total_milk), True, WHITE)
        screen.blit(milk_count, (stats_x + 130, stats_y + 30))
        
        # Wol
        wool_label = font_medium.render("WOL:", True, WHITE)
        screen.blit(wool_label, (stats_x + 260, stats_y))
        wool_count = font_large.render(str(self.total_wool), True, WHITE)
        screen.blit(wool_count, (stats_x + 260, stats_y + 30))
        
        # Missions - KIRI BAWAH
        mission_x = 20
        mission_y = HEIGHT - 220
        
        # Mission background
        mission_bg = pygame.Rect(mission_x - 10, mission_y - 7, 400, 210)
        pygame.draw.rect(screen, (20, 20, 40, 200), mission_bg, border_radius=10)
        
        mission_title = font_medium.render("MISI", True, GOLD)
        screen.blit(mission_title, (mission_x, mission_y))
        mission_y += 40
        
        for mission in self.missions:
            color = GREEN if mission["completed"] else WHITE
            status = "[V]" if mission["completed"] else "[X]"
            mission_text = font_small.render(
                f"{status} {mission['text']}", 
                True, color
            )
            screen.blit(mission_text, (mission_x, mission_y))
            
            # Reward
            reward_text = font_small.render(f"+${mission['reward']}", True, YELLOW)
            screen.blit(reward_text, (mission_x + 280, mission_y + 2))
            mission_y += 35
        
        # Controls - KANAN BAWAH
        controls_x = WIDTH - 350
        controls_y = HEIGHT - 220
        
        # Control background
        control_bg = pygame.Rect(controls_x - 10, controls_y - 7, 340, 210)
        pygame.draw.rect(screen, (20, 40, 20, 200), control_bg, border_radius=10)
        
        controls_title = font_medium.render("KONTROL", True, GREEN)
        screen.blit(controls_title, (controls_x, controls_y))
        controls_y += 40
        
        controls = [
            "Klik = Pilih hewan",
            "F = Kasih makan ($5)",
            "P = Elus-elus (GRATIS!)",
            "C = Ambil hasil",
            "S = Buka toko"
        ]
        for text in controls:
            control_text = font_small.render(text, True, WHITE)
            screen.blit(control_text, (controls_x, controls_y))
            controls_y += 35
        
        # Selected animal info - KANAN TENGAH
        if self.selected_animal:
            info_x = WIDTH - 350
            info_y = 150
            
            # Background panel - LEBIH MENONJOL
            panel_rect = pygame.Rect(info_x - 15, info_y - 15, 350, 230)
            pygame.draw.rect(screen, (60, 30, 80, 240), panel_rect, border_radius=15)
            pygame.draw.rect(screen, GOLD, panel_rect, 4, border_radius=15)
            
            name_text = font_large.render(f"✨ {self.selected_animal.get_name()}", 
                                          True, GOLD)
            screen.blit(name_text, (info_x, info_y))
            info_y += 45
            
            stats = [
                f"Kesehatan: {int(self.selected_animal.get_health())}%",
                f"Kebahagiaan: {int(self.selected_animal.get_happiness())}%",
                f"Kenyang: {int(self.selected_animal.get_hunger())}%",
                f"Energi: {int(self.selected_animal.get_energy())}%"
            ]
            
            # Transform status
            if self.selected_animal.is_transformed():
                transform_text = font_medium.render("TRANSFORMASI!", True, YELLOW)
                screen.blit(transform_text, (info_x + 80, info_y))
                info_y += 35
            
            for stat in stats:
                stat_text = font_medium.render(stat, True, WHITE)
                screen.blit(stat_text, (info_x, info_y))
                info_y += 32
    
    def _draw_shop(self):
        """Draw shop interface"""
        # Shop background
        shop_rect = pygame.Rect(WIDTH - 280, 50, 260, 350)
        pygame.draw.rect(screen, (30, 30, 50, 240), shop_rect, border_radius=15)
        pygame.draw.rect(screen, YELLOW, shop_rect, 3, border_radius=15)
        
        # Title
        title = font_large.render("TOKO", True, YELLOW)
        screen.blit(title, (WIDTH - 250, 60))
        
        # Items
        items = [
            ("Ayam", 50, 120),
            ("Sapi", 100, 180),
            ("Domba", 80, 240)
        ]
        
        for name, price, y in items:
            # Button background
            button_rect = pygame.Rect(WIDTH - 250, y, 230, 50)
            color = GREEN if self.money >= price else GRAY
            pygame.draw.rect(screen, color, button_rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, button_rect, 2, border_radius=10)
            
            # Text
            item_text = font_medium.render(f"{name} - ${price}", True, WHITE)
            text_rect = item_text.get_rect(center=button_rect.center)
            screen.blit(item_text, text_rect)
        
        # Close hint
        hint = font_small.render("Tekan S untuk tutup", True, WHITE)
        screen.blit(hint, (WIDTH - 250, 310))
    
    def _draw_tutorial(self):
        """Draw tutorial overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Tutorial box - LEBIH PANJANG
        box_rect = pygame.Rect(WIDTH//4, 120, WIDTH//2, 540)
        pygame.draw.rect(screen, (40, 40, 60), box_rect, border_radius=20)
        pygame.draw.rect(screen, YELLOW, box_rect, 5, border_radius=20)
        
        # Title
        title = font_title.render("Polymor-Farm", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH//2, 170))
        screen.blit(title, title_rect)
        
        # Instructions
        instructions = [
            "Rawat hewan dengan baik!",
            "",
            "F = Kasih makan ($5)",
            "P = Elus-elus (gratis)",
            "C = Ambil hasil",
            "",
            "POLYMORPHISM MAGIC:",
            "Happiness > 70% + Kenyang > 70%",
            "= TRANSFORMASI! ",
            "",
            "Ayam -> Golden Chicken",
            "Sapi -> Super Cow", 
            "Domba -> Rainbow Sheep",
            "",
            "S = Toko || Selesaikan misi!"
        ]
        
        y_offset = 230
        for line in instructions:
            text = font_medium.render(line, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH//2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 28
        
        # Start hint 
        start_text = font_medium.render("Tekan SPACE untuk mulai!", True, WHITE)
        start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT - 80))
        
        # Background untuk tombol
        start_bg = start_rect.inflate(30, 15)
        pygame.draw.rect(screen, (0, 100, 0), start_bg, border_radius=10)
        pygame.draw.rect(screen, YELLOW, start_bg, 3, border_radius=10)
        
        screen.blit(start_text, start_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            if not self.show_tutorial:
                self.update()
            self.draw()
            clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


# ==================== MAIN ====================
if __name__ == "__main__":
    game = Farm()
    game.run()