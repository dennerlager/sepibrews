#!/usr/bin/env python
from __future__ import print_function, division
import unittest
import csv
import dsv
from recipe import Recipe
from step import Step

class RecipeBuilder():
    def parse(self, filename):
        recipe = Recipe()
        with open (filename, 'r') as filehandle:
            self.throwAwayHeaderLine(filehandle)
            reader = csv.reader(filehandle, dialect=dsv.DsvDialect)
            for line in reader:
                recipe.appendStep(self.parseline(line))
        return recipe

    def throwAwayHeaderLine(self, filehandle):
        filehandle.readline()

    def parseline(self, line):
        return Step(float(line[0]), float(line[1])*60)

class RecipeBuilderTest(unittest.TestCase):
    def setUp(self):
        self.rb = RecipeBuilder()
        self.recipe = self.rb.parse('./recipes/test.csv')

    def test_parseReturnsRecipe(self):
        self.assertIsInstance(self.recipe, Recipe)

    def test_parseFirstStepTemperature(self):
        self.assertEqual(self.recipe.steps[0].temperatureC, 30)

    def test_parseFirstStepDurationSec(self):
        self.assertEqual(self.recipe.steps[0].durationSec, 6)

    def test_parseLastStepTemperature(self):
        self.assertEqual(self.recipe.steps[-1].temperatureC, 40)

    def test_parseLastStepDurationSec(self):
        self.assertEqual(self.recipe.steps[-1].durationSec, 12)

if __name__ == '__main__':
    unittest.main()
