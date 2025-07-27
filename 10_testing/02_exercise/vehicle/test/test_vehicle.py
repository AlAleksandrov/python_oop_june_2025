from unittest import main, TestCase

from project.vehicle import Vehicle


class TestVehicle(TestCase):
    fuel = 49.5
    horse_power = 74.5
    def setUp(self):
        self.vehicle = Vehicle(self.fuel, self.horse_power)

    def test_init(self):
        self.assertEqual(self.fuel, self.vehicle.fuel)
        self.assertEqual(self.fuel, self.vehicle.capacity)
        self.assertEqual(self.horse_power, self.vehicle.horse_power)
        self.assertEqual(1.25, self.vehicle.fuel_consumption)

    def test_class_attr(self):
        self.assertIsInstance(self.vehicle.DEFAULT_FUEL_CONSUMPTION, float)
        self.assertIsInstance(self.vehicle.fuel_consumption, float)
        self.assertIsInstance(self.vehicle.fuel, float)
        self.assertIsInstance(self.vehicle.capacity, float)
        self.assertIsInstance(self.vehicle.horse_power, float)

    def test_drive_error(self):
        with self.assertRaises(Exception) as ex:
            self.vehicle.drive(500.)
        self.assertEqual("Not enough fuel", str(ex.exception))

    def test_drive_successful(self):
        self.vehicle.fuel = 50.
        self.vehicle.drive(30.)
        self.assertEqual(12.5, self.vehicle.fuel)

    def test_refuel_error(self):
        with self.assertRaises(Exception) as ex:
            self.vehicle.refuel(80.)
        self.assertEqual("Too much fuel", str(ex.exception))

    def test_refuel_successful(self):
        self.vehicle.fuel = 1.
        self.vehicle.refuel(10.)
        self.assertEqual(11, self.vehicle.fuel)

    def test_str(self):
        expected = f"The vehicle has {self.horse_power} " \
               f"horse power with {self.fuel} fuel left and 1.25 fuel consumption"
        self.assertEqual(expected, self.vehicle.__str__())


if __name__ == "main":
    main()