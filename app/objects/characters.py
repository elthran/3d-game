from app.objects.abilities import Abilities
from app.objects.attributes import Attributes
from app.objects.proficiencies import Proficiencies
from app.objects.constants_physics import FRICTION
from app.objects.physicals import PhysicalObject


class CharacterObject(PhysicalObject):
    """A character object. Generally capable of walking, attacking, interacting, responding, etc.

    Attributes:
        attributes (Attributes): All attributes accessible by the character.
        proficiencies (Proficiencies): All proficiencies accessible by the character.
        abilities (Abilities): All abilities accessible by the character.
        walking (bool): If the character is currently walking (mainly used for display).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attributes = Attributes(character=self)
        self.proficiencies = Proficiencies(character=self)
        self.abilities = None
        self.walking = False
        self.actor.loop("stand")

    def refresh(self):
        """Sets cooldowns to zero and fully restores proficiencies to their maximum values.
        """
        self.attributes.refresh()
        self.proficiencies.refresh()
        self.abilities.refresh()

    def update(self, time_delta, *args, **kwargs):
        """What gets done after every frame of the game.

        Args:
            time_delta (float): Time since the last frame?
        """
        super().update(time_delta, *args, **kwargs)

        speed = self.velocity.length()
        if speed > self.proficiencies.movement.speed:
            self.velocity.normalize()
            self.velocity *= self.proficiencies.movement.speed
            speed = self.proficiencies.movement.speed

        if not self.walking:
            friction_value = FRICTION * time_delta
            if friction_value > speed:
                self.velocity.set(0, 0, 0)
            else:
                friction_vector = -self.velocity
                friction_vector.normalize()
                friction_vector *= friction_value
                self.velocity += friction_vector

        self.actor.setFluidPos(self.velocity * time_delta + self.actor.getPos())

    def update_health(self, health_delta):
        """This is called anytime something will alter this character's health.

        Args:
            health_delta (float): How much to alter the health by.
        """
        if self.invulnerable:
            pass

        previous_health = self.proficiencies.health.current

        self.proficiencies.health.current += health_delta
        if self.proficiencies.health.current > self.proficiencies.health.maximum:
            self.proficiencies.health.current = self.proficiencies.health.maximum
        if self.proficiencies.health.current <= 0 < previous_health:
            print(f"{self.__class__.__name__} died.")
        print(f"{self.__class__.__name__} is now at {self.proficiencies.health.current} health.")

    def update_health_visual(self):
        """If a visual is required when the character's health changes.
        """
        pass
