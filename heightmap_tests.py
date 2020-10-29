# Author: Mark Mendez
# Date: 10/29/2020
# Description: Contains sample unit tests for HeightMap class


import unittest
from recursion_inheritance import *


class HeightMapTests(unittest.TestCase):
    """defines a sample of unit tests for HeightMap class"""
    def test_ceiling_when_provided(self):
        """heightmap correctly uses its given ceiling"""
        ceiling = 5
        heightmap = HeightMap(10, ceiling=ceiling, terrain_type='mountains')
        self.assertEqual(heightmap._CEILING, ceiling)

    def test_ceiling_when_not_provided(self):
        """heightmap correctly uses apex + 1 as its ceiling"""
        heightmap = HeightMap(10, terrain_type='mountains')
        apex = heightmap.get_highest_point(heightmap.get_non_negative_heights())
        self.assertEqual(heightmap._CEILING, apex + heightmap._WALL_VARIANCE)

    def test_get_highest_point_is_apex(self):
        """heightmap correctly returns its apex"""
        heightmap = HeightMap(length=10, ceiling=5, terrain_type='mountains')
        apex = heightmap.get_highest_point()
        expected_apex = max(heightmap.get_height_values())
        self.assertEqual(apex, expected_apex)

    def test_get_lowest_point_is_nadir(self):
        """heightmap correctly returns its nadir"""
        heightmap = HeightMap(length=10, ceiling=5, terrain_type='mountains')
        apex = heightmap.get_lowest_point()
        expected_apex = min(heightmap.get_height_values())
        self.assertEqual(apex, expected_apex)


if __name__ == '__main__':
    unittest.main()
