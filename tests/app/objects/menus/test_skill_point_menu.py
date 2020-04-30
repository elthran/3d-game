from app.objects.menus.skill_point_select import SkillPointSelect


class TestSkillPointSelectMenu:
    def test_enter_menu(self, started_game):
        skill_point_select_menu = SkillPointSelect(started_game)
        skill_point_select_menu.enter_menu(hero=started_game.hero)
        assert skill_point_select_menu.choose_skill("Regrowth") is None



