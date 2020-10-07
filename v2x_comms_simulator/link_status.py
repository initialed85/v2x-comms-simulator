from typing import NamedTuple, List, Dict, Tuple

from .device import V2XDevice
from .distance import get_distance_between_locations
from .path_loss import V2XFreeSpacePathLoss


class LinkStatus(NamedTuple):
    distance: float
    device_a_rx_signal_strength: float
    device_a_can_rx_device_b: bool
    device_b_rx_signal_strength: float
    device_b_can_rx_device_a: bool
    bidirectional_link: bool


def get_link_status(
    path_loss: V2XFreeSpacePathLoss, device_a: V2XDevice, device_b: V2XDevice
) -> LinkStatus:
    distance = get_distance_between_locations(device_a.location, device_b.location)
    if distance <= 0.1:
        distance = 0.1

    device_a_rx_signal_strength = path_loss.get_rx_signal_strength(
        tx_power=device_b.tx_power,
        tx_gain=device_b.antenna_gain,
        rx_gain=device_a.antenna_gain,
        distance=distance,
    )

    device_a_can_rx_device_b = device_a_rx_signal_strength > device_a.rx_sensitivity

    device_b_rx_signal_strength = path_loss.get_rx_signal_strength(
        tx_power=device_a.tx_power,
        tx_gain=device_a.antenna_gain,
        rx_gain=device_b.antenna_gain,
        distance=distance,
    )

    device_b_can_rx_device_a = device_b_rx_signal_strength > device_b.rx_sensitivity

    return LinkStatus(
        distance=distance,
        device_a_rx_signal_strength=device_a_rx_signal_strength,
        device_a_can_rx_device_b=device_a_can_rx_device_b,
        device_b_rx_signal_strength=device_b_rx_signal_strength,
        device_b_can_rx_device_a=device_b_can_rx_device_a,
        bidirectional_link=device_a_can_rx_device_b and device_b_can_rx_device_a,
    )


def _reverse_link_status(link_status) -> LinkStatus:
    return LinkStatus(
        distance=link_status.distance,
        device_a_rx_signal_strength=link_status.device_b_rx_signal_strength,
        device_a_can_rx_device_b=link_status.device_b_can_rx_device_a,
        device_b_rx_signal_strength=link_status.device_a_rx_signal_strength,
        device_b_can_rx_device_a=link_status.device_a_can_rx_device_b,
        bidirectional_link=link_status.bidirectional_link,
    )


def get_all_link_statuses(
    path_loss: V2XFreeSpacePathLoss, devices: List[V2XDevice]
) -> Dict[Tuple[V2XDevice, V2XDevice], LinkStatus]:
    link_status_by_devices: Dict[Tuple[V2XDevice, V2XDevice], LinkStatus] = {}
    for device_a in devices:
        for device_b in devices:
            if device_a == device_b:
                continue

            link_status = get_link_status(path_loss, device_a, device_b)
            link_status_by_devices[(device_a, device_b)] = link_status
            link_status_by_devices[(device_b, device_a)] = _reverse_link_status(
                link_status
            )

    return link_status_by_devices
