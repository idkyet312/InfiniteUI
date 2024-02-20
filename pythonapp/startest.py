import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()

# Screen dimensions and setup
screen_width, screen_height = 600, 400
grid_size = 20
cell_size = screen_width // grid_size

# Pygame display setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ecosystem Simulation with Interactive Herbivores")

# Load images function
def load_image(path):
    image = pygame.image.load(path).convert_alpha()  # Use convert_alpha() for transparency
    return pygame.transform.scale(image, (cell_size, cell_size))

# Assuming you have these images prepared
herbivore_img = load_image('herbivore.png')
plant_img = load_image('plant.png')
player_img = load_image('player.png')
carnivore_img = load_image('carnivore.png')

# Initialize entities with positions and additional attributes
entities = {
    'plants': [[random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)] for _ in range(50)],
    'herbivores': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'hunger': 100} for _ in range(10)],
    'carnivores': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'hunger': 100} for _ in range(5)],  # Initialize carnivores
    'player': {'pos': [grid_size // 2, grid_size // 2]}
}

def load_image(path):
    image = pygame.image.load(path).convert_alpha()  # Use convert_alpha() for transparency
    return pygame.transform.scale(image, (cell_size, cell_size))

def find_nearest_plant(h_pos):
    min_dist = float('inf')
    nearest_plant = None
    for plant in entities['plants']:
        dist = math.hypot(plant[0] - h_pos[0], plant[1] - h_pos[1])
        if dist < min_dist:
            min_dist = dist
            nearest_plant = plant
    return nearest_plant

def find_nearest_herbivore(c_pos):
    min_dist = float('inf')
    nearest_herbivore = None
    for herbivore in entities['herbivores']:
        dist = math.hypot(herbivore['pos'][0] - c_pos[0], herbivore['pos'][1] - c_pos[1])
        if dist < min_dist:
            min_dist = dist
            nearest_herbivore = herbivore
    return nearest_herbivore

def move_herbivores():
    for herbivore in entities['herbivores']:
        if herbivore['hunger'] > 50:
            direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            herbivore['pos'][0] = (herbivore['pos'][0] + direction[0]) % grid_size
            herbivore['pos'][1] = (herbivore['pos'][1] + direction[1]) % grid_size
            herbivore['hunger'] -= 3  # Decrease hunger over time
        else:
            nearest_plant = find_nearest_plant(herbivore['pos'])
            if nearest_plant:
                move_towards_plant(herbivore, nearest_plant)
                if herbivore['pos'] == nearest_plant:
                    herbivore['hunger'] = 100  # Reset hunger
                    entities['plants'].remove(nearest_plant)  # The plant is consumed

def move_carnivores():
    for carnivore in entities['carnivores']:
        if carnivore['hunger'] > 50:
            direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            carnivore['pos'][0] = (carnivore['pos'][0] + direction[0]) % grid_size
            carnivore['pos'][1] = (carnivore['pos'][1] + direction[1]) % grid_size
            carnivore['hunger'] -= 1  # Decrease hunger over time
        else:
            nearest_herbivore = find_nearest_herbivore(carnivore['pos'])
            if nearest_herbivore:
                move_towards_herbivore(carnivore, nearest_herbivore)
                if carnivore['pos'] == nearest_herbivore['pos']:
                    carnivore['hunger'] = 100  # Reset hunger
                    entities['herbivores'].remove(nearest_herbivore)  # The herbivore is consumed

def move_towards_plant(herbivore, plant):
    # Move herbivore towards the plant
    if plant[1] > herbivore['pos'][1]:
        herbivore['pos'][1] += 1
    elif plant[1] < herbivore['pos'][1]:
        herbivore['pos'][1] -= 1
    if plant[0] > herbivore['pos'][0]:
        herbivore['pos'][0] += 1
    elif plant[0] < herbivore['pos'][0]:
        herbivore['pos'][0] -= 1

def move_towards_herbivore(carnivore, herbivore):
    # Move carnivore towards the herbivore
    if herbivore['pos'][1] > carnivore['pos'][1]:
        carnivore['pos'][1] += 1
    elif herbivore['pos'][1] < carnivore['pos'][1]:
        carnivore['pos'][1] -= 1
    if herbivore['pos'][0] > carnivore['pos'][0]:
        carnivore['pos'][0] += 1
    elif herbivore['pos'][0] < carnivore['pos'][0]:
        carnivore['pos'][0] -= 1

def display_hunger_level(hunger_level, position):
    font = pygame.font.SysFont('Arial', 20)
    hunger_text = font.render(f'Hunger: {hunger_level}', True, (255, 255, 255))
    text_position = (position[0] + 20, position[1] - 25)  # Display just above the herbivore
    screen.blit(hunger_text, text_position)

def check_herbivore_hover(mouse_pos):
    for herbivore in entities['herbivores']:
        herb_rect = pygame.Rect(herbivore['pos'][1] * cell_size, herbivore['pos'][0] * cell_size, cell_size, cell_size)
        if herb_rect.collidepoint(mouse_pos):
            return herbivore['hunger'], herb_rect.topleft
    return None, None

def check_carnivore_hover(mouse_pos):
    for carnivore in entities['carnivores']:
        carni_rect = pygame.Rect(carnivore['pos'][1] * cell_size, carnivore['pos'][0] * cell_size, cell_size, cell_size)
        if carni_rect.collidepoint(mouse_pos):
            return carnivore['hunger'], carni_rect.topleft
    return None, None

def update_screen(hover_info=None, hover_info_carni=None):
    screen.fill((0, 100, 0))  # Fill screen with dark green
    for plant in entities['plants']:
        screen.blit(plant_img, (plant[1] * cell_size, plant[0] * cell_size))
    for herbivore in entities['herbivores']:
        screen.blit(herbivore_img, (herbivore['pos'][1] * cell_size, herbivore['pos'][0] * cell_size))
    for carnivore in entities['carnivores']:
        screen.blit(carnivore_img, (carnivore['pos'][1] * cell_size, carnivore['pos'][0] * cell_size))
    screen.blit(player_img, (entities['player']['pos'][1] * cell_size, entities['player']['pos'][0] * cell_size))
    
    if hover_info and hover_info[0] is not None:
        display_hunger_level(hover_info[0], (hover_info[1][0], hover_info[1][1]))
    if hover_info_carni and hover_info_carni[0] is not None:
        display_hunger_level(hover_info_carni[0], (hover_info_carni[1][0], hover_info_carni[1][1]))

    pygame.display.flip()

def player_move():
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = 1
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = 1
    
    if dx != 0 or dy != 0:
        entities['player']['pos'][0] = (entities['player']['pos'][0] + dy) % grid_size
        entities['player']['pos'][1] = (entities['player']['pos'][1] + dx) % grid_size
        return True
    return False

def run_game():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player_moved = player_move()
        if player_moved:
            move_herbivores()
            move_carnivores()  # Add carnivore movement

        mouse_pos = pygame.mouse.get_pos()
        hover_info = check_herbivore_hover(mouse_pos)
        hover_info_carni = check_carnivore_hover(mouse_pos)
        update_screen(hover_info, hover_info_carni)

        clock.tick(10)  # Higher FPS for smoother hover detection

run_game()
