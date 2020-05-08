from app.objects.proficiencies.generic_spendable_resource import GenericSpendableResource


class Mana(GenericSpendableResource):
    def __init__(self, *args):
        super().__init__(*args)
        self.name = 'Mana'
        self.description = 'Determines maximum mana.'
        self.base_maximum = 5

    @property
    def hero_attribute_bonus(self):
        return self.character.attributes.intellect.level * 3

    def __str__(self):
        return __class__.__name__