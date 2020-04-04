from app.objects.physicals import PhysicalObject


class StaticObject(PhysicalObject):
    def __init__(self, pos, model_name, model_animation):
        PhysicalObject.__init__(self, pos, model_name, model_animation)