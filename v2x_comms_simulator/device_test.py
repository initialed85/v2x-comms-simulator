import unittest

from .device import CohdaMK5
from .distance import Location

_LOCATION = Location(x=100, y=200)


class CohdaMK5Test(unittest.TestCase):
    def setUp(self):
        self._v2x_device: CohdaMK5 = CohdaMK5(
            name="cohda-mk5-01", tx_power=23, antenna_gain=5
        )

    def test_getters(self):
        self.assertEqual(23, self._v2x_device.tx_power)

        self.assertEqual(5, self._v2x_device.antenna_gain)

        self.assertEqual(-95, self._v2x_device.rx_sensitivity)

    def test_location_setter_and_getter(self):
        with self.assertRaises(ValueError):
            _ = self._v2x_device.location

        self._v2x_device.location = _LOCATION

        self.assertEqual(_LOCATION, self._v2x_device.location)
