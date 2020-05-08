from app.game.constants import CharacterTypes, Masks
from app.objects.skills import Abilities
from app.objects.game_objects.physicals.characters.characters import CharacterObject


class Monster(CharacterObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.character_type = CharacterTypes.MONSTER
        # Set the collider for basic collisions. Monsters can collide into Heroes and Monsters
        self.collider.node().setFromCollideMask(Masks.HERO_AND_MONSTER)
        self.collider.node().setIntoCollideMask(Masks.MONSTER)

        self.experience_rewarded = 1

        self.abilities = Abilities(character=self, enemies=Masks.HERO, allies=Masks.MONSTER)

    def update(self, time_delta, *args, hero=None, **kwargs):
        """
        In short, update as a PhysicalObject, then run whatever enemy-specific logic is to be done.
        The use of a separate "run_logic" method allows us to customise that specific logic to the enemy,
        without re-writing the rest.
        """
        super().update(time_delta, *args, **kwargs)
        assert hero, 'Requires hero keyword.'

        if self.dying:
            death_control = self.actor.getAnimControl("die")
            if death_control is None or not death_control.isPlaying():
                self.dead = True
                self.remove_object_from_world()
            return

        spawn_control = self.actor.getAnimControl("spawn")
        if spawn_control is not None and spawn_control.isPlaying():
            '''If the monster is still playing their spawn animation, they don't take action yet.'''
            return

        self.run_logic(hero, time_delta)

        # Play the appropriate animation. Can be improved? State-machine?
        # Should just be.... self.update_current_animation()
        if self.walking:
            walking_control = self.actor.getAnimControl("walk")
            if not walking_control.isPlaying():
                self.actor.loop("walk")
        else:
            spawn_control = self.actor.getAnimControl("spawn")
            if spawn_control is None or not spawn_control.isPlaying():
                attack_control = self.actor.getAnimControl("attack")
                if attack_control is None or not attack_control.isPlaying():
                    stand_control = self.actor.getAnimControl("stand")
                    if not stand_control.isPlaying():
                        self.actor.loop("stand")

    def run_logic(self, player, time_delta):
        """
        Needs to be implemented for each sub-class.
        """
        raise ValueError('run_logic must be implemented for each monster')

