"""Routines for analysing precipitation climatology from ESM runs."""

import json
import numpy as np
import matplotlib.pyplot as plot
import matplotlib.ticker as mticker
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cmocean
import regionmask


def convert_precipitation_units(precipitation_in_kg_per_m_squared_s):
    """
    Convert precipitation units from [kg m-2 s-1] to [mm day-1].

    Parameters
    ----------
    precipitation_in_kg_per_m_squared_s : xarray.DataArray
        xarray DataArray containing model precipitation data

    Returns
    -------
    precipitation_in_mm_per_day : xarray.DataArray
        the input DataArray with precipitation units modified
    """
    # density 1000 kg m-3 => 1 kg m-2 == 1 mm
    # There are 60*60*24 = 86400 seconds per day
    precipitation_in_mm_per_day = xr.DataArray(precipitation_in_kg_per_m_squared_s * 86400)

    precipitation_in_mm_per_day.attrs["units"] = "mm/day"

    if precipitation_in_mm_per_day.data.min() < 0.0:
        raise ValueError("There is at least one negative precipitation value")
    if precipitation_in_mm_per_day.data.max() > 2000:
        raise ValueError("There is a precipitation value/s > 2000 mm/day")

    return precipitation_in_mm_per_day


# I think it would be good to give more detail here about what the dimensions and
# content of the input array needs to be, to save the reader having to go through
# the code and infer it in order to use the method. Would it also be possible to give
# the input variable a more specific name?
def plot_zonally_averaged_precipitation(data):
    """
    Plot zonally-averaged precipitation data and save to file.

    Parameters
    ----------
    data : xarray.DataArray
        xarray DataArray containing model data

    Returns
    -------
    None

    """
    zonal_precipitation = data["precipitation"].mean("longitude", keep_attrs=True)

    figure, axes = plot.subplots(nrows=4, ncols=1, figsize=(12, 8))

    zonal_precipitation.sel(lat=[0]).plot.line(ax=axes[0], hue="latitude")
    zonal_precipitation.sel(lat=[-20, 20]).plot.line(ax=axes[1], hue="latitude")
    zonal_precipitation.sel(lat=[-45, 45]).plot.line(ax=axes[2], hue="latitude")
    zonal_precipitation.sel(lat=[-70, 70]).plot.line(ax=axes[3], hue="latitude")

    plot.tight_layout()
    for axis in axes:
        axis.set_ylim(0.0, 1.0e-4)
        axis.grid()
    plot.savefig("zonal.png", dpi=200)  # Save figure to file

    figure, axes = plot.subplots(nrows=1, ncols=1, figsize=(12, 5))

    zonal_precipitation.T.plot()

    plot.savefig("zonal_map.png", dpi=200)  # Save figure to file

# could data be named more specifically and more detail be given in the docstring about
# what the dimension and contents of the array are?
def get_country_annual_average(data, countries):
    """
    Calculate annual precipitation averages for countries and save to file.

    Parameters
    ----------
    data : xarray.DataArray
        xarray DataArray containing model data
    countries : dict(str: str)
        dictionary mapping country names to regionmask codes. For a list see:
        regionmask.defined_regions.natural_earth_v5_0_0.countries_110.regions

    Returns
    -------
    None

    """
    data_average = data["precipitation"].groupby("time.year").mean("time",
                                                                   keep_attrs=True)
    data_average = convert_precipitation_units(data_average)

    # would it be possible to give land a more specific name?
    land = (regionmask.
            defined_regions.
            natural_earth_v5_0_0
            .countries_110.mask(data_average))

    with open("data.txt", "w", encoding="utf-8") as datafile:
        # could k and v be named more specifically?
        for k, v in countries.items():
            data_avg_mask = data_average.where(land.cf == v)

            for year in data_avg_mask.year.values:
                precipitation = data_avg_mask.sel(year=year).mean().values
                datafile.write(f"{k.ljust(25)} {year} : {precipitation:2.3f} mm/day\n")
            datafile.write("\n")


# could data be named more specifically and more detail be given in the docstring about
# what the dimension and contents of the array are?
def plot_enso_hovmoller_diagram(data):
    """
    Plot Hovmöller diagram of equatorial precipitation to visualise ENSO.

    Parameters
    ----------
    data : xarray.DataArray
        xarray DataArray containing model data

    Returns
    -------
    None

    """
    enso = (
        data["precipitation"]
        .sel(lat=slice(-1, 1))
        .sel(lon=slice(120, 280))
        .mean(dim="latitude", keep_attrs=True)
    )

    enso.plot()
    plot.savefig("enso.png", dpi=200)  # Save figure to file


