#!/usr/bin/env python
from __future__ import print_function, division
import unittest
from recipe_builder import RecipeBuilder

class TotalRemainingTimeEstimator():
    """There are two different states to consider:
    - the controller is still heating up to the next target temperature
    - the target temperature is reached and hold time is ticking """
    def __init__(self, recipe, temperatureChangeRateCperSec):
        self.recipe = recipe
        self.temperatureChangeRateCperSec = temperatureChangeRateCperSec

    def estimateRemainingSeconds(self,
                                 currentStep,
                                 currentTemp,
                                 elapsedStepTime,
                                 isStepTempReached):
        timeLeft = 0
        for index, step in enumerate(self.recipe):
            if index < currentStep:
                continue
            if not isStepTempReached:
                timeLeft += self.getHeatTime(currentTemp, step.temperatureC)
                timeLeft += step.durationSec
            else:
                timeLeft += step.durationSec - elapsedStepTime
            currentTemp = step.temperatureC
            isStepTempReached = False
        return timeLeft

    def getHeatTime(self, fromTempC, toTempC):
        deltaT = toTempC - fromTempC
        return deltaT / self.temperatureChangeRateCperSec

class TotalRemainingTimeEstimatorTest(unittest.TestCase):
    def setUp(self):
        self.e = TotalRemainingTimeEstimator(RecipeBuilder().parse('./recipes/test.csv'), 1)

    def test_estimateRemainingSeconds(self):
        self.assertEqual(self.e.estimateRemainingSeconds(currentStep=0,
                                                         currentTemp=25,
                                                         elapsedStepTime=0,
                                                         isStepTempReached=False), 33)

    def test_estimateRemainingSecondsTempReached(self):
        self.assertEqual(self.e.estimateRemainingSeconds(currentStep=0,
                                                         currentTemp=25,
                                                         elapsedStepTime=1,
                                                         isStepTempReached=True), 27)

    def test_estimateRemainingSecondsStep1(self):
        self.assertEqual(self.e.estimateRemainingSeconds(currentStep=1,
                                                         currentTemp=30,
                                                         elapsedStepTime=0,
                                                         isStepTempReached=False), 22)

    def test_estimateRemainingSecondsTempReachedStep1(self):
        self.assertEqual(self.e.estimateRemainingSeconds(currentStep=1,
                                                         currentTemp=40,
                                                         elapsedStepTime=1,
                                                         isStepTempReached=True), 11)

    def test_getHeatTime(self):
        self.assertEqual(self.e.getHeatTime(25, 30), 5)

if __name__ == '__main__':
    unittest.main()
