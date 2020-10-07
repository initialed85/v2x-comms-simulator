from v2x_comms_simulator.device import CohdaMK5
from v2x_comms_simulator.distance import Location
from v2x_comms_simulator.link_status import get_all_link_statuses
from v2x_comms_simulator.path_loss import V2XFreeSpacePathLoss


def print_link_statuses(path_loss, devices):
    all_link_statuses = get_all_link_statuses(path_loss=path_loss, devices=devices)

    for (device_a, device_b), link_status in all_link_statuses.items():
        print(
            "{} receives {} at {}dBm from {}m away; link is {}".format(
                device_a.name,
                device_b.name,
                round(link_status.device_a_rx_signal_strength, 2),
                link_status.distance,
                "established" if link_status.bidirectional_link else "not established",
            )
        )


if __name__ == "__main__":
    path_loss = V2XFreeSpacePathLoss()

    # create some devices
    device_1 = CohdaMK5(name="device-1", tx_power=10, antenna_gain=3)
    device_2 = CohdaMK5(name="device-2", tx_power=10, antenna_gain=3)
    device_3 = CohdaMK5(name="device-3", tx_power=10, antenna_gain=3)

    # put them in a straight line, 100m apart
    device_1.location = Location(x=0, y=0, z=0)
    device_2.location = Location(x=100, y=0, z=0)
    device_3.location = Location(x=200, y=0, z=0)

    print("before moving")
    print_link_statuses(path_loss=path_loss, devices=[device_1, device_2, device_3])

    # now move the centre device away in a straight line
    for i in range(0, 2000, 20):
        device_2.location = Location(x=i, y=device_2.location.y, z=device_2.location.z)

        print("")
        print("{} moved to {}".format(device_2.name, device_2.location))
        print_link_statuses(path_loss=path_loss, devices=[device_1, device_2, device_3])
