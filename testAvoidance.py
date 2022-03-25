import unittest
import Avoidance

vectorsToTest = [
    [[100, 0, 500], [50, 0, 0]],
    [[100, 0, 500], [50, 0, 400]]
]

expectedOutcomes = [
    ['left', 150.0],
    ['right', 450.0]
]

class testAvoidance(unittest.TestCase):
    def testVectors(self):
        for currentSet in range(len(vectorsToTest)):
            choice, distance = Avoidance.DodgeWrench(vectorsToTest[currentSet][0], vectorsToTest[currentSet][1], 200.0)
            self.assertEqual(choice, expectedOutcomes[currentSet][0], msg = f"Choice from set {currentSet + 1} does not match.")
            self.assertAlmostEqual(distance, expectedOutcomes[currentSet][1], msg = f"Distance from set {currentSet + 1} does not match.")


if __name__ == '__main__':
    if len(vectorsToTest) == len(expectedOutcomes):
        unittest.main()
    else:
        print("There are not the same number of vectorsToTest and expectedOutcomes.")