from project.legendary_item import LegendaryItem

from unittest import TestCase, main

class TestLegendaryItem(TestCase):
    def setUp(self):
        self.item = LegendaryItem("Sword", 300, 20, 500)

    def test_init(self):
        self.assertEqual("Sword", self.item.identifier)
        self.assertEqual(300, self.item.power)
        self.assertEqual(20, self.item.durability)
        self.assertEqual(500, self.item.price)

    def test_identifier_validation_not_contain_only_letters_digits_or_hyphens(self):
        with self.assertRaises(ValueError) as e:
            self.item.identifier = "$_I8ne"
        self.assertEqual("Identifier can only contain letters, digits, or hyphens!", str(e.exception))

    def test_identifier_validation_len_under_four(self):
        with self.assertRaises(ValueError) as e:
            self.item.identifier = "One"
        self.assertEqual("Identifier must be at least 4 characters long!", str(e.exception))

    def test_power_validation_under_zero(self):
        with self.assertRaises(ValueError) as e:
            self.item.power = -1
        self.assertEqual("Power must be a non-negative integer!", str(e.exception))

    def test_durability_validation_under_zero(self):
        with self.assertRaises(ValueError) as e:
            self.item.durability = -1
        self.assertEqual("Durability must be between 1 and 100 inclusive!", str(e.exception))

    def test_durability_validation_above_hundred(self):
        with self.assertRaises(ValueError) as e:
            self.item.durability = 120
        self.assertEqual("Durability must be between 1 and 100 inclusive!", str(e.exception))

    def test_price_validation_with_zero(self):
        with self.assertRaises(ValueError) as e:
            self.item.price = 0
        self.assertEqual("Price must be a multiple of 10 and not 0!", str(e.exception))

    def test_price_validation_with_other_number_that_is_not_a_multiple_of_10(self):
        with self.assertRaises(ValueError) as e:
            self.item.price = 5
        self.assertEqual("Price must be a multiple of 10 and not 0!", str(e.exception))

    def test_is_precious_validation_true(self):
        self.item.power = 60
        self.assertTrue(self.item.is_precious)

    def test_is_precious_validation_false(self):
        self.item.power = 20
        self.assertFalse(self.item.is_precious)

    def test_enhance_validation_durability_under_hundred(self):
        self.item.enhance()
        self.assertEqual(600, self.item.power)
        self.assertEqual(510, self.item.price)
        self.assertEqual(30, self.item.durability)

    def test_enhance_validation_durability_with_hundred(self):
        self.item.enhance()
        self.assertEqual(600, self.item.power)
        self.assertEqual(510, self.item.price)
        self.item.durability = 100
        self.assertEqual(100, self.item.durability)

    def test_evaluate_validation_eligible_is_precious_true(self):
        result = self.item.evaluate(1)
        self.assertEqual("Sword is eligible.", result)

    def test_evaluate_validation_not_eligible_is_precious_false(self):
        self.item.power = 20
        result = self.item.evaluate(1)
        self.assertEqual("Item not eligible.", result)

    def test_evaluate_validation_not_eligible_min_durability_above_durability_and_is_precious_true(self):
        result = self.item.evaluate(30)
        self.assertEqual("Item not eligible.", result)

    def test_evaluate_validation_not_eligible_min_durability_above_durability_and_is_precious_false(self):
        self.item.power = 20
        result = self.item.evaluate(30)
        self.assertEqual("Item not eligible.", result)


if __name__ == "__main__":
    main()