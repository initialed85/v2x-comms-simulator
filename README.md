# v2x-simulator

# status: working last time I touched it a very, very long time ago

This repo contains a Python3 library that can be used as a simple V2X simulator.

The goal is for a given set of devices with known locations, calculate whether or not they'd be able to communicate based on distance and the free-space path-loss formula.

The Cohda MK5 has been used as a reference device (regarding receive sensitivity, frequency, etc).

## Usage

### Prerequisites

-   a Python3 environment

### Steps

-   clone this repo to a folder
-   change to that folder
-   run `pip install .`

At this point, the `v2x_comms_simulator` is now available to your Python3 environment as a site package.

### Example

See `example.py` at the root of this repo.

## Further development

### Prerequisites

-   a Python3 environment

### Steps

-   clone this repo to a folder
-   change to that folder
-   run `pip install .`
-   run `pip install -r requirements-dev.txt`

At this point, you can run the tests as follows:

```
python -m pytest -vv v2x_comms_simulator
```
