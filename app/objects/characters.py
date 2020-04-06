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
        self.experience = 0
        self.experience_awarded_on_death = 1
        self.attributes = Attributes(character=self)
        self.proficiencies = Proficiencies(character=self)
        self.abilities = None
        self.walking = False
        self.actor.loop("stand")
        self.dying = False
        self.dead = False

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

        if self.actor is not None:
            self.actor.setFluidPos(self.velocity * time_delta + self.actor.getPos())

    def update_current_animation(self):
        pass
        # # Heroes
        # if self.walking:
        #     stand_control = self.actor.getAnimControl("stand")
        #     if stand_control.isPlaying():
        #         stand_control.stop()
        #     walk_control = self.actor.getAnimControl("walk")
        #     if not walk_control.isPlaying():
        #         self.actor.loop("walk")
        # else:
        #     stand_control = self.actor.getAnimControl("stand")
        #     if not stand_control.isPlaying():
        #         self.actor.stop("walk")
        #         self.actor.loop("stand")
        # # Monsters
        # if self.walking:
        #     walking_control = self.actor.getAnimControl("walk")
        #     if not walking_control.isPlaying():
        #         self.actor.loop("walk")
        # else:
        #     spawn_control = self.actor.getAnimControl("spawn")
        #     if spawn_control is None or not spawn_control.isPlaying():
        #         attack_control = self.actor.getAnimControl("attack")
        #         if attack_control is None or not attack_control.isPlaying():
        #             stand_control = self.actor.getAnimControl("stand")
        #             if not stand_control.isPlaying():
        #                 self.actor.loop("stand")

    def update_health(self, health_delta, damage_dealer=None):
        """This is called anytime something will alter this character's health.

        Args:
            health_delta (float): How much to alter the health by.
        """
        if self.invulnerable:
            pass
        print(damage_dealer.__class__.__name__)

        previous_health = self.proficiencies.health.current

        self.proficiencies.health.current += health_delta
        if self.proficiencies.health.current > self.proficiencies.health.maximum:
            self.proficiencies.health.current = self.proficiencies.health.maximum
        if self.proficiencies.health.current <= 0 < previous_health:
            self.die(damage_dealer)
        print(f"{self.__class__.__name__} is now at {self.proficiencies.health.current} health.")

    def update_health_visual(self):
        """If a visual is required when the character's health changes.
        """
        pass

    def die(self, damage_dealer):
        print(f"{self.__class__.__name__} died.")
        self.dying = True
        self.collider.removeNode()
        self.actor.play("die")
        if damage_dealer.__class__.__name__ == 'WizardHero':
            damage_dealer.experience += self.experience_awarded_on_death
            print(f"{damage_dealer.__class__.__name__} now has {damage_dealer.experience} total experience!")

