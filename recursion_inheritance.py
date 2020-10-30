# Author: Mark Mendez
# Date: 10/26/2020
# Description: Defines classes for generating heightmaps, contrived around use of recursion, 2D list algorithms, and
#              inheritance


from random import randrange


class PointsObject:
    """defines an object that gives points when touched"""
    def __init__(self, points=2):
        """initializes the number of points this object gives"""
        self.points = points


class Tile(PointsObject):
    """defines a tile used for 2D tilemaps"""
    def __init__(self, style='*'):
        """initializes tile type and points"""
        super().__init__(points=1)
        self._style = style

    def get_style(self):
        """returns tile style character"""
        return self._style


class HeightMap:
    """defines a randomly generated heightmap shape"""
    def __init__(self, length, ceiling=None, terrain_type='gentle_hills', tile_styles=None):
        """
        generates and initializes the HeightMap's list of heights and a 2D representation
        :param length: length of height list to generate. First column is set to the axis value of 0 and last column
                       is set to a wall
        :param ceiling: max height of sky and height of walls
        :param terrain_type: type of terrain to simulate. Default is gentle hills
        """
        if tile_styles is None:
            tile_styles = {'ground': '*', 'sky': ' '}

        self._GROUND_TILE = Tile(tile_styles['ground'])
        self._SKY_TILE = Tile(tile_styles['sky'])
        self._WALL_VARIANCE = 1  # how much higher walls are than the apex. If ceiling is provided, walls == ceiling

        # if ceiling provided by caller, use that. Else, use the generated apex + 1 as the ceiling
        if ceiling is not None:
            self._ceiling_provided = True
            self._CEILING = ceiling
        else:
            self._ceiling_provided = False

        # generate list of height values
        starting_height = 0  # height of first column
        self._height_values = self.generate_heightmap(length, terrain_type, starting_height)

        # after generating height values, make another list guaranteed to have only non-negative values
        self._non_negative_heights = self._height_values.copy()
        for height in self._height_values:
            if height < 0:
                # shift to nonzero values by adding lowest value to all (guaranteed to be <= 0)
                nadir = self.get_lowest_point(self._height_values)
                self._non_negative_heights = [value - nadir for value in self._height_values]
                break  # for efficiency

        # after generating non-negative height values, add a wall to show the boundary
        if self._ceiling_provided:  # use provided ceiling height as wall height
            self._WALL = self._CEILING
            self._non_negative_heights.append(self._WALL)
            self._height_values.append(self._WALL)
        else:  # use apex + wall variance as wall height
            self._CEILING = self._WALL = self.get_highest_point(self._non_negative_heights) + self._WALL_VARIANCE
            self._non_negative_heights.append(self._WALL)
            self._height_values.append(self._WALL)

        # after generating height values, make a 2D version
        self._heightmap_2D = self.make_2D_copy_above_ground()  # depends on self._non_negative_heights

    def get_height_values(self):
        """returns height values"""
        return self._height_values

    def get_non_negative_heights(self):
        """returns list of height values, with 0 as a minimum value"""
        return self._non_negative_heights

    def get_highest_point(self, heights=None, ignore_wall=False):
        """
        returns highest point (apex) in heightmap
        :param heights: list of height values. If not provided, method will use the generated height values
        :param ignore_wall: whether to exclude the wall value. Default is False
        :return maximum: highest point (apex) in heights
        """
        # if heights is not provided, assume caller wants the highest point of the generated height values
        if heights is None:
            heights = self.get_height_values()

        # default comparisons to first height
        maximum = heights[0]

        for height in heights:
            if height > maximum and not (ignore_wall and height == self._WALL):
                maximum = height

        return maximum

    def get_lowest_point(self, heights=None, ignore_wall=False):
        """
        returns lowest point (nadir) in heightmap
        :param heights: list of height values. If not provided, method will use the generated height values
        :param ignore_wall: whether to exclude the wall value. Default is False
        :return minimum: lowest point (nadir) in heights
        """
        # if heights is not provided, assume caller wants the lowest point of the generated height values
        if heights is None:
            heights = self.get_height_values()

        # default comparison to first height
        minimum = heights[0]

        for height in heights:
            if height < minimum and not (ignore_wall and height == self._WALL):
                minimum = height

        return minimum

    def make_2D_copy_above_ground(self):
        """
        converts to 2D array by padding with a "blank-space" character
        :return : a 2D version of the heightmap
        """
        # prepare variables used in loop
        ceiling = self._CEILING
        ground_tile = self._GROUND_TILE.get_style()
        sky_tile = self._SKY_TILE.get_style()
        heightmap_2D = []  # return value

        for height in self.get_non_negative_heights():  # iterates horizontally
            # prepare vertical list to append
            column = []

            # assign terrain blocks
            for block in range(0, height):
                column.append(ground_tile)  # adds vertically

            # assign air blocks
            for padding_block in range(height, ceiling):
                column.append(sky_tile)  # adds vertically

            # append new column to heightmap
            heightmap_2D.append(column)

        return heightmap_2D

    def print(self):
        """prints 2D heightmap list to terminal in ASCII-art style"""
        # guaranteed to be same length, so just grab the first one
        ceiling = self._CEILING

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

        # add the new column
        heightmap.append(column_height)

        # enforce given ceiling, if applicable
        if self._ceiling_provided:
            # make sure column is not higher than given ceiling
            if column_height >= self._CEILING:
                # reduce column_height by its excess, and leave a gap
                excess = column_height - self._CEILING
                column_height -= (excess + 1)

            # for wider ranges, enforce range is not more than ceiling, since nadir will be added to highest value
            heights_range = max(heightmap) + abs(min(heightmap))
            if heights_range >= self._CEILING:
                # reduce range by column_height's excess (positive or negative), and leave a gap
                excess = heights_range - self._CEILING
                if column_height >= 0:
                    heightmap[-1] -= (excess + 1)
                else:
                    heightmap[-1] += (excess + 1)

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

if __name__ == '__main__':
    # test
    heightmap = HeightMap(10, terrain_type='gentle_hills', tile_styles={'ground': '*', 'sky': '-'})
    heightmap.print()
