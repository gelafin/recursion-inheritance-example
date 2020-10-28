# Author: Mark Mendez
# Date: 10/26/2020
# Description: Defines a HeightMap class for generating heightmaps, contrived to show off impractical code examples
#              which showcase knowledge of practical concepts, such as recursion, 2D list algorithms, and inheritance


from random import randrange


class HeightMap:
    """defines a randomly generated heightmap shape"""
    def __init__(self, length, ceiling=None, terrain_type='gentle_hills'):
        """
        generates and initializes the HeightMap's list of heights and a 2D representation
        :param length: length of height list to generate. First column is set to the axis value of 0 and last column
                       is set to a wall
        :param ceiling: max height of sky and height of walls
        :param terrain_type: type of terrain to simulate. Default is gentle hills
        """
        self._WALL_VARIANCE = 1  # how much higher walls are than the apex

        # if ceiling provided by caller, use that. Else, use the apex as the ceiling
        need_ceiling = False
        if ceiling is not None:
            self._ceiling = self._WALL = ceiling + self._WALL_VARIANCE  # convenient to have different semantic terms
        else:
            need_ceiling = True

        # generate list of height values
        starting_height = 0  # height of first column
        self._height_values = self.generate_heightmap(length, terrain_type, starting_height)

        # after generating height values, make another list guaranteed to have only non-negative values
        self._non_negative_heights = self._height_values
        for height in self._height_values:
            if height < 0:
                # shift to nonzero values by adding lowest value to all. Exclude the wall
                self._non_negative_heights = ([value - self.get_lowest_point()
                                               for value in self._height_values if value != self._WALL])
                # restore the wall
                self._non_negative_heights.append(self._WALL)
                break  # for efficiency

        # after generating non-negative height values, use the apex to find the ceiling if not provided by caller
        if need_ceiling:
            self._ceiling = self._WALL = self.get_highest_point() + self._WALL_VARIANCE  # TODO: circular dependency between need_ceiling _WALL instantiation and _non_negative_heights instantiation

        # after generating height values, make a 2D version
        self._heightmap_2D = self.make_2D_copy_above_ground()  # depends on self._non_negative_heights

    def get_wall_variance(self):
        """:return wall variance: how much higher walls are than the highest point (apex)"""
        return self._WALL_VARIANCE

    def get_height_values(self):
        """returns height values"""
        return self._height_values

    def get_non_negative_heights(self):
        """returns list of height values, with 0 as a minimum value"""
        return self._non_negative_heights

    def get_highest_point(self, heights=None):
        """
        returns highest point (apex) in heightmap
        :param heights: list of height values
        :return maximum: highest point (apex) in heights
        """
        # if heights is not provided, assume caller wants the highest point of the generated height values
        if heights is None:
            heights = self.get_height_values()

        # default comparisons to first height
        maximum = heights[0]

        for height in heights:
            if height > maximum:
                maximum = height

        return maximum

    def get_lowest_point(self):
        """returns lowest point (nadir) in heightmap"""
        # default comparison to first height
        minimum = self.get_height_values()[0]

        for height in self._height_values:
            if height < minimum:
                minimum = height

        return minimum

    def make_2D_copy_above_ground(self):
        """
        converts to 2D array by padding with a "blank-space" character
        :return : a 2D version of the heightmap
        """
        # prepare variables used in loop
        ceiling = self._ceiling
        heightmap_2D = []  # return value

        for height in self.get_non_negative_heights():  # iterates horizontally
            # prepare vertical list to append
            column = []

            # assign terrain blocks
            for block in range(0, height):
                column.append('*')  # adds vertically

            # assign air blocks
            for padding_block in range(height, ceiling):
                column.append(' ')  # adds vertically

            # append new column to heightmap
            heightmap_2D.append(column)

        return heightmap_2D

    def print(self):
        """prints 2D heightmap list to terminal in ASCII-art style"""
        # guaranteed to be same length, so just grab the first one
        ceiling = self._ceiling

        for block in range(ceiling - 1, 0 - 1, -1):  # print in reverse, since sky is stored at end
            printable_row = []

            for column in range(len(self._heightmap_2D)):
                printable_row.append(self._heightmap_2D[column][block])

            print(printable_row)

    def recursive_generate_heightmap(self, length, max_variance, heightmap, previous_height):
        """
        helper function for generate_heightmap()
        :param length: desired number of rows
        :param max_variance: acceptable maximum height variance between rows
        :param heightmap: array of height values
        :param previous_height: used for recursion
        """
        # handy helpers
        INCLUSIVE = 1  # for ranges

        # base case: if length has been reached, we're done
        if len(heightmap) >= length:
            # add a wall to show the boundary
            heightmap.append(self.get_highest_point(heightmap) + self.get_wall_variance())
            return heightmap

        # recursive case
        # pick a random number in acceptable range for the variance
        variance = randrange(0, max_variance + INCLUSIVE)

        # decide whether the new column is higher or lower
        fifty_fifty = randrange(1, 2 + INCLUSIVE)

        # 50% chance to negate value
        if fifty_fifty == 1:
            variance = 0 - variance

        column_height = previous_height + variance

        print('adding height', column_height)

        # add the new column
        heightmap.append(column_height)

        # heightmap array mutated in-place on the way down the recursion rabbit hole
        return self.recursive_generate_heightmap(length, max_variance, heightmap, previous_height=column_height)

    def generate_heightmap(self, length, terrain_type, starting_height):
        """
        generates a new, random heightmap as an array of height values for the HeightMap object
        first column is 0 and last column is equal to the highest plus 1
        :param length: how many columns of terrain to generate
        :param terrain_type: type of terrain to generate, e.g., gentle_hills, mountains, etc.
        :param starting_height: desired height of leftmost column
        """
        # decide variance pattern based on terrain_type
        if terrain_type == 'gentle_hills':
            max_variance = 1
        elif terrain_type == 'mountains':
            max_variance = 3
        else:
            max_variance = 1

        # initialize final return value with a given starting height
        heightmap = [starting_height]

        # account for the extra column we just created
        length -= 1

        return self.recursive_generate_heightmap(length, max_variance, heightmap, previous_height=starting_height)

# test
heightmap = HeightMap(10)
heightmap.print()
