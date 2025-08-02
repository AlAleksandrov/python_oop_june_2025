from project.furniture import Furniture

from unittest import main, TestCase

class TestFurniture(TestCase):
    def setUp(self):
        self.furniture_1 = Furniture("Furniture_One", 355, (120, 130, 200), True, 80)
        self.furniture_2 = Furniture("Furniture_Two", 255, (110, 120, 180), False)

    def test_init(self):
        self.assertEqual("Furniture_One", self.furniture_1.model)
        self.assertEqual(355, self.furniture_1.price)
        self.assertEqual((120, 130, 200), self.furniture_1.dimensions)
        self.assertEqual(True, self.furniture_1.in_stock)
        self.assertEqual(80, self.furniture_1.weight)

    def test_model_validation(self):
        with self.assertRaises(ValueError) as e:
            self.furniture_1.model = ""
        self.assertEqual("Model must be a non-empty string with a maximum length of 50 characters.", str(e.exception))

        with self.assertRaises(ValueError) as e:
            self.furniture_1.model = "111111111111111111111111111111111111111111111111111"
        self.assertEqual("Model must be a non-empty string with a maximum length of 50 characters.", str(e.exception))

    def test_price_validation(self):
        with self.assertRaises(ValueError) as e:
            self.furniture_1.price = -1.0
        self.assertEqual("Price must be a non-negative number.", str(e.exception))

    def test_dimension_validation(self):
        with self.assertRaises(ValueError) as e:
            self.furniture_1.dimensions = (100, 100)
        self.assertEqual("Dimensions tuple must contain 3 integers.", str(e.exception))

        with self.assertRaises(ValueError) as e:
            self.furniture_1.dimensions = (100, 100, -30)
        self.assertEqual("Dimensions tuple must contain integers greater than zero.", str(e.exception))

        with self.assertRaises(ValueError) as e:
            self.furniture_1.dimensions = (100, 100, 0)
        self.assertEqual("Dimensions tuple must contain integers greater than zero.", str(e.exception))

    def test_weight_validation(self):
        with self.assertRaises(ValueError) as e:
            self.furniture_1.weight = -1.0
        self.assertEqual("Weight must be greater than zero.", str(e.exception))

        with self.assertRaises(ValueError) as e:
            self.furniture_1.weight = 0.0
        self.assertEqual("Weight must be greater than zero.", str(e.exception))

    def test_get_available_status(self):
        self.furniture_1.model = "Furniture_One"
        result = self.furniture_1.get_available_status()
        self.assertEqual("Model: Furniture_One is currently in stock.", result)

        self.furniture_2.model = "Furniture_Two"
        result = self.furniture_2.get_available_status()
        self.assertEqual("Model: Furniture_Two is currently unavailable.", result)

    def test_get_specifications(self):
        self.furniture_1.model = "Furniture_One"
        result = self.furniture_1.get_specifications()
        self.assertEqual("Model: Furniture_One has the following dimensions: 120mm x 130mm x 200mm and weighs: 80", result)

        self.furniture_2.model = "Furniture_One"
        result = self.furniture_2.get_specifications()
        self.assertEqual("Model: Furniture_One has the following dimensions: 110mm x 120mm x 180mm and weighs: N/A",
                         result)

if __name__ == "__main__":
    main()