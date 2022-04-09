import unittest
import Avoidance

vectorsToTest = [
    # Level with camera in y-axis
    [[0, 0, 500], [0, 0, 0]],       # straight on
    [[0, 0, 101], [0, 0, 0]],       # straight on
    [[150, 0, 500], [50, 0, 0]],    # from right to right of sled
    [[-150, 0, 500], [-50, 0, 0]],  # from left to left of sled
    [[150, 0, 500], [-50, 0, 0]],   # from right to left of sled
    [[-150, 0, 500], [50, 0, 0]],   # from left to right of sled
    [[0, 0, 10000], [40, 0, 0]],    # from center to right of sled
    [[0, 0, 10000], [-40, 0, 0]],   # from center to left of sled
    [[400, 0, 1000], [250, 0, 0]],  # always right of camera and outside tolerance
    [[200, 0, 200], [201, 0, 0]],   # always right of camera and outside tolerance
    [[-200, 0, 101], [-210, 0, 0]], # always left of camera and outside tolerance
    [[-200, 0, 101], [-210, 0, 0]], # always left of camera and outside tolerance

    # Above camera coming downwards in y-axis
    [[0, 500, 500], [0, 50, 0]],        # straight
    [[0, 500, 50], [0, 50, 0]],         # straight
    [[150, 350, 500], [50, 50, 0]],     # from right to right of sled
    [[-150, 100, 500], [-50, 10, 0]],   # from left to left of sled
    [[150, 1000, 500], [-50, 250, 0]],  # from right to left of sled
    [[-150, 10, 500], [50, 0, 0]],      # from left to right of sled
    [[0, 1000, 10000], [80, 500, 0]],   # from center to right of sled
    [[0, 750, 10000], [-80, 200, 0]],   # from center to left of sled
    [[400, 400, 1000], [300, 375, 0]],  # always right of camera and outside tolerance
    [[200, 375, 200], [201, 350, 0]],   # always right of camera and outside tolerance
    [[-200, 375, 101], [-215, 350, 0]], # always left of camera and outside tolerance
    [[-200, 375, 105], [-215, 350, 0]], # always left of camera and outside tolerance

    # Below camera moving upwards in y-axis
    [[0, -500, 500], [0, -50, 0]],          # straight
    [[0, -500, 10], [0, -50, 0]],           # straight
    [[250, -350, 500], [75, -50, 0]],       # from right to right of sled
    [[-150, -100, 500], [-10, 0, 0]],       # from left to left of sled
    [[150, -1000, 500], [-175, -250, 0]],   # from right to left of sled
    [[-150, -10, 500], [25, 0, 0]],         # from left to right of sled
    [[0, -1000, 5000], [199, -250, 0]],     # from center to right of sled
    [[0, -1000, 5000], [-199, -500, 0]],    # from center to left of sled
    [[400, 200, 1000], [225, 175, 0]],      # always right of camera and outside tolerance
    [[200, 350, 200], [201, 125, 0]],       # always right of camera and outside tolerance
    [[-200, 350, 101], [-205, 125, 0]],     # always left of camera and outside tolerance
    [[-200, 350, 101], [-205, 125, 0]]      # always left of camera and outside tolerance
]

expectedOutcomes = [
    ['Move Either Way', 200.0],
    ['Move Either Way', 200.0],
    ['left', 150.0],
    ['right', 150.0],
    ['right', 150.0],
    ['left', 150.0],
    ['left', 160.0],
    ['right', 160.0],
    ['Stay', -50.0],
    ['Stay', -1.0],
    ['Stay', -10.0],
    ['Stay', -10.0],

    ['Move Either Way', 200.0],
    ['Move Either Way', 200.0],
    ['left', 150.0],
    ['right', 150.0],
    ['right', 150.0],
    ['left', 150.0],
    ['left', 120.0],
    ['right', 120.0],
    ['Stay', -100.0],
    ['Stay', -1.0],
    ['Stay', -15.0],
    ['Stay', -15.0],

    ['Move Either Way', 200.0],
    ['Move Either Way', 200.0],
    ['left', 125.0],
    ['right', 190.0],
    ['right', 25.0],
    ['left', 175.0],
    ['left', 1.0],
    ['right', 1.0],
    ['Stay', -25.0],
    ['Stay', -1.0],
    ['Stay', -5.0],
    ['Stay', -5.0]
]

sep = '\n-------------------------------------------------\n'
new_line = '\n'
tab = '\t'

class testAvoidance(unittest.TestCase):
    def testVectors(self):
        print("\nTesting output from 'Avoidance.py' using different input vectors...")
        for currentSet in range(len(vectorsToTest)):
            choice, distance = Avoidance.DodgeWrench(vectorsToTest[currentSet][0], vectorsToTest[currentSet][1], 200.0)
            self.assertEqual(choice, expectedOutcomes[currentSet][0], msg = f"{sep}'Choice' from set {currentSet + 1} does not match.\
                {new_line}CALCULATED: {choice}{tab}EXPECTED: {expectedOutcomes[currentSet][0]}{sep}")
            self.assertAlmostEqual(distance, expectedOutcomes[currentSet][1], msg = f"{sep}'moveDistance' from set {currentSet + 1} does not match.\
                {new_line}CALCULATED: {distance}{tab}EXPECTED: {expectedOutcomes[currentSet][1]}{sep}")
        print(f"Testing done.\nTotal test vectors applied: {len(vectorsToTest)}")


if __name__ == '__main__':
    if len(vectorsToTest) == len(expectedOutcomes):
        unittest.main()
    else:
        print("There are not the same number of vectorsToTest and expectedOutcomes.")