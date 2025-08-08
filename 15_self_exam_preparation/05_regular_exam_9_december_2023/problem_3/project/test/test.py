from collections import deque
from unittest import TestCase, main

from project.railway_station import RailwayStation


class TestRailwayStation(TestCase):
    def setUp(self):
        self.station = RailwayStation("Sofia")

    def test_init_empty_deque(self):
        self.assertEqual("Sofia", self.station.name)
        self.assertEqual(deque([]), self.station.arrival_trains)
        self.assertEqual(deque([]), self.station.departure_trains)

    def test_init_full_deque(self):
        self.assertEqual("Sofia", self.station.name)
        self.station.arrival_trains = deque(["Train One", "Train Two"])
        self.station.departure_trains = deque(["Train Three"])
        self.assertEqual(deque(["Train One", "Train Two"]), self.station.arrival_trains)
        self.assertEqual(deque(["Train Three"]), self.station.departure_trains)

    def test_name_validation_empty_string(self):
        with self.assertRaises(ValueError) as e:
            self.station.name = ""
        self.assertEqual("Name should be more than 3 symbols!", str(e.exception))

    def test_name_validation_little_than_3(self):
        with self.assertRaises(ValueError) as e:
            self.station.name = "ab"
        self.assertEqual("Name should be more than 3 symbols!", str(e.exception))

    def test_new_arrival_on_board(self):
        self.station.arrival_trains = deque(["Train One", "Train Two"])
        self.assertEqual(deque(["Train One", "Train Two"]), self.station.arrival_trains)
        self.station.new_arrival_on_board("Train Four")
        self.assertEqual(deque(["Train One", "Train Two", "Train Four"]), self.station.arrival_trains)

    def test_train_has_arrived_unsuccessful(self):
        self.station.arrival_trains = deque(["Train One", "Train Two"])
        result = self.station.train_has_arrived("Train Two")
        self.assertEqual("There are other trains to arrive before Train Two.", result)

    def test_train_has_arrived_successful(self):
        self.station.arrival_trains = deque(["Train One", "Train Two"])
        result = self.station.train_has_arrived("Train One")
        self.assertEqual("Train One is on the platform and will leave in 5 minutes.", result)
        self.assertEqual(deque(["Train Two"]), self.station.arrival_trains)
        self.assertEqual(deque(["Train One"]), self.station.departure_trains)

    def test_train_has_left_true(self):
        self.station.departure_trains = deque(["Train One"])
        result = self.station.train_has_left("Train One")
        self.assertTrue(result)
        self.assertEqual(deque([]), self.station.departure_trains)

    def test_train_has_left_false(self):
        self.station.departure_trains = deque(["Train One"])
        result = self.station.train_has_left("Train Two")
        self.assertFalse(result)
        self.assertEqual(deque(["Train One"]), self.station.departure_trains)

if __name__ == "__main__":
    main()