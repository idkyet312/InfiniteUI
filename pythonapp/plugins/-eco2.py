import pygame
import random
import sys
import math
from openai import OpenAI
import pyttsx3
import threading
import time
from gtts import gTTS
import tempfile
import os
import speech_recognition as sr

r = sr.Recognizer()

maplevel = 0

coins = 0


GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

running = False

sound = pygame.mixer

def draw_health_bar(health):
    bar_width = 200
    bar_height = 20
    pygame.draw.rect(screen, RED, (20, 20, bar_width, bar_height))  # Red background
    pygame.draw.rect(screen, GREEN, (20, 20, bar_width * (health / 100), bar_height))  # Green foreground

# Function to draw score
def draw_score(score):
    score_text = score_font.render(f'Coins: {score}', True, WHITE)
    screen.blit(score_text, (screen_width - score_text.get_width() - 20, 20))

def stop_speech():
    global sound
    sound.stop()

def play_speech(text, stop_after=8):
    global stop_threads
    pygame.mixer.init()

    # Creating a temporary file for the speech
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts = gTTS(text=text, lang='en')
    tts.save(temp_file.name)
    temp_file.close()  # Explicitly close the file to ensure it's written
    global sound
    if not pygame.mixer.get_busy():

        sound = pygame.mixer.Sound(temp_file.name)
        sound.play()
        while pygame.mixer.get_busy():
            a = 0
        else:
            stop_threads = True
        # Ensure the temporary file is deleted after playback


# Example usage


client = OpenAI(
    # This is the default and can be omitted
    api_key="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"
)

# Initialize pygame
pygame.init()

score_font = pygame.font.SysFont('Arial', 30)

# Screen dimensions and setup                                                                                                                   #Screen setup
screen_width, screen_height = 600, 700
grid_size = 30
cell_size = screen_width // grid_size

# Pygame display setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ecosystem Simulation with Interactive animals")

# Load images function
def load_image(path):
    image = pygame.image.load(path).convert_alpha()  # Use convert_alpha() for transparency
    return pygame.transform.scale(image, (cell_size, cell_size))

# Assuming you have these images prepared in your project directory
plant_img = load_image('plant.png')
indoor_img = load_image('indoor.png')
player_img = load_image('player.png')
carnivore_img = load_image('carnivore.png')
wall_img = load_image('wall.png')
ladder_img = load_image('ladder.png')


animaltier1_img = load_image('animal (1).png')
animaltier2_img = load_image('animal (2).png')
animaltier3_img = load_image('animal (3).png')
animaltier4_img = load_image('animal (4).png')
animaltier5_img = load_image('animal (5).png')

npc_img = load_image('npc.png')

# Initialize entities with positions and additional attributes
indoorObjects = [
    "Alarm clock",
    "Armchair",
    "Bed",
    "Bookshelf",
    "Cabinet or shelf for toiletries",
    "Cabinets",
    "Centerpiece",
    "Chairs",
    "China cabinet",
    "Coat rack or hooks",
    "Coffee table",
    "Computer",
    "Console table",
    "Desk",
    "Dining table",
    "Dishwasher",
    "Dresser",
    "Dryer",
    "Drying rack",
    "Filing cabinet",
    "Iron",
    "Ironing board",
    "Lamp",
    "Laundry basket",
    "Microwave",
    "Mirror"
    "Mirror",
    "Nightstand",
    "Office supplies (e.g., pens, paper, stapler)",
    "Oven",
    "Picture frames",
    "Printer",
    "Refrigerator",
    "Rug",
    "Shelves",
    "Shelving for detergent and supplies",
    "Shoe rack or storage bench",
    "Shower or bathtub",
    "Sideboard or buffet",
    "Sink",
    "Sofa",
    "Stove",
    "Tablecloth",
    "Television",
    "Toilet",
    "Towel rack",
    "Trash can",
    "Umbrella stand",
    "Wardrobe",
    "Washing machine",
]
outdoorObjects = ['tree', 'log', 'bush', 'puddle', 'lake', 'rocks', 'monolith']