def create_precipitation_climatology_plot(climatology_data, model_name, season, mask=None, plot_gridlines=False, levels=None):
    """
    Plot the precipitation climatology.

    Parameters
    ----------
    climatology_data : xarray.DataArray
        Precipitation climatology data
    model_name : str
        Name of the climate model
    season : str
        Climatological season (one of DJF, MAM, JJA, SON)
    mask : optional str
        mask to apply to plot (one of "land" or "ocean")
    plot_gridlines : bool

        Select whether to plot gridlines
    levels : list
        Tick mark values for the colorbar

    Returns
    -------
    None

    """
    if not levels:
        levels = np.arange(0, 13.5, 1.5)

    fig, geo_axes = plot.subplots(
        nrows=1,
        ncols=1,
        figsize=(12, 5),
        subplot_kw={"projection": ccrs.PlateCarree(central_longitude=180)},
    )

    climatology_data.sel(season=season).plot.contourf(
        ax=geo_axes,
        levels=levels,
        extend="max",
        transform=ccrs.PlateCarree(),
        cbar_kwargs={"label": climatology_data.units},
        cmap=cmocean.cm.rain,
    )

    geo_axes.add_feature(
        cfeature.COASTLINE, lw=2
    )  # Add coastines using cartopy feature

    if mask:
        # Mask out (fade) using 110m resolution data from cartopy.
        geo_axes.add_feature(
            cfeature.NaturalEarthFeature("physical", mask, "110m"),
            ec=None,
            fc="white",
            lw=2,
            alpha=0.75,
        )

    if plot_gridlines:
        gridlines = geo_axes.gridlines(
            crs=ccrs.PlateCarree(),
            draw_labels=True,
            linewidth=2,
            color="gray",
            alpha=0.5,
            linestyle="--",
        )
        gridlines.top_labels = False
        gridlines.left_labels = True
        # gl.xlines = False
        gridlines.xlocator = mticker.FixedLocator([-180, -90, 0, 90, 180])
        gridlines.ylocator = mticker.FixedLocator(
            [-66, -23, 0, 23, 66]
        )  # Tropics & Polar Circles
        gridlines.xformatter = LONGITUDE_FORMATTER
        gridlines.yformatter = LATITUDE_FORMATTER
        gridlines.xlabel_style = {"size": 15, "color": "gray"}
        gridlines.ylabel_style = {"size": 15, "color": "gray"}

    title = f"{model_name} precipitation climatology ({season})"
    plot.title(title)


def main(
        precipitation_netcdf_file,
        season="DJF",
        output_file="output.png",
        plot_gridlines=False,
        mask=None,
        cbar_levels=None,
        countries=None,
):
    """
    Run the program for producing precipitation plots.

    Parameters
    ----------
    precipitation_netcdf_file : str
        netCDF filename to read precipitation data from
    season : optional str
        Climatological season (one of DJF, MAM, JJA, SON)
    output_file : optional str
        filename to save main image to
    plot_gridlines : optional bool
        Select whether to plot gridlines
    mask : optional str
        mask to apply to plot (one of "land" or "ocean")
    cbar_levels : optional list
        Tick mark values for the colorbar
    countries : optional dict(str: str)
        dictionary mapping country names to regionmask codes. For a list see:
        regionmask.defined_regions.natural_earth_v5_0_0.countries_110.regions

    Returns
    -------
    None

    """
    if countries is None:
        countries = {"United Kingdom": "GB"}

    input_data = xr.open_dataset(precipitation_netcdf_file)

    plot_zonally_averaged_precipitation(input_data)
    plot_hovmoller_diagram(input_data)
    get_country_annual_average(input_data, countries)

    climatology = input_data["precipitation"].groupby("time.season").mean("time", keep_attrs=True)

    try:
        input_units = climatology.attrs["units"]
    except KeyError as exc:
        raise KeyError(
            "Precipitation variable in {pr_file} must have a units attribute"
        ) from exc

    if input_units == "kg m-2 s-1":
        climatology = convert_precipitation_units(climatology)
    elif input_units == "mm/day":
        pass
    else:
        raise ValueError("""Input units are not 'kg m-2 s-1' or 'mm/day'""")

    create_precipitation_climatology_plot(
        climatology,
        input_data.attrs["source_id"],
        season,
        mask=mask,
        plot_gridlines=plot_gridlines,
        levels=cbar_levels,
    )

    plot.savefig(output_file, dpi=200)


if __name__ == "__main__":
    # Get config from command line
    config_name = input("Enter configuration name: ")
    if config_name == "":
        print("Using default configuration in 'default_config.json'.")
        config_name = "default_config"
    else:
        print(f"Using configuration in '{config_name}.json'.")
    config_file = config_name + ".json"
    with open(config_file, encoding="utf-8") as json_file:
        config = json.load(json_file)

    output_filename = f"{config_name}_output.png"
    gridlines_on = True
    colorbar_levels = None

    main(
        config["input_file"],
        season=config["season_to_plot"],
        output_file=output_filename,
        mask=config["mask_id"],
        plot_gridlines=config["gridlines_on"],
        countries=config["countries_to_record"],
    )
