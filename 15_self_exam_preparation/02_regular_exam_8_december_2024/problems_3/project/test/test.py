from project.senior_student import SeniorStudent

from unittest import TestCase, main

class TestSeniorStudent(TestCase):
    def setUp(self):
        self.student_one = SeniorStudent("12345", "Peter", 5.44)
        self.student_two = SeniorStudent("67890", "Ivan", 5.87)

    def test_init(self):
        self.assertEqual("12345", self.student_one.student_id)
        self.assertEqual("Peter", self.student_one.name)
        self.assertEqual(5.44, self.student_one.student_gpa)
        self.assertEqual(set(), self.student_one.colleges)
        self.assertIsInstance(self.student_one.colleges, set)

    def test_student_id_validation_less_then_4_numbers(self):
        with self.assertRaises(ValueError) as e:
            self.student_one.student_id = " 123  "
        self.assertEqual("Student ID must be at least 4 digits long!", str(e.exception))

    def test_student_id_validation_empty(self):
        with self.assertRaises(ValueError) as e:
            self.student_one.student_id = "       "
        self.assertEqual("Student ID must be at least 4 digits long!", str(e.exception))

    def test_name_validation_empty_string(self):
        with self.assertRaises(ValueError) as e:
            self.student_one.name = ""
        self.assertEqual("Student name cannot be null or empty!", str(e.exception))

    def test_name_validation_white_spaces(self):
        with self.assertRaises(ValueError) as e:
            self.student_one.name = "     "
        self.assertEqual("Student name cannot be null or empty!", str(e.exception))

    def test_student_gpa_validation(self):
        with self.assertRaises(ValueError) as e:
            self.student_one.student_gpa = 0.9
        self.assertEqual("Student GPA must be more than 1.0!", str(e.exception))

    def test_apply_to_college_failed(self):
        result = self.student_one.apply_to_college(6.0, "College One")
        self.assertEqual('Application failed!', result)
        self.assertNotIn("COLLEGE ONE", self.student_one.colleges)
        self.assertEqual(0, len(self.student_one.colleges))

    def test_apply_to_college_applied(self):
        result = self.student_one.apply_to_college(5.0, "College One")
        self.assertEqual('Peter successfully applied to College One.', result)
        self.assertIn("COLLEGE ONE", self.student_one.colleges)
        self.assertEqual(1, len(self.student_one.colleges))

    def test_apply_to_multiple_colleges(self):
        self.student_one.apply_to_college(2.0, "Stanford")
        self.student_one.apply_to_college(3.5, "Yale")
        self.assertIn("STANFORD", self.student_one.colleges)
        self.assertIn("YALE", self.student_one.colleges)

    def test_update_gpa_not_successful(self):
        result = self.student_one.update_gpa(0.0)
        self.assertEqual('The GPA has not been changed!', result)

    def test_update_gpa_not_successful_edge_case(self):
        result = self.student_one.update_gpa(1.0)
        self.assertEqual('The GPA has not been changed!', result)
        self.assertEqual(5.44, self.student_one.student_gpa)

    def test_update_gpa_successful(self):
        result = self.student_one.update_gpa(3.9)
        self.assertEqual('Student GPA was successfully updated.', result)
        self.assertEqual(3.9, self.student_one.student_gpa)

    def test_eq_compare_true_result(self):
        self.student_one.student_gpa = 5.44
        other = SeniorStudent("00000", "Test", 5.44)
        self.assertTrue(self.student_one == other)

    def test_eq_compare_false_result(self):
        self.student_one.student_gpa = 5.64
        other = SeniorStudent("00000", "Test", 5.44)
        self.assertFalse(self.student_one == other)


if __name__ == "__main__":
    main()