class TaskManager:
    def __init__(self, app):
        self.app = app
        taskMgr.add(self.update, "update")

    def update(self, task):
        # Get the amount of time since the last update
        time_delta = globalClock.getDt()

        self.app.hero.update(self.app.key_mapper, time_delta)

        self.app.training_dummy_monster.update(self.app.hero, time_delta)

        self.app.sliding_crate_monster.update(self.app.hero, time_delta)

        return task.cont
