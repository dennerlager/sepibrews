import unittest

class Recipe():
    def __init__(self):
        self.steps = []

    def appendStep(self, step):
        self.steps.append(step)

    def __iter__(self):
        return self.steps.__iter__()

class RecipeTest(unittest.TestCase):
    def setUp(self):
        self.recipe = Recipe()
        for i in range(4):
            self.recipe.appendStep(i)

    def test_iteratorProtocol(self):
        targets = [i for i in range(4)]
        for step, target in zip(self.recipe, targets):
            self.assertEqual(step, target)

if __name__ == '__main__':
    unittest.main()
