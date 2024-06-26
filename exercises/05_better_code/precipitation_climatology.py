"""Routines for analysing precipitation climatology from ESM runs."""

import numpy as np
import matplotlib.pyplot as plt
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
        xarray DataArray containing model precipitation data in kg m-2 s-1

    Returns
    -------
    precipitation_in_mm_per_day : xarray.DataArray
        the input DataArray with precipitation units modified to mm day-1
    """
    # density 1000 kg m-3 => 1 kg m-2 == 1 mm
    # There are 60*60*24 = 86400 seconds per day
    precipitation_in_kg_per_m_squared_s.data = precipitation_in_kg_per_m_squared_s.data * 86400
    precipitation_in_kg_per_m_squared_s.attrs["units"] = "mm/day"

    assert (
            precipitation_in_kg_per_m_squared_s.data.min() >= 0.0
    ), "There is at least one negative precipitation value"
    assert precipitation_in_kg_per_m_squared_s.data.max() < 2000, "There is a precipitation value/s > 2000 mm/day"

    return precipitation_in_kg_per_m_squared_s


def plot_zonal(data):
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
    zonal_pr = data["pr"].mean("lon", keep_attrs=True)

    fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(12, 8))

    zonal_pr.sel(lat=[0]).plot.line(ax=ax[0], hue="lat")
    zonal_pr.sel(lat=[-20, 20]).plot.line(ax=ax[1], hue="lat")
    zonal_pr.sel(lat=[-45, 45]).plot.line(ax=ax[2], hue="lat")
    zonal_pr.sel(lat=[-70, 70]).plot.line(ax=ax[3], hue="lat")

    plt.tight_layout()
    for axis in ax:
        axis.set_ylim(0.0, 1.0e-4)
        axis.grid()
    plt.savefig("zonal.png", dpi=200)  # Save figure to file

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))

    zonal_pr.T.plot()

    plt.savefig("zonal_map.png", dpi=200)  # Save figure to file


def get_country_ann_avg(data, countries):
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
    data_avg = data["pr"].groupby("time.year").mean("time", keep_attrs=True)
    data_avg = convert_precipitation_units(data_avg)

    land = regionmask.defined_regions.natural_earth_v5_0_0.countries_110.mask(data_avg)

    with open("data.txt", "w", encoding="utf-8") as datafile:
        for k, v in countries.items():
            data_avg_mask = data_avg.where(land.cf == v)

            # Debugging - plot countries to make sure mask works correctly
            # fig, geo_axes = plt.subplots(nrows=1, ncols=1, figsize=(12,5),
            #                 subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)})
            # data_avg_mask.sel(year = 2010).plot.contourf(ax=geo_axes,
            #                                       extend='max',
            #                                       transform=ccrs.PlateCarree(),
            #                                       cbar_kwargs={'label': data_avg_mask.units},
            #                                       cmap=cmocean.cm.haline_r)
            # geo_axes.add_feature(cfeature.COASTLINE, lw=0.5)
            # gl = geo_axes.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
            # linewidth=2, color='gray', alpha=0.5, linestyle='--')
            # gl.top_labels = False
            # gl.left_labels = True
            # gl.xlocator = mticker.FixedLocator([-180, -90, 0, 90])
            # gl.ylocator = mticker.FixedLocator([-66, -23, 0, 23, 66])
            # gl.xformatter = LONGITUDE_FORMATTER
            # gl.yformatter = LATITUDE_FORMATTER
            # gl.xlabel_style = {'size': 15, 'color': 'gray'}
            # gl.ylabel_style = {'size': 15, 'color': 'gray'}
            # print("show %s" %k)
            # plt.show()

            for yr in data_avg_mask.year.values:
                precip = data_avg_mask.sel(year=yr).mean().values
                datafile.write(
                    "{} {} : {:2.3f} mm/day\n".format(k.ljust(25), yr, precip)
                )
            datafile.write("\n")


def plot_enso(data):
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
        data["pr"]
        .sel(lat=slice(-1, 1))
        .sel(lon=slice(120, 280))
        .mean(dim="lat", keep_attrs=True)
    )

    enso.plot()
    plt.savefig("enso.png", dpi=200)  # Save figure to file


def create_plot(clim, model, season, mask=None, gridlines=False, levels=None):
    """
    Plot the precipitation climatology.

    Parameters
    ----------
    clim : xarray.DataArray
        Precipitation climatology data
    model : str
        Name of the climate model
    season : str
        Climatological season (one of DJF, MAM, JJA, SON)
    mask : optional str
        mask to apply to plot (one of "land" or "ocean")
    gridlines : bool
        Select whether to plot gridlines
    levels : list
        Tick mark values for the colorbar

    Returns
    -------
    None

    """
    if not levels:
        levels = np.arange(0, 13.5, 1.5)

    fig, geo_axes = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=(12, 5),
        subplot_kw={"projection": ccrs.PlateCarree(central_longitude=180)},
    )

    clim.sel(season=season).plot.contourf(
        ax=geo_axes,
        levels=levels,
        extend="max",
        transform=ccrs.PlateCarree(),
        cbar_kwargs={"label": clim.units},
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

    if gridlines:
        gl = geo_axes.gridlines(
            crs=ccrs.PlateCarree(),
            draw_labels=True,
            linewidth=2,
            color="gray",
            alpha=0.5,
            linestyle="--",
        )
        gl.top_labels = False
        gl.left_labels = True
        # gl.xlines = False
        gl.xlocator = mticker.FixedLocator([-180, -90, 0, 90, 180])
        gl.ylocator = mticker.FixedLocator(
            [-66, -23, 0, 23, 66]
        )  # Tropics & Polar Circles
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {"size": 15, "color": "gray"}
        gl.ylabel_style = {"size": 15, "color": "gray"}

    title = "{} precipitation climatology ({})".format(model, season)
    plt.title(title)


def main(
    pr_file,
    season="DJF",
    output_file="output.png",
    gridlines=False,
    mask=None,
    cbar_levels=None,
    countries=None,
):
    """
    Run the program for producing precipitation plots.

    Parameters
    ----------
    pr_file : str
        netCDF filename to read precipitation data from
    season : optional str
        Climatological season (one of DJF, MAM, JJA, SON)
    output_file : optional str
        filename to save main image to
    gridlines : optional bool
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

    dset = xr.open_dataset(pr_file)

    plot_zonal(dset)
    plot_enso(dset)
    get_country_ann_avg(dset, countries)

    clim = dset["pr"].groupby("time.season").mean("time", keep_attrs=True)

    try:
        input_units = clim.attrs["units"]
    except KeyError as exc:
        raise KeyError(
            "Precipitation variable in {pr_file} must have a units attribute"
        ) from exc

    if input_units == "kg m-2 s-1":
        clim = convert_precipitation_units(clim)
    elif input_units == "mm/day":
        pass
    else:
        raise ValueError("""Input units are not 'kg m-2 s-1' or 'mm/day'""")

    create_plot(
        clim,
        dset.attrs["source_id"],
        season,
        mask=mask,
        gridlines=gridlines,
        levels=cbar_levels,
    )

    plt.savefig(output_file, dpi=200)


if __name__ == "__main__":
    input_file = (
        "../../data/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc"
    )
    season_to_plot = "JJA"
    output_filename = "output.png"
    gridlines_on = True
    mask_id = "ocean"
    colorbar_levels = None
    countries_to_record = {
        "United Kingdom": "GB",
        "United States of America": "US",
        "Antarctica": "AQ",
        "South Africa": "ZA",
    }

    main(
        input_file,
        season=season_to_plot,
        mask=mask_id,
        gridlines=gridlines_on,
        countries=countries_to_record,
    )
