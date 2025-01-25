
WIDTH, HEIGHT = 900, 600

class Camera:
    def __init__(self, group):
        self.dx = 0
        self.dy = 0
        self.group = group

    def apply(self):
        for sprite in self.group:
            sprite.rect.x += self.dx
            sprite.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)