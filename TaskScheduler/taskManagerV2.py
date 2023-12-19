import pygame
import json
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TASK_HEIGHT = 70
FONT_SIZE = 20
TASK_FILE = "tasks.json"
BEEP_SOUND_FILE = "beeps.wav"
TASK_SPACING = 10

# Colors
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Load tasks from JSON file
def load_tasks():
    with open(TASK_FILE, "r") as file:
        return json.load(file)

# Save tasks to JSON file
def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

# Check if it's Sunday
def is_sunday():
    return datetime.today().weekday() == 6

# Function to draw a task on the screen
def draw_rounded_rect(screen, rect, color, corner_radius):
    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    pygame.draw.rect(screen, color, rect, border_radius=corner_radius)

# Updated draw_task function
def draw_task(screen, task, color, padding=10):
    # Increase the width of the task rectangle to add padding on both sides
    task_width = WINDOW_WIDTH - 2 * padding
    task_rect = pygame.Rect(
        padding,
        task["rect"].y,
        task_width,
        TASK_HEIGHT,
    )
    
    draw_rounded_rect(screen, task_rect, color, corner_radius=10)
    
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render(task["title"], True, (0, 0, 0))
    
    # Center the text within the padded rectangle
    text_rect = text.get_rect(center=task_rect.center)
    
    screen.blit(text, text_rect)


# Main function
def task_manager():
    # Initialize Pygame screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Task Manager")

    tasks = load_tasks()
    last_beep_time = 0  # Initialize the last beep time to 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Handle mouse click event
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for task in tasks:
                    if task["rect"].collidepoint(event.pos):
                        tasks.remove(task)

        # Check if it's midnight and not Sunday
        if datetime.now().time().strftime("%H:%M") == "00:00" and not is_sunday():
            tasks = load_tasks()

        # Clear the screen
        screen.fill((255, 255, 255))

        # Update and draw tasks
        for task in tasks:
            if not isinstance(task["time"], datetime):
                task["time"] = datetime.strptime(task["time"], "%H:%M")

            time_difference = datetime.now() - task["time"]
            task["rect"] = pygame.Rect(
                0,
                tasks.index(task) * (TASK_HEIGHT + TASK_SPACING),
                WINDOW_WIDTH,
                TASK_HEIGHT,
            )
            task["text_position"] = (10, task["rect"].centery - FONT_SIZE / 2)

            if time_difference > timedelta(minutes=15):
                draw_task(screen, task, RED)
                # Check if enough time has passed since the last beep
                if pygame.time.get_ticks() - last_beep_time > 60000:
                    pygame.mixer.Sound(BEEP_SOUND_FILE).play()
                    last_beep_time = pygame.time.get_ticks()  # Update last beep time
            elif time_difference > timedelta(minutes=10):
                draw_task(screen, task, YELLOW)
            else:
                draw_task(screen, task, GREEN)

        # Update the display
        pygame.display.flip()
        clock.tick(300)  # Adjust the frames per second (FPS) as needed

if __name__ == "__main__":
    task_manager()

