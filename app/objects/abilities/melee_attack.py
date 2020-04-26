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
        self.progress_time = 0.3  # The delay between the start of an attack, and the attack (potentially) landing
        self.progress_timer = 0  # Init the timer
        self.wait_timer = 0.2  # How long to wait between attacks

    def get_damage(self, time_delta=None):
        if randint(1,10) == 10:
            effects = [Stun(source=self)]
        elif randint(1,10) > 8:
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

        if self.progress_timer > 0:
            self.progress_timer -= time_delta
            if self.progress_timer <= 0:
                # The animation has finished. See if the attack hit with a collision.
                if self.collision_node_queue.getNumEntries() > 0:
                    self.collision_node_queue.sortEntries()
                    segment_hit = self.collision_node_queue.getEntry(0)
                    hit_node_path = segment_hit.getIntoNodePath()
                    if hit_node_path.hasPythonTag("owner"):
                        # Apply damage!
                        hit_object = hit_node_path.getPythonTag("owner")
                        hit_object.take_damage(self.get_damage())
                self.wait_timer = 1.0
        # If we're instead waiting to be allowed to attack...
        elif self.wait_timer > 0:
            self.wait_timer -= time_delta
            # If the wait has ended...
            if self.wait_timer <= 0:
                # Start an attack. The next frame should do the actual attack.
                # The attack lands when the delay_timer gets to 0.
                self.wait_timer = uniform(0.5, 0.7)
                self.progress_timer = self.progress_time
                self.character.actor.play("attack")