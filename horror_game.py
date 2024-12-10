import pygame

pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load background images
office_center = pygame.image.load("/Users/ctongel19/Downloads/Python/FNAF/FNAF_Office_Center.jpg")
office_center = pygame.transform.scale(office_center, (SCREEN_WIDTH, SCREEN_HEIGHT))

office_left = pygame.image.load("/Users/ctongel19/Downloads/Python/FNAF/FNAF_Office_Left.png")
office_left = pygame.transform.scale(office_left, (SCREEN_WIDTH, SCREEN_HEIGHT))

office_right = pygame.image.load("/Users/ctongel19/Downloads/Python/FNAF/FNAF_Office_Right.png")
office_right = pygame.transform.scale(office_right, (SCREEN_WIDTH, SCREEN_HEIGHT))

office_left_closed = pygame.image.load("/Users/ctongel19/Downloads/Python/FNAF/FNAF_Office_Left_Closed.png")
office_left_closed = pygame.transform.scale(office_left_closed, (SCREEN_WIDTH, SCREEN_HEIGHT))

office_right_closed = pygame.image.load("/Users/ctongel19/Downloads/Python/FNAF/FNAF_Office_Right_Closed.png")
office_right_closed = pygame.transform.scale(office_right_closed, (SCREEN_WIDTH, SCREEN_HEIGHT))

office_center_closed = pygame.image.load("/Users/ctongel19/Downloads/Python/FNAF/FNAF_Office_Closed.png")
office_center_closed = pygame.transform.scale(office_center_closed, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game variables
current_view = "center"  # Tracks current view: 'center', 'left', 'right'
is_left_door_closed = False  # Tracks left door state
is_right_door_closed = False  # Tracks right door state
power = 100  # Starting power percentage
power_usage_per_door = 0.01  # Power used per door toggle

# Clock and FPS
clock = pygame.time.Clock()
FPS = 30

def draw_office(view):
    """Draw the office view based on the current view and door states."""
    if view == "center":
        # If both doors are closed, display the center closed image
        if is_left_door_closed and is_right_door_closed:
            screen.blit(office_center_closed, (0, 0))
        else:
            screen.blit(office_center, (0, 0))
            if is_left_door_closed:  # Overlay left door closed state
                screen.blit(office_left_closed, (0, 0))
            if is_right_door_closed:  # Overlay right door closed state
                screen.blit(office_right_closed, (0, 0))
    elif view == "left":
        # Display left view with door state
        screen.blit(office_left_closed if is_left_door_closed else office_left, (0, 0))
    elif view == "right":
        # Display right view with door state
        screen.blit(office_right_closed if is_right_door_closed else office_right, (0, 0))

def draw_power_bar():
    """Draw the power bar on the screen."""
    power_bar_width = 200
    power_bar_height = 20
    power_bar_x = 10
    power_bar_y = 10
    
    # Draw the background of the power bar (gray)
    pygame.draw.rect(screen, (100, 100, 100), (power_bar_x, power_bar_y, power_bar_width, power_bar_height))
    
    # Draw the current power (green)
    pygame.draw.rect(screen, (0, 255, 0), (power_bar_x, power_bar_y, power_bar_width * (power / 100), power_bar_height))

def update_power():
    """Update the power based on door usage."""
    global power
    if is_left_door_closed or is_right_door_closed:
        power -= power_usage_per_door
        if power < 0:
            power = 0  # Ensure power doesn't go below 0

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle door toggle on key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Toggle left door
                is_left_door_closed = not is_left_door_closed
            if event.key == pygame.K_e:  # Toggle right door
                is_right_door_closed = not is_right_door_closed

    # Handle key inputs for changing views
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Look left
        current_view = "left"
    elif keys[pygame.K_d]:  # Look right
        current_view = "right"
    else:  # Default to center view
        current_view = "center"

    update_power()
    draw_office(current_view)
    draw_power_bar()

    # Check if power is 0, then stop the game (or trigger an event)
    if power == 0:
        font = pygame.font.SysFont(None, 55)
        text = font.render("Power Out!", True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)  # Show "Power Out!" message for 2 seconds
        running = False  # End the game

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
