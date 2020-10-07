from math import log10

_LOWER_FREQ_MHZ = 5.85 * 1000.0
_UPPER_FREQ_MHZ = 5.925 * 1000.0
_CENTER_FREQ = _UPPER_FREQ_MHZ - ((_UPPER_FREQ_MHZ - _LOWER_FREQ_MHZ) / 2.0)

_MHZ_TO_GHZ = 1.0 / 1000.0
_KM_TO_M = 1.0 / 1000.0
_FSPL_GHZ_AND_KM_CONSTANT = 92.45


class V2XFreeSpacePathLoss(object):
    def __init__(self, center_freq: float = _CENTER_FREQ):
        self._center_freq = center_freq

    def get_rx_signal_strength(self, tx_power, tx_gain, rx_gain, distance) -> float:
        distance = distance * _KM_TO_M
        freq = self._center_freq * _MHZ_TO_GHZ

        return (
            tx_power
            + tx_gain
            + rx_gain
            - (20 * log10(distance) + 20 * log10(freq) + _FSPL_GHZ_AND_KM_CONSTANT)
        )
