from g_surface import G_Surface


class g_object():
    @property
    def position(self):
        return self.body.position

    @position.setter
    def position(self, val):
        self.body.position = val

    def __init__(self, game, position=(0, 0), angle=0, dynamic=True, additive=(0, 0)):
        self.game = game
        self.additive = additive

        if dynamic:
            body_def = self.game.world.CreateDynamicBody
        else:
            body_def = self.game.world.CreateStaticbody

        self.body = body_def(position=position, angle=angle)

        self.surface = G_Surface()
        self.body.angularDamping = .5
        self.body.userData = self

    def event(self, event):
        pass

    def draw(self):
        center = self.surface.current.get_rect().center
        pos = self.game.to_screen(self.position)
        self.game.screen.blit(self.surface.current, (pos[0] - center[0], pos[1] - center[1]))

    def update(self):
        self.surface.transform(self.body.angle, self.game.camera.zoom)

