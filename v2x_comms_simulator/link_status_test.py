import datetime
import unittest
from typing import List

from .device import CohdaMK5
from .distance import Location
from .link_status import get_link_status, get_all_link_statuses
from .path_loss import V2XFreeSpacePathLoss

_PATH_LOSS = V2XFreeSpacePathLoss()

_DEVICE_1 = CohdaMK5(name="cohda-mk5-01", tx_power=23, antenna_gain=5)
_DEVICE_1.location = Location(0, 0)

_DEVICE_2 = CohdaMK5(name="cohda-mk5-02", tx_power=23, antenna_gain=5,)
_DEVICE_2.location = Location(0, 500)

_DEVICE_3 = CohdaMK5(name="cohda-mk5-03", tx_power=10, antenna_gain=5,)
_DEVICE_3.location = Location(0, 3000)

_DEVICES: List[CohdaMK5] = []
for i in range(0, 10):
    device = CohdaMK5(name="cohda-mk5-{}".format(i), tx_power=23, antenna_gain=5,)

    coordinate = (1 + i) * 750.0

    device.location = Location(coordinate, coordinate, coordinate)

    _DEVICES += [device]


class LinkStatusTest(unittest.TestCase):
    maxDiff = 65536

    def test_get_link_status(self):
        link_status = get_link_status(_PATH_LOSS, _DEVICE_1, _DEVICE_2)
        self.assertEqual(True, link_status.device_a_can_rx_device_b)
        self.assertEqual(True, link_status.device_b_can_rx_device_a)
        self.assertEqual(True, link_status.bidirectional_link)

        link_status = get_link_status(_PATH_LOSS, _DEVICE_1, _DEVICE_3)
        self.assertEqual(False, link_status.device_a_can_rx_device_b)
        self.assertEqual(True, link_status.device_b_can_rx_device_a)
        self.assertEqual(False, link_status.bidirectional_link)

    def test_get_all_link_statuses(self):
        link_status_by_devices = get_all_link_statuses(_PATH_LOSS, _DEVICES)

        self.assertEqual(90, len(link_status_by_devices))

        for (device_a, device_b), link_status in link_status_by_devices.items():
            if link_status.device_a_rx_signal_strength < device_a.rx_sensitivity:
                self.assertFalse(link_status.device_a_can_rx_device_b)

            if link_status.device_b_rx_signal_strength < device_b.rx_sensitivity:
                self.assertFalse(link_status.device_b_can_rx_device_a)

            if (
                link_status.device_a_can_rx_device_b
                and link_status.device_b_can_rx_device_a
            ):
                self.assertTrue(link_status.bidirectional_link)

    def test_performance(self):
        before = datetime.datetime.now()
        for _ in range(0, 60 * 10):  # 60 seconds of calculations at 10 Hz
            _ = get_all_link_statuses(_PATH_LOSS, _DEVICES)
        after = datetime.datetime.now()

        print(after - before)

        self.assertLess(
            after - before,
            datetime.timedelta(
                seconds=60.0 / 10
            ),  # in theory, less than 10% CPU to achieve this
        )
