from app.Objects.characters import CharacterObject


# class Interactive(CharacterObject):
#     def __init__(self, starting_position, model_name, model_animation):
#         super().__init__(starting_position, model_name, model_animation)
#
#     def update_position(self, player, time_delta):
#         """
#         In short, update as a PhysicalObject, then run whatever enemy-specific logic is to be done.
#         The use of a separate "run_logic" method allows us to customise that specific logic to the enemy,
#         without re-writing the rest.
#
#         :param player:
#         :param time_delta:
#         :return:
#         """
#         self.update_position(self, time_delta)
#
#
# class CrateInteractive(Interactive):
#     def __init__(self, starting_position, model_name, model_animation):
#         super().__init__(self, starting_position,
#                          model_name="Models/PandaChan/act_p3d_chan",
#                          model_animation={"stand": "Models/Misc/trap-stand"})
#
#         base.pusher.addCollider(self.collider, self.actor)
#         base.cTrav.addCollider(self.collider, base.pusher)
#
#         self.actor.loop("stand")



