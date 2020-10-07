import datetime
import unittest

from .path_loss import V2XFreeSpacePathLoss

_TX_POWER = 23
_TX_GAIN = 5
_RX_GAIN = 5
_DISTANCE_NEAR = 500
_DISTANCE_FAR = 5000


class V2XFreeSpacePathLossTest(unittest.TestCase):
    def setUp(self):
        self.v2x_free_space_path_loss = V2XFreeSpacePathLoss()

    def test_math(self):
        rx_signal_strength = self.v2x_free_space_path_loss.get_rx_signal_strength(
            _TX_POWER, _TX_GAIN, _RX_GAIN, _DISTANCE_NEAR
        )

        self.assertAlmostEqual(
            -68.82801848945942, rx_signal_strength,
        )

        rx_signal_strength = self.v2x_free_space_path_loss.get_rx_signal_strength(
            _TX_POWER, _TX_GAIN, _RX_GAIN, _DISTANCE_FAR
        )

        self.assertAlmostEqual(
            -88.82801848945942, rx_signal_strength,
        )

    def test_performance(self):
        before = datetime.datetime.now()
        for i in range(0, 10 * 60 * 100):  # 10 Hz for 60 seconds for 100 vehicles
            _ = self.v2x_free_space_path_loss.get_rx_signal_strength(
                _TX_POWER, _TX_GAIN, _RX_GAIN, _DISTANCE_NEAR
            )
        after = datetime.datetime.now()

        self.assertLess(
            after - before,
            datetime.timedelta(
                seconds=60.0 / 10
            ),  # in theory, less than 10% CPU to achieve this
        )
