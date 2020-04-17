from app.objects.effects import Effect


class Stun(Effect):
    def __init__(self, source):
        super().__init__(source)
        self.name = "Stun!"
        self.description = "You can't move!"
        self.status_name = "stunned"
