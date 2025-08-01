from unittest import main,TestCase

from project.soccer_player import SoccerPlayer

class TestSoccerPlayer(TestCase):
    def setUp(self):
        self.player_1 = SoccerPlayer("Player_One", 28, 45, "Barcelona")
        self.player_2 = SoccerPlayer("Player_Two", 25, 60, "Real Madrid")

    def test_init(self):
        self.assertEqual("Player_One", self.player_1.name)
        self.assertEqual(28, self.player_1.age)
        self.assertEqual(45, self.player_1.goals)
        self.assertEqual("Barcelona", self.player_1.team)
        self.assertEqual({}, self.player_1.achievements)

    def test_name_validation(self):
        with self.assertRaises(ValueError) as e:
            self.player_1.name = "One"
        self.assertEqual("Name should be more than 5 symbols!", str(e.exception))

    def test_age_validation(self):
        with self.assertRaises(ValueError) as e:
            self.player_1.age = 15
        self.assertEqual("Players must be at least 16 years of age!", str(e.exception))

    def test_goals_validation(self):
        self.player_1.goals = -1
        self.assertEqual(0, self.player_1.goals)

    def test_team_validation(self):
        with self.assertRaises(ValueError) as e:
            self.player_1.team = "CSKA"
        self.assertEqual(f"Team must be one of the following: Barcelona, Real Madrid, Manchester United, Juventus, PSG!", str(e.exception))

    def test_change_team_valid_name(self):
        result = self.player_1.change_team("Juventus")
        self.assertEqual("Juventus", self.player_1.team)
        self.assertEqual("Team successfully changed!", result)

    def test_change_team_not_valid_name(self):
        result = self.player_1.change_team("CSKA")
        self.assertEqual("Barcelona", self.player_1.team)
        self.assertEqual("Invalid team name!", result)

    def test_add_new_achievement_successful(self):
        result = self.player_1.add_new_achievement("Achievement One")
        self.assertEqual(1, self.player_1.achievements["Achievement One"])
        self.assertEqual(1, len(self.player_1.achievements))
        self.assertEqual("Achievement One has been successfully added to the achievements collection!", result)

    def test_add_new_achievement_unsuccessful(self):
        result = self.player_1.add_new_achievement("Achievement One")
        self.assertEqual(1, self.player_1.achievements["Achievement One"])
        self.assertEqual(1, len(self.player_1.achievements))
        self.assertEqual("Achievement One has been successfully added to the achievements collection!", result)

        result = self.player_1.add_new_achievement("Achievement One")
        self.assertEqual(2, self.player_1.achievements["Achievement One"])
        self.assertEqual(1, len(self.player_1.achievements))
        self.assertEqual("Achievement One has been successfully added to the achievements collection!", result)

    def test_add_new_achievement_unsuccessful_two_diff(self):
        result = self.player_1.add_new_achievement("Achievement One")
        self.assertEqual(1, self.player_1.achievements["Achievement One"])
        self.assertEqual(1, len(self.player_1.achievements))
        self.assertEqual("Achievement One has been successfully added to the achievements collection!", result)

        result = self.player_1.add_new_achievement("Achievement Two")
        self.assertEqual(1, self.player_1.achievements["Achievement Two"])
        self.assertEqual(2, len(self.player_1.achievements))
        self.assertEqual("Achievement Two has been successfully added to the achievements collection!", result)

    def test_lt_compare(self):
        self.assertEqual("Player_Two is a top goal scorer! S/he scored more than Player_One.",
                         self.player_1 < self.player_2)
        self.assertEqual("Player_Two is a better goal scorer than Player_One.",
                         self.player_2 < self.player_1)

    if __name__ == "main":
        main()