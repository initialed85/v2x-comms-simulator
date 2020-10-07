from threading import RLock
from typing import Optional

from .distance import Location


class V2XDevice(object):
    def __init__(
        self, name: str, tx_power: float, antenna_gain: float, rx_sensitivity: float
    ):
        self._name: str = name
        self._tx_power: float = tx_power
        self._antenna_gain: float = antenna_gain
        self._rx_sensitivity: float = rx_sensitivity

        self._location_lock: RLock = RLock()
        self._location: Optional[Location] = None

    def __repr__(self):
        return "{}(name={}, tx_power={}, antenna_gain={}, rx_sensitivity={})".format(
            self.__class__.__name__,
            repr(self._name),
            repr(self._tx_power),
            repr(self._antenna_gain),
            repr(self._rx_sensitivity),
        )

    @property
    def name(self):
        return self._name

    @property
    def tx_power(self) -> float:
        return self._tx_power

    @property
    def antenna_gain(self) -> float:
        return self._antenna_gain

    @property
    def rx_sensitivity(self) -> float:
        return self._rx_sensitivity

    @property
    def location(self) -> Location:
        with self._location_lock:
            if self._location is None:
                raise ValueError("location not set")

            return self._location

    @location.setter
    def location(self, location: Location):
        with self._location_lock:
            self._location = location


_COHDA_MK5_RX_SENSITIVITY = -95


class CohdaMK5(V2XDevice):
    def __init__(
        self,
        name: str,
        tx_power: float,
        antenna_gain: float,
        rx_sensitivity: float = _COHDA_MK5_RX_SENSITIVITY,
    ):
        super().__init__(
            name=name,
            rx_sensitivity=rx_sensitivity,
            tx_power=tx_power,
            antenna_gain=antenna_gain,
        )
