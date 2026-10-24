import pygame
import socket
import pickle
import random

pygame.init()

WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Racing - for local")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
GRAY = (200, 200, 200)
ASPHALT = (60, 60, 60)
WHITE_LINE = (255, 255, 255)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
network = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
network.connect(('127.0.0.1', 5555))
player_id = int(network.recv(2048).decode())
car_images = {}
try:
    for i in range(4):
        img = pygame.image.load(f'car{i}.png')
        car_images[i] = pygame.transform.scale(img, (80, 40))
except Exception as e:
    print("There is no image of cars.")
words = [
    "ability", "absence", "academy", "account", "address", "advance", "advisor", "against", "airport", "algebra",
    "already", "analyze", "ancient", "another", "anxiety", "anybody", "apology", "approve", "arrange", "article",
    "attempt", "average", "balance", "battery", "believe", "benefit", "bicycle", "biology", "blanket", "brother",
    "cabinet", "camera", "capital", "captain", "capture", "careful", "carrier", "catalog", "century", "certain",
    "channel", "chapter", "charity", "chicken", "classic", "climate", "collect", "college", "combine", "comfort",
    "command", "comment", "company", "compare", "complex", "concept", "concern", "concert", "conduct", "confirm",
    "connect", "consist", "contact", "contain", "context", "control", "council", "country", "courage", "culture",
    "current", "dataset", "declare", "decline", "deliver", "deposit", "desktop", "destroy", "develop", "diamond",
    "digital", "discuss", "disease", "display", "distance", "divorce", "dynamic", "economy", "edition", "educate",
    "element", "emotion", "emperor", "empower", "endless", "english", "enhance", "episode", "equally", "evening"
]

current_word = random.choice(words)
typed_text = ""
speed = 0.0
position = 0.0

FINISH_LINE = 7000

font = pygame.font.SysFont("Arial", 40)
large_font = pygame.font.SysFont("Arial", 60, bold=True)

start_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT - 120, 200, 60)
restart_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT - 120, 200, 60)

def draw_window(win, state_data):
    win.fill(ASPHALT)
    for i in range(1, 4):
        y_pos = 100 + (i * 120) - 40
        for dash_x in range(0, WIDTH, 40):
            pygame.draw.line(win, WHITE_LINE, (dash_x, y_pos), (dash_x + 20, y_pos), 3)
    finish_x = WIDTH - 150
    pygame.draw.line(win, GREEN, (finish_x, 50), (finish_x, HEIGHT - 150), 10)
    
    all_players = state_data["positions"]
    status = state_data["status"]
    winner_id = state_data["winner"]

    for p_id, pos in all_players.items():
        x = (pos / FINISH_LINE) * finish_x 
        if x > finish_x:
            x = finish_x
            
        y = 100 + (p_id * 120)
        
    
        if p_id in car_images:
            win.blit(car_images[p_id], (x, y))
        else:
            pygame.draw.rect(win, COLORS[p_id], (x, y, 80, 40))
            
        label = "YOU" if p_id == player_id else f"P{p_id + 1}"
        id_text = font.render(label, True, WHITE_LINE)
        win.blit(id_text, (x, y - 40))

    if status == "WAITING":
        pygame.draw.rect(win, GRAY, start_btn)
        start_text = font.render("START", True, BLACK)
        win.blit(start_text, (start_btn.x + 40, start_btn.y + 10))
        
        msg = font.render(" ", True, WHITE_LINE)
        win.blit(msg, (WIDTH//2 - 350, HEIGHT - 120))

    elif status == "FINISHED":
        if winner_id == player_id:
            msg = "You are winner"
            color = GREEN
        else:
            msg = f"P{winner_id + 1} unfortunately , you lose."
            color = COLORS[0]
            
        win_text = large_font.render(msg, True, color)
        text_rect = win_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
        win.blit(win_text, text_rect)

        pygame.draw.rect(win, GRAY, restart_btn)
        restart_text = font.render("RESTART", True, BLACK)
        win.blit(restart_text, (restart_btn.x + 20, restart_btn.y + 10))

    elif status == "RUNNING":
        word_text = font.render(f"Word: {current_word}", True, WHITE_LINE)
        typed_label = font.render(f"Typed: {typed_text}", True, GREEN)
        speed_text = font.render(f"Speed: {speed:.1f}", True, WHITE_LINE)
        
        win.blit(word_text, (50, HEIGHT - 150))
        win.blit(typed_label, (50, HEIGHT - 100))
        win.blit(speed_text, (50, HEIGHT - 50))
    
    pygame.display.update()

def main():
    global current_word, typed_text, speed, position
    clock = pygame.time.Clock()
    run = True
    command = None

    state_data = {
        "positions": {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0},
        "status": "WAITING",
        "winner": -1
    }

    while run:
        clock.tick(60)
        
        if state_data["status"] == "RUNNING":
            if speed > 0:
                position += speed
                speed -= 0.01 
                if speed < 0:
                    speed = 0
        elif state_data["status"] == "WAITING":
            position = 0.0
            speed = 0.0
            if len(typed_text) > 0:
                typed_text = ""
                current_word = random.choice(words)

        try:
            payload = {"position": position, "command": command}
            network.send(pickle.dumps(payload))
            command = None 
            
            state_data = pickle.loads(network.recv(2048))
        except:
            run = False
            print("Server is not available")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if state_data["status"] == "WAITING" and start_btn.collidepoint(mouse_pos):
                    command = "START"
                elif state_data["status"] == "FINISHED" and restart_btn.collidepoint(mouse_pos):
                    command = "RESTART"
                    
            if event.type == pygame.KEYDOWN and state_data["status"] == "RUNNING":
                char = event.unicode.lower()
                if len(typed_text) < len(current_word):
                    expected_char = current_word[len(typed_text)].lower()
                    
                    if char == expected_char:
                        typed_text += char
                        speed += 0.5
                        
                        if typed_text == current_word:
                            current_word = random.choice(words)
                            typed_text = ""
                    else:
                        speed -= 1.0
                        if speed < 0:
                            speed = 0
                        
        draw_window(win, state_data)

    pygame.quit()

if __name__ == "__main__":
    main()
