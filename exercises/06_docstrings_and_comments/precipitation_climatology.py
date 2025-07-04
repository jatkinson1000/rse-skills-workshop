import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import regionmask
import xarray as xr
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER


def convert_precipitation_units(precipitation_in_kg_per_m_squared_s):
    """Convert kg m-2 s-1 to mm day-1."""
    # density 1000 kg m-3 => 1 kg m-2 == 1 mm
    # There are 60*60*24 = 86400 seconds per day
    precipitation_in_mm_per_day = precipitation_in_kg_per_m_squared_s * 86400

    precipitation_in_mm_per_day.attrs["units"] = "mm/day"

    precipitation_upper_bound = 2000  # mm/day

    if precipitation_in_mm_per_day.data.min() < 0.0:
        raise ValueError("There is at least one negative precipitation value")
    if precipitation_in_mm_per_day.data.max() > precipitation_upper_bound:
        raise ValueError(
            f"There are precipitation values > {precipitation_upper_bound} mm/day"
        )

    return precipitation_in_mm_per_day


def plot_zonally_averaged_precipitation(precipitation_data):
    # print(data)
    zonal_precipitation = precipitation_data["pr"].mean("lon", keep_attrs=True)

    figure, axes = plt.subplots(nrows=4, ncols=1, figsize=(12, 8))

    zonal_precipitation.sel(lat=[0]).plot.line(ax=axes[0], hue="lat")
    zonal_precipitation.sel(lat=[-20, 20]).plot.line(ax=axes[1], hue="lat")
    zonal_precipitation.sel(lat=[-45, 45]).plot.line(ax=axes[2], hue="lat")
    zonal_precipitation.sel(lat=[-70, 70]).plot.line(ax=axes[3], hue="lat")

    plt.tight_layout()
    for axis in axes:
        axis.set_ylim(0.0, 1.0e-4)
        axis.grid()
    plt.savefig("zonal.png", dpi=200)  # Save figure to file

    figure, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))

    zonal_precipitation.T.plot()

    plt.savefig("zonal_map.png", dpi=200)  # Save figure to file


def get_country_annual_average(precipitation_data, countries):
    annual_average_precipitation = (
        precipitation_data["pr"].groupby("time.year").mean("time", keep_attrs=True)
    )
    annual_average_precipitation = convert_precipitation_units(
        annual_average_precipitation
    )

    country_mask = regionmask.defined_regions.natural_earth_v5_0_0.countries_110.mask(
        annual_average_precipitation
    )

    # List possible locations to plot
    # [print(k, v) for k, v in regionmask.defined_regions.natural_earth_v5_0_0.countries_110.regions.items()]

    with open(
        "annual_average_precipitation_by_country.txt", "w", encoding="utf-8"
    ) as datafile:
        for country_name, country_code in countries.items():
            # land.plot(ax=geo_axes, add_label=False, fc="white", lw=2, alpha=0.5)
            # clim = clim.where(ocean == "South Pacific Ocean")
            country_annual_average_precipitation = annual_average_precipitation.where(
                country_mask.cf == country_code
            )

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

            for year in country_annual_average_precipitation.year.values:
                precip = (
                    country_annual_average_precipitation.sel(year=year).mean().values
                )
                datafile.write(
                    "{} {} : {:2.3f} mm/day\n".format(
                        country_name.ljust(25), year, precip
                    )
                )
            datafile.write("\n")


def plot_enso_hovmoller_diagram(precipitation_data):
    enso = (
        precipitation_data["pr"]
        .sel(lat=slice(-1, 1))
        .sel(lon=slice(120, 280))
        .mean(dim="lat", keep_attrs=True)
    )
    # print(enso)
    # .groupby('time.year').mean('time', keep_attrs=True)

    # # convert to dataframe:
    # df = monthly_speed.reset_coords(drop=True).to_dataframe()
    # # add year and month indices:
    # df['month']=df.index.month
    # df['year']=df.index.year
    # # groupby month and year then mean:
    # enso = enso.groupby(['time.year','time.month']).mean().unstack().T.droplevel(0)
    # plot:
    enso.plot()

    plt.savefig("enso.png", dpi=200)  # Save figure to file


