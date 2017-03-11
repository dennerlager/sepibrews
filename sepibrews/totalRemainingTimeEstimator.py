#!/usr/bin/env python
from __future__ import print_function, division
import unittest
from recipe_builder import RecipeBuilder

class TotalRemainingTimeEstimater():
    """There are two different states to consider:
    - the controller is still heating up to the next target temperature
    - the target temperature is reached and hold time is ticking """
    def __init__(self, recipe, temperatureChangeRateCperSec):
        self.recipe = RecipeBuilder().parse(recipe)
        self.temperatureChangeRateCperSec = temperatureChangeRateCperSec

    def estimateRemainingSeconds(self,
                                 currentStep,
                                 currentTemp,
                                 elapsedStepTime, 
                                 isStepTempReached):
        timeLeft = 0
        for index, step in enumerate(self.recipe):
            if not isStepTempReached:
                timeLeft += self.getHeatTime(currentTemp, step.temperatureC)
                timeLeft += step.durationMin * 60
            else:
                timeLeft += step.durationMin * 60 - elapsedStepTime
            currentTemp = step.temperatureC
            isStepTempReached = False
        return timeLeft

    def getHeatTime(self, fromTempC, toTempC):
        deltaT = toTempC - fromTempC
        return deltaT / self.temperatureChangeRateCperSec

class TotalRemainingTimeEstimaterTest(unittest.TestCase):
    def setUp(self):
        self.e = TotalRemainingTimeEstimater('./recipes/test.csv', 1)

    def test_estimateRemainingSeconds(self):
        self.assertEqual(self.e.estimateRemainingSeconds(currentStep=1,
                                                         currentTemp=25,
                                                         elapsedStepTime=0, 
                                                         isStepTempReached=False), 33)

    def test_estimateRemainingSecondsTempReached(self):
        self.assertEqual(self.e.estimateRemainingSeconds(currentStep=1,
                                                         currentTemp=25,
                                                         elapsedStepTime=1, 
                                                         isStepTempReached=True), 27)

    def test_getHeatTime(self):
        self.assertEqual(self.e.getHeatTime(25, 30), 5)

if __name__ == '__main__':
    unittest.main()
