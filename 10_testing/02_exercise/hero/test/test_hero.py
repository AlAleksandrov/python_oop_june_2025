from unittest import main, TestCase

from project.hero import Hero


class TestHero(TestCase):
    username = "Test Hero"
    health = 50.
    damage = 75.
    level = 5
    def setUp(self):
        self.hero = Hero(self.username, self.level, self.health, self.damage)

    def test_init(self):
        self.assertEqual(self.username, self.hero.username)
        self.assertEqual(self.health, self.hero.health)
        self.assertEqual(self.damage, self.hero.damage)
        self.assertEqual(self.level, self.hero.level)

    def test_init_attr_type(self):
        self.assertIsInstance(self.hero.username, str)
        self.assertIsInstance(self.hero.health, float)
        self.assertIsInstance(self.hero.damage, float)
        self.assertIsInstance(self.hero.level, int)

    def test_battle_enemy_same_name(self):
        enemy = Hero(self.username, self.level, self.health, self.damage)
        with self.assertRaises(Exception) as ex:
            self.hero.battle(enemy)
        self.assertEqual('You cannot fight yourself', str(ex.exception))

    def test_battle_hero_health_equal_to_zero(self):
        self.hero.health = 0
        enemy = Hero("Enemy", self.level, 60, self.damage)
        with self.assertRaises(ValueError) as e:
            self.hero.battle(enemy)
        self.assertEqual("Your health is lower than or equal to 0. You need to rest", str(e.exception))

    def test_battle_hero_health_under_zero(self):
        self.hero.health = -10
        enemy = Hero("Enemy", self.level, 60, self.damage)
        with self.assertRaises(ValueError) as e:
            self.hero.battle(enemy)
        self.assertEqual("Your health is lower than or equal to 0. You need to rest", str(e.exception))

    def test_battle_enemy_not_enough_health(self):
        enemy = Hero("Enemy", self.level, 0, self.damage)
        with self.assertRaises(ValueError) as e:
            self.hero.battle(enemy)
        self.assertEqual("You cannot fight Enemy. He needs to rest", str(e.exception))

        enemy.health = -10
        with self.assertRaises(ValueError) as e:
            self.hero.battle(enemy)
        self.assertEqual("You cannot fight Enemy. He needs to rest", str(e.exception))

    def test_battle_draw_result(self):
        enemy = Hero("Enemy", self.level, self.health, self.damage)
        result = self.hero.battle(enemy)
        self.assertEqual("Draw", result)
        self.assertEqual(self.level, self.hero.level)
        self.assertEqual(-325.0, self.hero.health)
        self.assertEqual(self.damage, self.hero.damage)
        self.assertEqual(self.level, enemy.level)
        self.assertEqual(-325.0, enemy.health)
        self.assertEqual(self.damage, enemy.damage)

    def test_battle_win_result(self):
        enemy = Hero("Enemy", 1, 1, 1)
        result = self.hero.battle(enemy)
        self.assertEqual("You win", result)
        self.assertEqual(6, self.hero.level)
        self.assertEqual(54., self.hero.health)
        self.assertEqual(80, self.hero.damage)
        self.assertEqual(1, enemy.level)
        self.assertEqual(-374, enemy.health)
        self.assertEqual(1, enemy.damage)

    def test_battle_lose_result(self):
        enemy = Hero("Enemy", 10, 1000, 1000)
        result = self.hero.battle(enemy)
        self.assertEqual("You lose", result)
        self.assertEqual(self.level, self.hero.level)
        self.assertEqual(-9950., self.hero.health)
        self.assertEqual(self.damage, self.hero.damage)
        self.assertEqual(11, enemy.level)
        self.assertEqual(630, enemy.health)
        self.assertEqual(1005, enemy.damage)

    def test_str(self):
        expected =  f"Hero {self.username}: {self.level} lvl\n" \
                    f"Health: {self.health}\n" \
                    f"Damage: {self.damage}\n"
        self.assertEqual(expected, str(self.hero))


if __name__ == "main":
    main()