def create_precipitation_climatology_plot(
    seasonal_average_precipitation,
    model_name,
    season,
    mask=None,
    plot_gridlines=False,
    levels=None,
):
    """Plot the precipitation climatology.

    clim (xarray.DataArray): Precipitation climatology data
    model (str): Name of the climate model
    season (str): Season

    gridlines (bool): Select whether to plot gridlines
    levels (list): Tick marks on the colorbar

    """
    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,5), subplot_kw={'projection': "3d"})
    # clim.sel(season=season).T.plot.surface()
    # plt.show()

    if not levels:
        levels = np.arange(0, 13.5, 1.5)

    fig, geo_axes = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=(12, 5),
        subplot_kw={"projection": ccrs.PlateCarree(central_longitude=180)},
    )

    seasonal_average_precipitation.sel(season=season).plot.contourf(
        ax=geo_axes,
        levels=levels,
        extend="max",
        transform=ccrs.PlateCarree(),
        cbar_kwargs={"label": seasonal_average_precipitation.units},
        cmap=cmocean.cm.rain,
    )

    geo_axes.add_feature(
        cfeature.COASTLINE, lw=2
    )  # Add coastines using cartopy feature

    if mask:
        # Old approach of adding mask before combining into the below command.
        # if mask == "ocean":
        # old mask_feat = cfeature.NaturalEarthFeature("physical", "ocean", "110m")
        # oldold geo_axes.add_feature(cfeature.NaturalEarthFeature("physical", "ocean", "110m"),
        #                      ec="red", fc="yellow", lw=2, alpha=1.0)
        # elif mask == "land":
        # old mask_feat = cfeature.NaturalEarthFeature("physical", "land", "110m")
        # oldold # geo_axes.add_feature(cfeature.NaturalEarthFeature("physical", "ocean", "110m"),
        #                           ec="red", fc="yellow", lw=2, alpha=1.0)

        # oldold else:
        # oldold pass
        # oldold raise ValueError("Unknown ")

        # Mask out (fade) using 110m resolution data from cartopy.
        geo_axes.add_feature(
            cfeature.NaturalEarthFeature("physical", mask, "110m"),
            ec=None,
            fc="white",
            lw=2,
            alpha=0.75,
        )

    if plot_gridlines:
        # If we want gridlines run the code to do this:
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

    title = "{} precipitation climatology ({})".format(model_name, season)
    plt.title(title)
    # print("\n\n{}\n\n".format(clim.mean()))


def main(
    precipitation_netcdf_file,
    season="DJF",
    output_file="output.png",
    plot_gridlines=False,
    mask=None,
    cbar_levels=None,
    countries=None,
):
    """Run the program."""
    if countries is None:
        countries = {"United Kingdom": "GB"}

    precipitation_data = xr.open_dataset(precipitation_netcdf_file)

    plot_zonally_averaged_precipitation(precipitation_data)
    plot_enso_hovmoller_diagram(precipitation_data)
    get_country_annual_average(precipitation_data, countries)

    seasonal_average_precipitation = (
        precipitation_data["pr"].groupby("time.season").mean("time", keep_attrs=True)
    )

    try:
        input_units = seasonal_average_precipitation.attrs["units"]
    except KeyError as exc:
        raise KeyError(
            "Precipitation variable in {pr_file} must have a units attribute"
        ) from exc

    if input_units == "kg m-2 s-1":
        seasonal_average_precipitation = convert_precipitation_units(
            seasonal_average_precipitation
        )
    elif input_units == "mm/day":
        pass
    else:
        raise ValueError("""Input units are not 'kg m-2 s-1' or 'mm/day'""")

    create_precipitation_climatology_plot(
        seasonal_average_precipitation,
        precipitation_data.attrs["source_id"],
        season,
        mask=mask,
        plot_gridlines=plot_gridlines,
        levels=cbar_levels,
    )

    plt.savefig(output_file, dpi=200)  # Save figure to file


if __name__ == "__main__":
    input_file = (
        "../../data/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc"
    )
    # season_to_plot = "DJF"
    # season_to_plot = "MAM"
    season_to_plot = "JJA"
    # season_to_plot = "SON"
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
        plot_gridlines=gridlines_on,
        countries=countries_to_record,
    )
