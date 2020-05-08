from panda3d.core import CollisionNode, CollisionHandlerQueue, AudioSound

from app.game.constants import Masks, Keys
from app.objects.damage import Damage
from app.objects.game_objects.game_objects import GameObject
from app.objects.game_objects.physicals.physicals import PhysicalObject


class Ability(GameObject):
    def __init__(self, character, enemies, allies, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.character = character
        self.name = None
        self._level = 0
        self.skill_tree = None  # Which skill tree this will appear in (maximum of 1)

        # Types (only one can be true)
        self.is_castable = False  # Means it can be activated
        self.is_permanent = False  # Means it is always on after being learned
        self.is_equipped = False

        # Temp
        self.tool_belt_key = None

        # Miscellaneous
        self.cooldown_timer_max = 0
        self.cooldown_timer_current = 0
        self.animation_timer_max = 0
        self.animation_timer_current = 0

        # Physics
        self.collision_node = None
        self.collision_node_path = None
        self.collision_node_queue = None
        self.from_collider_attack = enemies
        self.from_collider_protect = allies
        self.from_collider_all = Masks.HERO_AND_MONSTER
        self.into_collider = Masks.NONE

        # Display
        self.beam_hit_light_node_path = None
        self.model = None  # The basic model of the animation
        self.model_collision = None  # The model when the animation collides with another object

        # Sound
        self.sound_miss_file_path = None
        self.sound_hit_file_path = None
        self.sound_damage_file_path = None
        self.sound_miss = None
        self.sound_hit = None
        self.sound_damage = None

    @property
    def description(self):
        raise ValueError("Must set description.")

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_value):
        if self.level == 0:
            if self.is_permanent:
                self.apply()
            elif self.is_castable:
                self.equip_to_tool_belt(Keys.MOUSE_RIGHT)
        self._level = new_value

    def equip_to_tool_belt(self, key=None):
        self.is_equipped = True
        self.physics_init()
        self.sound_init()
        self.display_init()
        if key:
            self.tool_belt_key = key
            self.character.tool_belt.add_action(key, self, None)

    def unequip_from_tool_belt(self):
        self.is_equipped = False
        self.character.tool_belt.remove_action(self.tool_belt_key)
        self.tool_belt_key = None
        self.remove_object_from_world()

    def physics_init(self):
        if self.collision_node is None:
            return
            # raise ValueError("Can't initiate physics model without a declared collision_node.")
        collision_node = CollisionNode(self.__class__.__name__)
        collision_node.addSolid(self.collision_node)
        collision_node.setFromCollideMask(self.from_collider_attack)
        collision_node.setIntoCollideMask(self.into_collider)
        self.collision_node_path = render.attachNewNode(collision_node)
        self.collision_node_path.show()
        self.collision_node_queue = CollisionHandlerQueue()
        # We want this node to collide with things, so tell our traverser about it.
        # However, we don't have to tell our "CollisionHandlerQueue" about it.
        base.cTrav.addCollider(self.collision_node_path, self.collision_node_queue)

    def display_init(self):
        pass

    def sound_init(self):
        if self.sound_miss_file_path:
            self.sound_miss = loader.loadSfx(self.sound_miss_file_path)
            self.sound_miss.setLoop(True)
        if self.sound_hit_file_path:
            self.sound_hit = loader.loadSfx(self.sound_hit_file_path)
            self.sound_hit.setLoop(True)
        if self.sound_damage_file_path:
            self.sound_damage = loader.loadSfx(self.sound_damage_file_path)

    def get_damage(self, time_delta=None):
        return Damage()

    def apply(self):
        raise AttributeError("Must be defined")

    def update(self, time_delta, *args, **kwargs):
        super().update(time_delta, *args, **kwargs)

    def remove_object_from_world(self):
        if self.sound_hit and self.sound_hit.status() == AudioSound.PLAYING:
            self.sound_hit.stop()
        if self.sound_miss and self.sound_miss.status() == AudioSound.PLAYING:
            self.sound_miss.stop()
        if self.sound_damage and self.sound_damage.status() == AudioSound.PLAYING:
            self.sound_damage.stop()
        if self.collision_node is not None and self.model_collision is not None:
            self.model_collision.removeNode()
            base.cTrav.removeCollider(self.collision_node_path)
        if self.beam_hit_light_node_path is not None:
            render.clearLight(self.beam_hit_light_node_path)
            self.beam_hit_light_node_path.removeNode()
        PhysicalObject.remove_object_from_world(self)

    def __str__(self):
        return self.__class__.__name__