enemy_types = {
    "Aliens": {"health": 110, "damage": 25, "tier": 4, "name": "Aliens"},
    "Bandits": {"health": 20, "damage": 9, "tier": 2, "name": "Bandits"},
    "Cultists": {"health": 70, "damage": 10, "tier": 3, "name": "Cultists"},
    "Demons": {"health": 70, "damage": 25, "tier": 4, "name": "Demons"},
    "Dragons": {"health": 200, "damage": 30, "tier": 5, "name": "Dragons"},
    "Ghosts": {"health": 60, "damage": 10, "tier": 3, "name": "Ghosts"},
    "Giant spiders": {"health": 70, "damage": 18, "tier": 4, "name": "Giant spiders"},
    "Goblins": {"health": 12, "damage": 5, "tier": 1, "name": "Goblins"},
    "Golems": {"health": 140, "damage": 25, "tier": 4, "name": "Golems"},
    "Mutants": {"health": 80, "damage": 17, "tier": 3, "name": "Mutants"},
    "Orcs": {"health": 10, "damage": 5, "tier": 1, "name": "Orcs"},
    "Robots": {"health": 100, "damage": 20, "tier": 3, "name": "Robots"},
    "Skeletons": {"health": 10, "damage": 3, "tier": 1, "name": "Skeletons"},
    "Snakes": {"health": 4, "damage": 2, "tier": 1, "name": "Snakes"},
    "Trolls": {"health": 20, "damage": 10, "tier": 2, "name": "Trolls"},
    "Vampires": {"health": 100, "damage": 18, "tier": 3, "name": "Vampires"},
    "Werewolves": {"health": 120, "damage": 22, "tier": 3, "name": "Werewolves"},
    "Wolves": {"health": 6, "damage": 3, "tier": 1, "name": "Wolves"},
    "Wraiths": {"health": 90, "damage": 22, "tier": 3, "name": "Wraiths"},
    "Zombies": {"health": 10, "damage": 4, "tier": 1, "name": "Zombies"},
}

game_items = [
    "ladder", "ladderup", "Small dagger",
    "Iron ingot", "Battleaxe",
    "Gemstone", "Club",
    "Bone", "Rusty sword",
    "Decayed flesh", "Corroded shield",
    "Dragon scale", "Fire essence",
    "Spider silk", "Venom gland",
    "Wolf pelt", "Fang",
    "Stolen goods", "Thief's dagger",
    "Infernal horn", "Dark orb",
    "Ectoplasm", "Shadow blade",
    "Spectral essence", "Haunting whisper",
    "Vampire fang", "Blood vial",
    "Werewolf fur", "Moonstone shard",
    "Mutant tissue", "Radioactive fluid",
    "Alien artifact", "Extraterrestrial metal",
    "Circuit board", "Energy cell",
    "Snake skin", "Venomous fang",
    "Golem core", "Earthen crystal",
    "Occult tome", "Sacrificial knife"
]

