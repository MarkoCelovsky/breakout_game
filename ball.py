import pygame
import random 

BLACK = (0, 0, 0)

class Ball(pygame.sprite.Sprite):
    # This class represents a ball. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, radius):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the ball, and its radius.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the ball (a circle!)
        pygame.draw.circle(self.image, color, (radius, radius), radius)

        self.velocity = [random.randint(4, 8), random.randint(-8, 8)]

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect(center=(radius, radius))

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = random.choice([-1, 1]) * random.randint(3, 4)

    def bouncePaddle(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = random.choice([-1, 1]) * random.randint(3, 4)
        # self.velocity[1] = random.randint(-8,8)
