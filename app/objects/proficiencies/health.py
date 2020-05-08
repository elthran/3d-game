from app.objects.proficiencies.generic_spendable_resource import GenericSpendableResource


class Health(GenericSpendableResource):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Health'
        self.description = 'Determines maximum health.'
        self.base_maximum = 5

    @property
    def hero_attribute_bonus(self):
        return self.character.attributes.vitality.level * 2

    def __str__(self):
        return __class__.__name__