enemy_drops = {
    "Goblins": [("Bone", 0.8), ("Small dagger", 0.5), ("Coins", 20)],
    "Orcs": [("Iron ingot", 0.7), ("Battleaxe", 0.4), ("Coins", 30)],
    "Trolls": [("Gemstone", 0.6), ("Club", 0.3), ("Coins", 50)],
    "Skeletons": [("Bone", 0.8), ("Rusty sword", 0.5), ("Coins", 10)],
    "Zombies": [("Decayed flesh", 0.7), ("Corroded shield", 0.4), ("Coins", 25)],
    "Dragons": [("Dragon scale", 0.6), ("Fire essence", 0.3), ("Coins", 100)],
    "Giant spiders": [("Spider silk", 0.8), ("Venom gland", 0.5), ("Coins", 15)],
    "Wolves": [("Wolf pelt", 0.7), ("Fang", 0.4), ("Coins", 35)],
    "Bandits": [("Stolen goods", 0.6), ("Thief's dagger", 0.3), ("Coins", 40)],
    "Demons": [("Infernal horn", 0.8), ("Dark orb", 0.5), ("Coins", 70)],
    "Wraiths": [("Ectoplasm", 0.7), ("Shadow blade", 0.4), ("Coins", 60)],
    "Ghosts": [("Spectral essence", 0.6), ("Haunting whisper", 0.3), ("Coins", 45)],
    "Vampires": [("Vampire fang", 0.8), ("Blood vial", 0.5), ("Coins", 80)],
    "Werewolves": [("Werewolf fur", 0.7), ("Moonstone shard", 0.4), ("Coins", 55)],
    "Mutants": [("Mutant tissue", 0.6), ("Radioactive fluid", 0.3), ("Coins", 65)],
    "Aliens": [("Alien artifact", 0.8), ("Extraterrestrial metal", 0.5), ("Coins", 90)],
    "Robots": [("Circuit board", 0.7), ("Energy cell", 0.4), ("Coins", 75)],
    "Snakes": [("Snake skin", 0.6), ("Venomous fang", 0.3), ("Coins", 20)],
    "Golems": [("Golem core", 0.8), ("Earthen crystal", 0.5), ("Coins", 85)],
    "Cultists": [("Occult tome", 0.7), ("Sacrificial knife", 0.4), ("Coins", 50)]
}

inventory = []





filename = "map0.txt"

global entities

entities = {
    'areas': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'type': '', 'contains': '', 'descript': 'empty', 'name': ''} for _ in range(0)],
    'walls': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'type': '', 'contains': '', 'descript': 'empty'} for _ in range(0)],
    'objects': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'type': '', 'contains': '', 'descript': 'empty', 'use': 'no', 'abletokill': True} for _ in range(0)],
    'items': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'type': '', 'contains': '', 'descript': 'empty', 'use': 'no', 'abletokill': True} for _ in range(0)],
    'animals': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'type': random.choice(['pig', 'deer']), 'contains': '', 'hunger': 100, 'use': 'no'} for _ in range(0)],
    'carnivores': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'hunger': 100} for _ in range(0)],
    'player': {'pos': [grid_size // 2, grid_size // 2], 'playerhealth':100, 'playerdmg': 10, 'coins': 0},
}


def reset():
    global entities
    storehealth = entities['player']['playerhealth']
    storecoins = entities['player']['coins']
    storepos = entities['player']['pos']
    if(entities['player']['playerhealth'] < 0):
        storehealth = 100
        sounddie = pygame.mixer.Sound('expl.mp3')
        sounddie.play()
    entities.clear()
    entities = {
    'areas': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'type': '', 'contains': '', 'descript': 'empty', 'name': ''} for _ in range(0)],
    'walls': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'type': '', 'contains': '', 'descript': 'empty'} for _ in range(0)],
    'objects': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'type': '', 'contains': '', 'descript': 'empty', 'use': 'no', 'abletokill': True} for _ in range(0)],
    'items': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'type': '', 'contains': '', 'descript': 'empty', 'use': 'no', 'abletokill': True} for _ in range(0)],
    'animals': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'type': random.choice(['pig', 'deer']), 'contains': '', 'hunger': 100, 'use': 'no'} for _ in range(0)],
    'carnivores': [{'pos': [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)], 'hunger': 100} for _ in range(0)],
    'player': {'pos': storepos, 'playerhealth':storehealth, 'playerdmg': 10, 'coins': storecoins},
}
    read_file()

################################ real one below


stop_threads = False



for entity_type in ['objects', 'animals']:
    for obj in entities[entity_type]:
        if obj['type'] == 'bush' and random.randint(0,2) == 1:
            obj['contains'] = 'berry'
        elif obj['type'] == 'tree' and random.randint(0,2) == 1:
            obj['contains'] = 'fruit'

