from panda3d.core import Vec3

from app.objects.abilities import Abilities
from app.objects.attributes import Attributes
from app.objects.proficiencies import Proficiencies
from app.objects.constants import WorldPhysics, CharacterTypes
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
        self.character_type = None
        self.attributes = Attributes(character=self)
        self.proficiencies = Proficiencies(character=self)
        self.abilities = None
        self.experience_rewarded = 0  # Experience earned for killing this unit

        # Possible animations to play
        self.walking = False
        # The starting animation (stand plays if no action is set)
        self.actor.loop("stand")
        # If the model is in the process of dying
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

        # Regenerate pools
        if self.proficiencies.mana.regeneration_cooldown_current == 0:
            self.proficiencies.mana.current += self.proficiencies.mana.regeneration_amount
        else:
            self.proficiencies.mana.regeneration_cooldown_current -= 1
        if self.proficiencies.health.regeneration_cooldown_current == 0:
            self.proficiencies.health.current += self.proficiencies.health.regeneration_amount
        else:
            self.proficiencies.health.regeneration_cooldown_current -= 1

        speed = self.velocity.length()
        if speed > self.proficiencies.movement.speed:
            self.velocity.normalize()
            self.velocity *= self.proficiencies.movement.speed
            speed = self.proficiencies.movement.speed

        if not self.walking:
            friction_value = WorldPhysics.FRICTION * time_delta
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

    def take_damage(self, damage):
        physical = damage.physical * (1 - self.proficiencies.resistances.physical.reduction)
        magical = damage.magical * (1 - self.proficiencies.resistances.magical.reduction)
        frost = damage.frost * (1 - self.proficiencies.resistances.frost.reduction)
        total = physical + magical + frost
        print(f'{damage.source.__class__.__name__} is hurting {self.__class__.__name__} for '
              f'{physical} physical, {magical} magical, and {frost} frost damage.')
        self.update_health(-total, source=damage.source)

    def update_health(self, health_delta, source=None):
        """This is called anytime something will alter this character's health.

        Args:
            health_delta (float): How much to alter the health by.
            source (Character):
        """
        if self.invulnerable:
            pass

        previous_health = self.proficiencies.health.current

        self.proficiencies.health.current += health_delta
        if self.proficiencies.health.current > self.proficiencies.health.maximum:
            self.proficiencies.health.current = self.proficiencies.health.maximum
        if self.proficiencies.health.current <= 0 < previous_health:
            self.die(source)

    def update_health_visual(self):
        """If a visual is required when the character's health changes.
        """
        pass

    def die(self, source):
        if self.character_type == CharacterTypes.MONSTER:
            source.experience += self.experience_rewarded
            source.kills += 1
            self.dying = True
            self.velocity = Vec3(0, 0, 0)
            self.actor.play("die")
            if self.sound_dying is not None:
                self.sound_dying.play()
        elif self.character_type == CharacterTypes.HERO:
            # If the game-over screen isn't showing...
            self.dead = True
