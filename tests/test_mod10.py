import unittest
from script import mod10

class TestBlockChainMethods(unittest.TestCase):
    
    def setUp(self):
        # Test ascii array
        self.ascii_array = [3, 4, 9, 6, 6, 2, 8, 8, 1, 6, 3, 7, 5, 4, 1, 2, 5, 5, 6, 0, 1, 2, 0, 8, 6, 4, 
        1, 6, 0, 8, 5, 3, 6, 0, 2, 5, 6, 7, 4, 1, 9, 5, 0, 9, 0, 9, 7, 7, 6, 9, 0, 8, 6, 6, 2, 0, 3, 6, 1, 
        5, 4, 8, 3, 5, 3, 5, 4, 2, 4, 5, 2, 8, 3, 3, 7, 1, 1, 5, 3, 3, 8, 0, 8, 1, 4, 2, 7, 2, 3, 6, 6, 1, 
        5, 5, 3, 2, 8, 2, 2, 5]
    
    def test_mod10_hash(self):
        """
        Test the mod10 hashing method 
        """
        self.assertEqual(100, len(self.ascii_array))
        
        print("Given ascii array")
        print(self.ascii_array)
        print("-----------------------")

        mod_10_calculation = mod10(self.ascii_array[0:10], self.ascii_array[10:20])

        print("Result of mod_10_hash:")
        print(mod_10_calculation)
        
        self.assertEqual(['6', '1', '4', '0', '7', '4', '3', '3', '7', '6'], mod_10_calculation)

if __name__ == '__main__':
    unittest.main()