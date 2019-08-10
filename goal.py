import pygame


class Goal(pygame.sprite.DirtySprite):
    def __init__(self, scale):
        super().__init__()
        self.scale = scale
        self.color = (255, 144, 0)

        self.image = pygame.Surface((1, 1))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (2*scale-1, 2*scale-1)

    def update(self):
        pass

    def reset(self):
        self.rect.topleft = (2*self.scale-1, 2*self.scale-1)
