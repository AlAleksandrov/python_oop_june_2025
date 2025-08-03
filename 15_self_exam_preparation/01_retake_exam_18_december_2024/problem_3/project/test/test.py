from project.gallery import Gallery
from unittest import TestCase, main


class TestGallery(TestCase):
    def setUp(self):
        self.gallery_one = Gallery("One", "Plovdiv", 125.7, True)
        self.gallery_two = Gallery("Two", "Sofia", 111.3, False)

    def test_init(self):
        self.assertEqual("One", self.gallery_one.gallery_name)
        self.assertEqual("Plovdiv", self.gallery_one.city)
        self.assertEqual(125.7, self.gallery_one.area_sq_m)
        self.assertEqual(True, self.gallery_one.open_to_public)
        self.assertEqual({}, self.gallery_one.exhibitions)

    def test_init_with_different_open_to_public(self):
        self.assertEqual("Two", self.gallery_two.gallery_name)
        self.assertEqual("Sofia", self.gallery_two.city)
        self.assertEqual(111.3, self.gallery_two.area_sq_m)
        self.assertEqual(False, self.gallery_two.open_to_public)
        self.assertEqual({}, self.gallery_two.exhibitions)

    def test_gallery_name_validation(self):
        with self.assertRaises(ValueError) as e:
            self.gallery_one.gallery_name = "Ga Lery"
        self.assertEqual("Gallery name can contain letters and digits only!", str(e.exception))

        with self.assertRaises(ValueError) as e:
            self.gallery_one.gallery_name = "Gallery_70"
        self.assertEqual("Gallery name can contain letters and digits only!", str(e.exception))

        with self.assertRaises(ValueError) as e:
            self.gallery_one.gallery_name = ""
        self.assertEqual("Gallery name can contain letters and digits only!", str(e.exception))

        with self.assertRaises(ValueError) as e:
            self.gallery_one.gallery_name = "    "
        self.assertEqual("Gallery name can contain letters and digits only!", str(e.exception))

    def test_city_validation(self):
        with self.assertRaises(ValueError) as e:
            self.gallery_one.city = "7Days"
        self.assertEqual("City name must start with a letter!", str(e.exception))

        with self.assertRaises(ValueError) as e:
            self.gallery_one.city = ""
        self.assertEqual("City name must start with a letter!", str(e.exception))

    def test_city_valid_with_digits(self):
        try:
            self.gallery_one.city = "Sofia2000"
            self.gallery_one.city = "Plovdiv7"
        except ValueError:
            self.fail("City with digits after first letter should be valid")

    def test_area_sq_m_small_positive(self):
        try:
            self.gallery_one.area_sq_m = 0.001
        except ValueError:
            self.fail("Very small positive area should be valid")

    def test_area_sq_m(self):
        with self.assertRaises(ValueError) as e:
            self.gallery_one.area_sq_m = -120.3
        self.assertEqual("Gallery area must be a positive number!", str(e.exception))

        with self.assertRaises(ValueError) as e:
            self.gallery_one.area_sq_m = 0.0
        self.assertEqual("Gallery area must be a positive number!", str(e.exception))

    def test_add_exhibition_exists(self):
        self.gallery_one.add_exhibition("One", 2025)
        result = self.gallery_one.add_exhibition("One", 2025)
        self.assertEqual('Exhibition "One" already exists.', result)

    def test_add_exhibition_same_name_different_year(self):
        self.gallery_one.add_exhibition("One", 2025)
        result = self.gallery_one.add_exhibition("One", 2026)
        self.assertEqual('Exhibition "One" already exists.', result)

    def test_add_exhibition_not_exists(self):
        self.gallery_one.add_exhibition("One", 2025)
        result = self.gallery_one.add_exhibition("Two", 2025)
        self.assertIn("Two", self.gallery_one.exhibitions)
        self.assertEqual('Exhibition "Two" added for the year 2025.', result)

    def test_remove_exhibition_not_found(self):
        self.gallery_one.exhibitions = {"One": 2025, "Two": 2025, "Three": 2025}
        result = self.gallery_one.remove_exhibition("Four")
        self.assertEqual('Exhibition "Four" not found.', result)

    def test_remove_exhibition_not_found_empty_list(self):
        self.gallery_one.exhibitions = {}
        result = self.gallery_one.remove_exhibition("Four")
        self.assertEqual('Exhibition "Four" not found.', result)

    def test_remove_exhibition_successful(self):
        self.gallery_one.exhibitions = {"One": 2025, "Two": 2025, "Three": 2025}
        result = self.gallery_one.remove_exhibition("Two")
        self.assertEqual('Exhibition "Two" removed.', result)
        self.assertNotIn("Two", self.gallery_one.exhibitions)

    def test_remove_exhibition_successful_single(self):
        self.gallery_one.exhibitions = {"One": 2025}
        result = self.gallery_one.remove_exhibition("One")
        self.assertEqual('Exhibition "One" removed.', result)
        self.assertNotIn("One", self.gallery_one.exhibitions)

    def test_list_exhibitions_open_to_public_single(self):
        self.gallery_one.exhibitions = {"One": 2025}
        result = self.gallery_one.list_exhibitions()
        self.assertEqual("One: 2025", result)

    def test_list_exhibitions_open_to_public_multiple(self):
        self.gallery_one.exhibitions = {"One": 2025, "Two": 2025}
        result = self.gallery_one.list_exhibitions()
        self.assertEqual("One: 2025\nTwo: 2025", result)

    def test_list_exhibitions_open_to_public_empty_list(self):
        self.gallery_one.exhibitions = {}
        result = self.gallery_one.list_exhibitions()
        self.assertEqual("", result)

    def test_list_exhibitions_not_open_to_public(self):
        self.gallery_two.exhibitions = {"One": 2025}
        result = self.gallery_two.list_exhibitions()
        self.assertEqual("Gallery Two is currently closed for public! Check for updates later on.", result)

    def test_list_exhibitions_not_open_to_public_empty_list(self):
        self.gallery_two.exhibitions = {}
        result = self.gallery_two.list_exhibitions()
        self.assertEqual("Gallery Two is currently closed for public! Check for updates later on.", result)


if __name__ == "__main__":
    main()