entitiessight = {
    'plant': {'pos': [grid_size // 2, grid_size // 2]} for _ in range(2)
}




def find_items_with_key_and_value(dictionary, key, value):
    matching_items = []
    for k, v in dictionary.items():
        if key in v and v[key] == value:
            matching_items.append((k, v))
    return matching_items

tier1 = find_items_with_key_and_value(enemy_types, 'tier', 1)
tier2 = find_items_with_key_and_value(enemy_types, 'tier', 2)
tier3 = find_items_with_key_and_value(enemy_types, 'tier', 3)
tier4 = find_items_with_key_and_value(enemy_types, 'tier', 4)
tier5 = find_items_with_key_and_value(enemy_types, 'tier', 5)


def read_file():
    filename2 = "map" + str(maplevel) + ".txt"   
    print(filename2)                                                                                             #read file and set up board
    screen.fill((0, 100, 0))
    try:
        i = -1
        j = -1
        k = 0
        with open(filename2, 'r') as file:
            for line in file:
                i += 1
                j = -1
                for char in line:
                    j += 1
                    if char == '#':
                        entities['walls'].append({'pos': [i, j], 'type': '', 'contains': '', 'descript': 'empty', 'name': 'wall ' + str(k)})
                        k += 1
                    elif char == 'o':
                        entities['objects'].append({'pos': [i, j], 'type': random.choice(indoorObjects), 'contains': '', 'descript': 'empty', 'use': 'no'})

                    elif char == '-':
                        entities['areas'].append({'pos': [i, j], 'type': 'indoor', 'contains': '', 'descript': 'empty'})

                    elif char == '+':
                        entities['areas'].append({'pos': [i, j], 'type': 'indoor', 'contains': '', 'descript': 'empty'})
                        entities['objects'].append({'pos': [i, j], 'type': random.choice(indoorObjects), 'contains': '', 'descript': 'empty', 'use': 'yes'})

                    elif char == 'L':
                        entities['items'].append({'pos': [i, j], 'type': game_items[0], 'contains': '', 'descript': 'empty', 'use': 'yes'})

                    elif char == 'U':
                        entities['items'].append({'pos': [i, j], 'type': game_items[1], 'contains': '', 'descript': 'empty', 'use': 'yes'})

                    elif char == 'i':
                        entities['items'].append({'pos': [i, j], 'type': random.choice(game_items), 'contains': '', 'descript': 'empty', 'use': 'yes'})
                    elif char == '$':

                        randomname = tier1[random.randint(0, len(tier1)-1)][1]
                        entities['animals'].append({'pos': [i, j], 'type': 'npc', 'contains': '', 'descript': 'empty', 'abletokill': True, 'health': randomname['health'], 'dmg':randomname['damage'], 'tier': 0})

                    elif char == '1':
                        randomname = tier1[random.randint(0, len(tier1)-1)][1]
                        entities['animals'].append({'pos': [i, j], 'type': randomname['name'], 'contains': '', 'descript': 'empty', 'abletokill': True, 'health': randomname['health'], 'dmg':randomname['damage'], 'tier': randomname['tier']})
                    elif char == '2':
                        randomname = tier2[random.randint(0, len(tier2)-1)][1]
                        entities['animals'].append({'pos': [i, j], 'type': randomname['name'], 'contains': '', 'descript': 'empty', 'abletokill': True, 'health': randomname['health'], 'dmg':randomname['damage'], 'tier': randomname['tier']})
                    elif char == '3':
                        randomname = tier3[random.randint(0, len(tier3)-1)][1]
                        entities['animals'].append({'pos': [i, j], 'type': randomname['name'], 'contains': '', 'descript': 'empty', 'abletokill': True, 'health': randomname['health'], 'dmg':randomname['damage'], 'tier': randomname['tier']})

                    elif char == '4':
                        randomname = tier4[random.randint(0, len(tier4)-1)][1]
                        entities['animals'].append({'pos': [i, j], 'type': randomname['name'], 'contains': '', 'descript': 'empty', 'abletokill': True, 'health': randomname['health'], 'dmg':randomname['damage'], 'tier': randomname['tier']})
                    elif char == '5':
                        randomname = tier5[random.randint(0, len(tier5)-1)][1]
                        entities['animals'].append({'pos': [i, j], 'type': randomname['name'], 'contains': '', 'descript': 'empty', 'abletokill': True, 'health': randomname['health'], 'dmg':randomname['damage'], 'tier': randomname['tier']})



                    # You can add additional conditions for other characters if needed
                    else:
                        # Handle other characters or do nothing
                        pass
    except FileNotFoundError:
        print("File not found.")

# Example usage  # Replace "map.txt" with your file path
read_file()





def spawn_animal(pos):                                              #spawn animal
    print(pos)
    pos = list(pos)
    print(pos)
    animal_type = random.choice(['herbivore', 'carnivore'])
    entities['objects'].append({'pos': [pos[1], pos[0]], 'type': '', 'contains': '', 'descript': 'empty'})


def find_nearest_entity(entity_pos, entities_list):
    min_dist = float('inf')
    nearest_entity = None
    for entity in entities_list:
        dist = math.hypot(entity['pos'][0] - entity_pos[0], entity['pos'][1] - entity_pos[1])
        if dist < min_dist:
            min_dist = dist
            nearest_entity = entity
    return nearest_entity

def move_entities():
    hit2 = False
    # Simplified movement logic for demonstration
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for entity_type in ['animals']:
        for entity in entities[entity_type]:
            direction = random.choice(directions)
            for wall in entities['walls']:
                newwall = [0,0]
                newwall[0] = wall['pos'][1]
                newwall[1] = wall['pos'][0]
                newpos = [0,0]
                dir = list(direction)
                newpos[0] = entity['pos'][1] + dir[0]
                newpos[1] = entity['pos'][0] + dir[1]
                if newpos == newwall:
                    hit2 = True
            if hit2 == False:
                entity['pos'][0] = (entity['pos'][0] + direction[1]) % grid_size
                entity['pos'][1] = (entity['pos'][1] + direction[0]) % grid_size
                
def update_screen():
    screen.fill((0, 0, 100))  # Fill screen with green
    draw_health_bar(entities['player']['playerhealth'])
    draw_score(entities['player']['coins'])
    pygame.display.flip()
    for item in entities['items']:
        if(item['type'] == 'ladder' or item['type'] == 'ladderup'):
            screen.blit(ladder_img, (item['pos'][1] * cell_size, item['pos'][0] * cell_size))
        else:
            screen.blit(indoor_img, (item['pos'][1] * cell_size, item['pos'][0] * cell_size))
    for area in entities['areas']:
        screen.blit(indoor_img, (area['pos'][1] * cell_size, area['pos'][0] * cell_size))
    for wall in entities['walls']:
        screen.blit(wall_img, (wall['pos'][1] * cell_size, wall['pos'][0] * cell_size))
    for plant in entities['objects']:
        screen.blit(plant_img, (plant['pos'][1] * cell_size, plant['pos'][0] * cell_size))
    for animal in entities['animals']:
        if animal['health'] < 1:
            sounddie = pygame.mixer.Sound('expl.mp3')
            sounddie.play()
            for drop in enemy_drops[animal['type']]:
                if drop[0] == "Coins":
                    drop1 = drop
                    entities['items'].append({'pos': (animal['pos']), 'type': drop1, 'contains': '', 'descript': 'empty', 'use': 'yes'})
                else:

                    drop1 = drop[0]
                    entities['items'].append({'pos': (animal['pos']), 'type': drop1, 'contains': '', 'descript': 'empty', 'use': 'yes'})
                #print(entities['items'])
                #print("dropped a", enemy_drops[animal['type']][0][0])
            entities['animals'].remove(animal)

        if animal['type'] == 'npc':
            screen.blit(npc_img, (animal['pos'][1] * cell_size, animal['pos'][0] * cell_size))
        if animal['tier'] == 1:
            screen.blit(animaltier1_img, (animal['pos'][1] * cell_size, animal['pos'][0] * cell_size))
        if animal['tier'] == 2:
            screen.blit(animaltier2_img, (animal['pos'][1] * cell_size, animal['pos'][0] * cell_size))
        if animal['tier'] == 3:
            screen.blit(animaltier3_img, (animal['pos'][1] * cell_size, animal['pos'][0] * cell_size))
        if animal['tier'] == 4:
            screen.blit(animaltier4_img, (animal['pos'][1] * cell_size, animal['pos'][0] * cell_size))
        if animal['tier'] == 5:
            screen.blit(animaltier5_img, (animal['pos'][1] * cell_size, animal['pos'][0] * cell_size))
    for carnivore in entities['carnivores']:
        screen.blit(carnivore_img, (carnivore['pos'][1] * cell_size, carnivore['pos'][0] * cell_size))
    if(entities['player']['playerhealth'] < 0):
        reset()
    screen.blit(player_img, (entities['player']['pos'][1] * cell_size, entities['player']['pos'][0] * cell_size))
    pygame.display.flip()

def player_move():
    hit = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:


        for wall in entities['walls']:
            newpos = [0,0]
            newpos[0] = entities['player']['pos'][0] - 1
            newpos[1] = entities['player']['pos'][1]
            if newpos == wall['pos']:
                hit = True
        if hit == False:
            entities['player']['pos'][0] = (entities['player']['pos'][0] - 1) % grid_size


    if keys[pygame.K_s]:

        for wall in entities['walls']:
            newpos = [0,0]
            newpos[0] = entities['player']['pos'][0] + 1
            newpos[1] = entities['player']['pos'][1]
            if newpos == wall['pos']:
                hit = True
        if hit == False:
            entities['player']['pos'][0] = (entities['player']['pos'][0] + 1) % grid_size


    if keys[pygame.K_a]:

        for wall in entities['walls']:
            newpos = [0,0]
            newpos[0] = entities['player']['pos'][0]
            newpos[1] = entities['player']['pos'][1] - 1
            if newpos == wall['pos']:
                hit = True
        if hit == False:
            entities['player']['pos'][1] = (entities['player']['pos'][1] - 1) % grid_size




    if keys[pygame.K_d]:
        for wall in entities['walls']:
            newpos = [0,0]
            newpos[0] = entities['player']['pos'][0]
            newpos[1] = entities['player']['pos'][1] + 1
            if newpos == wall['pos']:
                hit = True
        if hit == False:
            entities['player']['pos'][1] = (entities['player']['pos'][1] + 1) % grid_size

    global stop_threads


    if keys[pygame.K_UP]:
        stop_threads = True                                                                                                              # player mmovement looking up
        for entity_type in ['objects', 'animals', 'items']:
            for objecti in entities[entity_type]:
                objectcheck = list(objecti['pos'])
                objectcheck[0] = objectcheck[0] + 1

                if objectcheck == entities['player']['pos']:
                        stop_speech() 
                        stop_threads = False
                        thread = threading.Thread(target=callchat, args=(objecti,))
                        thread.start()
                #if plant['pos'] == entities['player']['pos'] + entities['player']['pos'][0] + 1: print("plant")
    if keys[pygame.K_DOWN]:
        stop_threads = True                                                                                                              # player mmovement looking up
        for entity_type in ['objects', 'animals', 'items']:
            for objecti in entities[entity_type]:
                objectcheck = list(objecti['pos'])
                objectcheck[0] = objectcheck[0] - 1

                if objectcheck == entities['player']['pos']:
                        stop_speech() 
                        stop_threads = False
                        thread = threading.Thread(target=callchat, args=(objecti,))
                        thread.start()
    if keys[pygame.K_LEFT]:
        stop_threads = True                                                                                                              # player mmovement looking up
        for entity_type in ['objects', 'animals', 'items']:
            for objecti in entities[entity_type]:
                objectcheck = list(objecti['pos'])
                objectcheck[1] = objectcheck[1] + 1

                if objectcheck == entities['player']['pos']:
                        stop_speech() 
                        stop_threads = False
                        thread = threading.Thread(target=callchat, args=(objecti,))
                        thread.start()
    if keys[pygame.K_RIGHT]:
        stop_threads = True                                                                                                              # player mmovement looking up
        for entity_type in ['objects', 'animals', 'items']:
            for objecti in entities[entity_type]:
                objectcheck = list(objecti['pos'])
                objectcheck[1] = objectcheck[1] - 1

                if objectcheck == entities['player']['pos']:
                        stop_speech() 
                        stop_threads = False
                        thread = threading.Thread(target=callchat, args=(objecti,))
                        thread.start()
    for item in entities['items']:      
        global maplevel                                                                                            # pick up ITEMS
        if entities['player']['pos'] == item['pos']:
            if(item)['type'] == 'ladder':
                entities['player']['pos'][0] = entities['player']['pos'][0] + 1 
                maplevel += 1
                reset()
            elif(item)['type'] == 'ladderup':
                entities['player']['pos'][0] = entities['player']['pos'][0] + 1 
                maplevel -= 1
                reset()
            elif(item['type'][0] == "Coins"):
                entities['player']['coins'] += item['type'][1]
                print("picked up",item['type'][1], item['type'][0], "and put it in your bag")
                entities['items'].remove(item)
            else:
                print("picked up", item['type'], "and put it in your bag")
                inventory.append(item)
                entities['items'].remove(item)


def callchat(obj):
    global stop_threads
    while not stop_threads:
        if obj['type'] == "npc":
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)

            print("You said: " + r.recognize_google(audio))
        else:
            
            if 'abletokill' in obj and obj['abletokill'] == True:                                                   # attack enemy

                messages = {"role": "user","content": obj}
                '''chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": "a 10 word story of a battle between you and a " + obj['type'] + "starting with the word" + obj['type']
                            }
                        ],
                        model="gpt-3.5-turbo",    
                )
                reply = chat_completion.choices[0].message.content 
                '''

                attack = random.randint(0, entities['player']['playerdmg'])

                obj['health'] -= attack
                print(obj['type'] + " health: " + str(obj['health']) + "   tier: " + str(obj['tier']))
                hitdmg = random.randint(0, obj['dmg'])
                    
                entities['player']['playerhealth'] -= hitdmg
                print("player health: " + str(entities['player']['playerhealth']))


                reply = obj['type'] + " attacked doing " + str(hitdmg) + "damage" 
                print(reply)
                thread = threading.Thread(target=play_speech, args=(reply,))                    #new thread
                thread.start()
                time.sleep(2)


            else:
                if obj['descript'] == 'empty':

                    if obj['contains'] != '':
                        obj['type'] = str(obj) + " and " + str(contains)
                        print("\n")


                    messages = {"role": "user","content": obj}
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": "in 20 words describe a place with a " + obj['type']
                            }
                        ],
                        model="gpt-3.5-turbo",    
                )
                    reply = "looks at: " + obj['type'] 
                    print(reply)    
                    obj['descript'] = reply
                elif obj['descript'] != '' and obj['use'] == 'no':


                    print(obj['descript'])


                elif obj['descript'] != '' and obj['use'] == 'yes':                 #run a simualtion on usable objects


                    '''messages = {"role": "user","content": obj}
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": "write a 2 word account of what happens when a person uses a " + obj['type'],
                            }
                        ],
                        model="gpt-3.5-turbo",    
                )
                    reply = chat_completion.choices[0].message.content
                    '''
                    print("uses: ", obj['type']) 
        stop_threads = True




def run_game():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    grid_pos = (mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)
                    spawn_animal(grid_pos)
        player_move()
        if random.randint(0, 10) == 3:
            move_entities()  # Move all entities each frame

        update_screen()  # Update the screen with new positions

        clock.tick(12)  # Limit the frame rate to 10 frames per second

run_game()
