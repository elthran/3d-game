from panda3d.core import CollisionSegment

from random import uniform, randint

from app.objects.effects.freeze import Freeze
from .base import Ability
from app.objects.damage import Damage
from app.objects.effects.stun import Stun


class MeleeAttack(Ability):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Melee Attack"
        self.collision_node = CollisionSegment(0, 0, 0, 1, 0, 0)
        self.description = "Swing your currently equipped weapon at an enemy.."
        self.is_castable = True
        self.animation_timer_max = 0.3  # The delay between the start of an attack, and the attack (potentially) landing
        self.cooldown_timer_max = 0.5

    def get_damage(self, time_delta=None):
        if randint(1,10) == 10:
            effects = [Stun(source=self)]
        elif randint(1,10) > 6:
            effects = [Freeze(source=self)]
        else:
            effects = []
        return Damage(source=self.character,
                      physical=self.character.proficiencies.melee_attack.damage,
                      effects=effects)

    def update(self, operation, key, hero, time_delta):
        active = key.on

        self.update_direct(active, hero, time_delta)

    def update_direct(self, active, hero, time_delta):
        super().update(time_delta)

        if not active:
            return

        self.collision_node.setPointA(self.character.actor.getPos())
        self.collision_node.setPointB(self.character.actor.getPos()
                                      + self.character.actor.getQuat().getForward()
                                      * self.character.proficiencies.melee_attack.distance)

        # If we are currently performing an attack...
        if self.animation_timer_current > 0:
            self.animation_timer_current -= time_delta
            if self.animation_timer_current <= 0:
                # The animation has finished. See if the attack hit with a collision.
                if self.collision_node_queue.getNumEntries() > 0:
                    self.collision_node_queue.sortEntries()
                    segment_hit = self.collision_node_queue.getEntry(0)
                    hit_node_path = segment_hit.getIntoNodePath()
                    if hit_node_path.hasPythonTag("owner"):
                        # Apply damage!
                        hit_object = hit_node_path.getPythonTag("owner")
                        hit_object.take_damage(self.get_damage())
                self.cooldown_timer_current = self.cooldown_timer_max
        # Else if we are capable of making an attack
        elif self.cooldown_timer_current <= 0:
            # Start an attack. The next frame should do the actual attack.
            # The attack lands when the delay_timer gets to 0.
            self.cooldown_timer_current = self.cooldown_timer_max + uniform(0.0, 0.2)
            self.animation_timer_current = self.animation_timer_max
            self.character.actor.play("attack")
        # Else
        else:
            self.cooldown_timer_current -= time_delta
