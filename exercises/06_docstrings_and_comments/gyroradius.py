"""Module with a single function to calculate gyroradius."""

def calculate_gyroradius(mass, v_perp, charge, B, gamma=None):
    """
    Calculates the gyroradius of a charged particle in a magnetic field

    Parameters
    ----------
    mass : float
        The mass of the particle [kg]
    v_perp : float
        velocity perpendicular to magnetic field [m/s]
    charge : float
        particle charge [coulombs]
    gamma : float, optional
        Lorentz factor for relativistic case. default=None for non-relativistic case.

    Returns
    -------
    r_g : float
        Gyroradius of particle [m]

    Notes
    -----
    .. [1]  Walt, M, "Introduction to Geomagnetically Trapped Radiation,"
       Cambridge Atmospheric and Space Science Series, equation (2.4), 2005.
    """

    r_g = mass * v_perp / (abs(charge) * B)

    if gamma:
        r_g = r_g * gamma

    return r_g

