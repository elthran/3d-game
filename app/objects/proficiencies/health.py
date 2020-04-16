from app.objects.proficiencies.generic_spendable_resource import GenericSpendableResource


class Health(GenericSpendableResource):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Health'
        self.description = 'Determines maximum health.'
        self.base_maximum = 5

    @property
    def maximum(self):
        return self.base_maximum + self.bonus_maximum + self.character.attributes.vitality.level * 1


