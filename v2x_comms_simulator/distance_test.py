import datetime
import unittest

from .distance import Location, get_distance_between_locations

_2D_WORK_UTM = Location(391761.18, 6463997.21)
_2D_PUB_UTM = Location(391846.66, 6463966.41)
_2D_DISTANCE_BETWEEN_WORK_AND_PUB = 90.85995320336748

_3D_WORK_UTM = Location(391761.18, 6463997.21, 100)
_3D_PUB_UTM = Location(391846.66, 6463966.41, 150)
_3D_DISTANCE_BETWEEN_WORK_AND_PUB = 103.70858402266103


class DistanceTest(unittest.TestCase):
    def test_math(self):
        self.assertAlmostEqual(
            _2D_DISTANCE_BETWEEN_WORK_AND_PUB,
            get_distance_between_locations(_2D_WORK_UTM, _2D_PUB_UTM),
            places=3,
        )

        self.assertAlmostEqual(
            _3D_DISTANCE_BETWEEN_WORK_AND_PUB,
            get_distance_between_locations(_3D_WORK_UTM, _3D_PUB_UTM),
            places=3,
        )

    def test_performance(self):
        before = datetime.datetime.now()
        for i in range(0, 10 * 60 * 100):  # 10 Hz for 60 seconds for 10 vehicles
            get_distance_between_locations(_2D_WORK_UTM, _2D_PUB_UTM)
        after = datetime.datetime.now()

        self.assertLess(
            after - before,
            datetime.timedelta(
                seconds=60.0 / 10
            ),  # in theory, less than 10% CPU to achieve this
        )

        before = datetime.datetime.now()
        for i in range(0, 10 * 60 * 100):  # 10 Hz for 60 seconds for 10 vehicles
            get_distance_between_locations(_3D_WORK_UTM, _3D_PUB_UTM)
        after = datetime.datetime.now()

        self.assertLess(
            after - before,
            datetime.timedelta(
                seconds=60.0 / 10
            ),  # in theory, less than 10% CPU to achieve this
        )
