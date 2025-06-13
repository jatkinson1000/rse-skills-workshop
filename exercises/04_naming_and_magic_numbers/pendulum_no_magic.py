"""Module implementing pendulum equations."""

import numpy as np

# Set the value of gravity as a module constant
GRAV = 9.81

def get_period(length):
    """
    Calculate the period of a pendulum.

    Parameters
    ----------
    length : float
        length of the pendulum [m]

    Returns
    -------
    float
        period [s] for a swing of the pendulum
    """
    return 2.0 * np.pi * np.sqrt(length / GRAV)


def max_height(length, theta):
    """
    Calculate the maximum height reached by a pendulum.

    Parameters
    ----------
    length : float
        length of the pendulum [m]
    theta : float
        maximum angle of displacment of the pendulum [radians]

    Returns
    -------
    float
        maximum vertical height [m] of the pendulum
    """
    return length * np.cos(theta)


def max_speed(length, theta):
    """
    Calculate the maximum speed of a pendulum.

    Parameters
    ----------
    length : float
        length of the pendulum [m]
    theta : float
        maximum angle of displacment of the pendulum [radians]

    Returns
    -------
    float
        maximum speed [m/s] of the pendulum
    """
    return np.sqrt(2.0 * GRAV * max_height(length, theta))


def energy(mass, length, theta):
    """
    Calculate the energy of a pendulum.

    Parameters
    ----------
    mass : float
        mass of the pendulum bob [kg]
    length : float
        length of the pendulum [m]
    theta : float
        maximum angle of displacment of the pendulum [radians]

    Returns
    -------
    float
        energy [kg . m2 /s2] of the pendulum
    """
    return mass * GRAV * max_height(length, theta)


def check_small_angle(theta, small_ang=np.pi/1800.0):
    """
    Check small angle approximation is valid.

    Parameters
    ----------
    theta : float
        maximum angle of displacment of the pendulum [radians]
    small_ang : float
        maximum value for which the small-angle approximation holds
        defaults to np.pi/1800.0 radians (0.1 degrees)

    Returns
    -------
    bool
        is the small angle approximation valid for the input theta?
    """
    if theta <= np.pi / small_ang:
        return True
    return False


def bpm(length):
    """
    Calculate pendulum frequency in beats per minute.

    Parameters
    ----------
    length : float
        length of the pendulum [m]

    Returns
    -------
    float
        pendulum frequency in beats per minute [1 / min]
    """
    # Divide 60 seconds by period [s] for beats per minute
    return 60.0 / get_period(length)
