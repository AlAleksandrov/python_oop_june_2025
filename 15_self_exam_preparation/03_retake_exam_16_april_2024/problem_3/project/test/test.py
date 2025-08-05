from unittest import TestCase, main

from project.restaurant import Restaurant


class TestRestaurant(TestCase):
    def setUp(self):
        self.restaurant = Restaurant("The Best", 99)

    def test_init(self):
        self.assertEqual("The Best", self.restaurant.name)
        self.assertEqual(99, self.restaurant.capacity)
        self.assertEqual([], self.restaurant.waiters)

    def test_name_validation_empty_string(self):
        with self.assertRaises(ValueError) as e:
            self.restaurant.name = ""
        self.assertEqual("Invalid name!", str(e.exception))

    def test_name_validation_white_spaces(self):
        with self.assertRaises(ValueError) as e:
            self.restaurant.name = "      "
        self.assertEqual("Invalid name!", str(e.exception))

    def test_get_waiters_with_none_earnings(self):
        self.restaurant.waiters = [{"name": "John"}, {"name": "Jane"}]
        self.assertEqual([{'name': "John"}, {'name': "Jane"}], self.restaurant.get_waiters())

    def test_get_waiters_with_real_earnings(self):
        self.restaurant.waiters = [{"name": "John"}, {"name": "Jane"}]
        self.assertEqual([], self.restaurant.get_waiters(10, 30))

    def test_get_waiters_with_min_and_max_earnings(self):
        self.restaurant.waiters = [
            {"name": "John", "total_earnings": 100},
            {"name": "Jane", "total_earnings": 150},
            {"name": "Joe", "total_earnings": 200}
        ]
        result = self.restaurant.get_waiters(min_earnings=120, max_earnings=180)
        self.assertEqual([{"name": "Jane", "total_earnings": 150}], result)

    def test_capacity_validation_less_than_0(self):
        with self.assertRaises(ValueError) as e:
            self.restaurant.capacity = -1
        self.assertEqual("Invalid capacity!", str(e.exception))

    def test_add_waiter_no_more_places(self):
        self.restaurant.capacity = 1
        self.restaurant.add_waiter("John")
        self.assertEqual([{'name': "John"}], self.restaurant.waiters)
        self.assertEqual(1, len(self.restaurant.waiters))
        result = self.restaurant.add_waiter("Jo")
        self.assertEqual("No more places!", result)

    def test_add_waiter_with_existing_waiter(self):
        self.restaurant.add_waiter("John")
        self.assertEqual([{'name': "John"}], self.restaurant.waiters)
        self.assertEqual(1, len(self.restaurant.waiters))
        self.assertIn("John", self.restaurant.waiters[0]["name"])
        result = self.restaurant.add_waiter("John")
        self.assertEqual(f"The waiter John already exists!", result)

    def test_add_waiter_successful(self):
        self.restaurant.add_waiter("John")
        self.assertEqual([{'name': "John"}], self.restaurant.waiters)
        self.assertEqual(1, len(self.restaurant.waiters))
        self.assertIn("John", self.restaurant.waiters[0]["name"])

    def test_remove_waiter_no_waiters(self):
        result = self.restaurant.remove_waiter("John")
        self.assertEqual("No waiter found with the name John.", result)
        self.assertEqual(0, len(self.restaurant.waiters))
        self.assertEqual([], self.restaurant.waiters)

    def test_remove_waiter_with_waiters(self):
        self.restaurant.waiters = [{"name": "Johny"}, {"name": "Jane"}]
        result = self.restaurant.remove_waiter("John")
        self.assertEqual("No waiter found with the name John.", result)
        self.assertEqual(2, len(self.restaurant.waiters))
        self.assertEqual([{'name': "Johny"}, {"name": "Jane"}], self.restaurant.waiters)

    def test_remove_waiter_with_waiters_successful(self):
        self.restaurant.waiters = [{"name": "John"}, {"name": "Jane"}]
        self.assertEqual(2, len(self.restaurant.waiters))
        result = self.restaurant.remove_waiter("John")
        self.assertEqual("The waiter John has been removed.", result)
        self.assertEqual(1, len(self.restaurant.waiters))
        self.assertEqual([{"name": "Jane"}], self.restaurant.waiters)

    def test_get_total_earnings_with_no_earnings(self):
        self.assertEqual(0, self.restaurant.get_total_earnings())

    def test_get_total_earnings_with_earnings(self):
        self.restaurant.waiters = [
            {"name": "John", "total_earnings": 40},
            {"name": "Jane", "total_earnings": 60}
        ]
        self.assertEqual(100, self.restaurant.get_total_earnings())