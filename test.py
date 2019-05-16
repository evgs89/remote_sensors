import unittest
from tests.test_listener import test_Listener


if __name__ == "__main__":
    loader = unittest.TestLoader()
    test_cases = [test_Listener, ]
    tests = [loader.loadTestsFromTestCase(i) for i in test_cases]
    suite = unittest.TestSuite(tests)
    unittest.TestRunner().run(suite)

