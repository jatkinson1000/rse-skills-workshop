"""Module implementing pendulum equations."""

import numpy as np


def get_period(l):
    """
    Calculate the period of a pendulum.

    Parameters
    ----------
    l : float
        length of the pendulum [m]

    Returns
    -------
    float
        period [s] for a swing of the pendulum
    """
    return 2.0 * np.pi * np.sqrt(l / 9.81)


def max_height(l, theta):
    """
    Calculate the maximum height reached by a pendulum.

    Parameters
    ----------
    l : float
        length of the pendulum [m]
    theta : float
        maximum angle of displacment of the pendulum [radians]

    Returns
    -------
    float
        maximum vertical height [m] of the pendulum
    """
    return l * np.cos(theta)


def max_speed(l, theta):
    """
    Calculate the maximum speed of a pendulum.

    Parameters
    ----------
    l : float
        length of the pendulum [m]
    theta : float
        maximum angle of displacment of the pendulum [radians]

    Returns
    -------
    float
        maximum speed [m/s] of the pendulum
    """
    return np.sqrt(2.0 * 9.81 * max_height(l, theta))


def energy(m, l, theta):
    """
    Calculate the energy of a pendulum.

    Parameters
    ----------
    m : float
        mass of the pendulum bob [kg]
    l : float
        length of the pendulum [m]
    theta : float
        maximum angle of displacment of the pendulum [radians]

    Returns
    -------
    float
        energy [kg . m2 /s2] of the pendulum
    """
    return m * 9.81 * max_height(l, theta)


def check_small_angle(theta):
    """
    Check small angle approximation is valid.

    Parameters
    ----------
    theta : float
        maximum angle of displacment of the pendulum [radians]

    Returns
    -------
    bool
        is the small angle approximation valid for the input theta?
    """
    if theta <= np.pi / 1800.0:
        return True
    return False


def bpm(l):
    """
    Calculate pendulum frequency in beats per minute.

    Parameters
    ----------
    l : float
        length of the pendulum [m]

    Returns
    -------
    float
        pendulum frequency in beats per minute [1 / min]
    """
    return 60.0 / get_period(l)
