from gamesurface import GameSurface
from Box2D import b2Vec2 as Vec2
import Box2D as B2


class GameObject():
    def get_position(self):
        return self.body.position

    def set_position(self, val):
        print(self.name)
        self.body.position = val

    def get_angle(self):
        return self.body.angle

    def set_angle(self, val):
        self.body.angle = val

    def __init__(self, game, position=(0.0, 0.0), angle=0, dynamic=True, additive=(0.0, 0.0), is_inside=True,
                 image='default.png', body=None):
        self.game = game
        self.additive = additive
        self.is_inside = is_inside

        if dynamic:
            body_def = self.game.world.CreateDynamicBody
        else:
            body_def = self.game.world.CreateStaticBody

        if body:
            self.body = body
        else:
            self.body = body_def(position=position, angle=angle, angularDamping=1.8)

        self.surface = GameSurface()
        self.surface.load(image)
        self.body.userData = self

    def event(self, event):
        pass

    def draw(self):
        center = self.surface.current.get_rect().center
        pos = self.game.to_screen(self.get_position())
        self.game.screen.blit(self.surface.current, Vec2(pos) - Vec2(center))

    def update(self):
        self.surface.transform(self.body.angle, self.game.camera.zoom)

