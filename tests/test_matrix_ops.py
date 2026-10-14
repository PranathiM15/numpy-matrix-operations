"""Unit tests for the NumPy calculations and their input validation."""
import unittest

from matrix_ops import calculate


A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
B = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]


class MatrixOperationsTests(unittest.TestCase):
    def test_addition(self):
        result = calculate(A, B, "add")
        self.assertEqual(result["result"], [[10, 10, 10], [10, 10, 10], [10, 10, 10]])
        self.assertEqual(result["shape"], [3, 3])

    def test_subtraction(self):
        result = calculate(A, B, "subtract")
        self.assertEqual(result["result"], [[-8, -6, -4], [-2, 0, 2], [4, 6, 8]])

    def test_matrix_multiplication(self):
        result = calculate(A, B, "multiply")
        self.assertEqual(result["result"], [[30, 24, 18], [84, 69, 54], [138, 114, 90]])

    def test_transpose_a(self):
        result = calculate([[1, 2, 3], [4, 5, 6]], [[1]], "transpose_a")
        self.assertEqual(result["result"], [[1, 4], [2, 5], [3, 6]])
        self.assertEqual(result["shape"], [3, 2])

    def test_transpose_b(self):
        result = calculate([[1]], [[1, 2], [3, 4]], "transpose_b")
        self.assertEqual(result["result"], [[1, 3], [2, 4]])

    def test_addition_requires_same_shape(self):
        with self.assertRaisesRegex(ValueError, "same dimensions"):
            calculate([[1, 2]], [[1], [2]], "add")

    def test_multiplication_requires_compatible_shapes(self):
        with self.assertRaisesRegex(ValueError, "columns in A"):
            calculate([[1, 2, 3]], [[1, 2]], "multiply")

    def test_rejects_non_finite_values(self):
        with self.assertRaisesRegex(ValueError, "finite numbers"):
            calculate([[float("nan")]], [[1]], "add")

    def test_rejects_unknown_operation(self):
        with self.assertRaisesRegex(ValueError, "Choose addition"):
            calculate(A, B, "divide")

    def test_rejects_non_matrix_input(self):
        with self.assertRaisesRegex(ValueError, "two-dimensional"):
            calculate([1, 2], B, "add")


if __name__ == "__main__":
    unittest.main(verbosity=2)
