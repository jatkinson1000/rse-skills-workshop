import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import scipy
import cf_xarray
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean
import regionmask


import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


def convert_pr_units(darray):
    """Convert kg m-2 s-1 to mm day-1.
    """
    
    darray.data = darray.data * 86400
    darray.attrs['units'] = 'mm/day'
    
    if darray.data.min() < 0.0:
        raise ValueError('There is at least one negative precipitation value')
    if darray.data.max() > 2000:
        raise ValueError('There is a precipitation value/s > 2000 mm/day')
    
    return darray


def apply_mask(darray, sftlf_file, realm):
    # Function to mask ocean or land using a sftlf (land surface fraction) file.
    # Inputs:
    #  darray: Data to mask
    #  sftlf_file: Land surface fraction file
    #  realm: Realm to mask
   
    # This is now done using cartopy package with a single line.
    pass


def plot_zonal(data):
    # print(data)
    zonal_pr = data['pr'].mean('lon', keep_attrs=True)

    fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(12,8))

    zonal_pr.sel(lat=[0]).plot.line(ax=ax[0], hue="lat")
    zonal_pr.sel(lat=[-20, 20]).plot.line(ax=ax[1], hue="lat")
    zonal_pr.sel(lat=[-45, 45]).plot.line(ax=ax[2], hue="lat")
    zonal_pr.sel(lat=[-70, 70]).plot.line(ax=ax[3], hue="lat")

    plt.tight_layout()
    for axis in ax:
        axis.set_ylim(0.0, 1.0e-4)
        axis.grid()
    plt.savefig("zonal.png", dpi=200)  # Save figure to file



    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,5))

    zonal_pr.T.plot()

    plt.savefig("zonal_map.png", dpi=200)  # Save figure to file



def get_country_ann_avg(data, countries):
    data_avg = data['pr'].groupby('time.year').mean('time', keep_attrs=True)
    data_avg = convert_pr_units(data_avg)

    land = regionmask.defined_regions.natural_earth_v5_0_0.countries_110.mask(data_avg)

    # List possible locations to plot
    # [print(k, v) for k, v in regionmask.defined_regions.natural_earth_v5_0_0.countries_110.regions.items()]

    with open("data.txt", "w") as datafile:
        for k, v in countries.items():
            # land.plot(ax=geo_axes, add_label=False, fc="white", lw=2, alpha=0.5)
            # clim = clim.where(ocean == "South Pacific Ocean")
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
                precip = data_avg_mask.sel(year = yr).mean().values
                datafile.write("{} {} : {:2.3f} mm/day\n".format(k.ljust(25), yr, precip))
            datafile.write("\n")






def plot_enso(data):
    enso = data['pr'].sel(lat=slice(-1, 1)).sel(lon=slice(120, 280)).mean(dim="lat", keep_attrs=True)
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




def create_plot(clim, model, season, mask=None, gridlines=False, levels=None):
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
        
    fig, geo_axes = plt.subplots(nrows=1, ncols=1, figsize=(12,5),
                    subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)})

    clim.sel(season=season).plot.contourf(ax=geo_axes,
                                          levels=levels,
                                          extend='max',
                                          transform=ccrs.PlateCarree(),
                                          cbar_kwargs={'label': clim.units},
                                          cmap=cmocean.cm.rain)
    
    geo_axes.add_feature(cfeature.COASTLINE, lw=2)  # Add coastines using cartopy feature

    if mask:
        # Old approach of adding mask before combining into the below command.
        # if mask == "ocean":
            #old mask_feat = cfeature.NaturalEarthFeature("physical", "ocean", "110m")
            #oldold geo_axes.add_feature(cfeature.NaturalEarthFeature("physical", "ocean", "110m"),
            #                      ec="red", fc="yellow", lw=2, alpha=1.0)
        # elif mask == "land":
            #old mask_feat = cfeature.NaturalEarthFeature("physical", "land", "110m")
            #oldold # geo_axes.add_feature(cfeature.NaturalEarthFeature("physical", "ocean", "110m"),
            #                           ec="red", fc="yellow", lw=2, alpha=1.0)

        #oldold else:
            #oldold pass
            #oldold raise ValueError("Unknown ")
        

        # Mask out (fade) using 110m resolution data from cartopy.
        geo_axes.add_feature(cfeature.NaturalEarthFeature("physical", mask, "110m"), ec=None, fc="white", lw=2, alpha=0.75)


    if gridlines:
        # If we want gridlines run the code to do this:
        gl = geo_axes.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
        linewidth=2, color='gray', alpha=0.5, linestyle='--')
        gl.top_labels = False
        gl.left_labels = True
        # gl.xlines = False
        gl.xlocator = mticker.FixedLocator([-180, -90, 0, 90, 180])
        gl.ylocator = mticker.FixedLocator([-66, -23, 0, 23, 66])  # Tropics & Polar Circles
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'size': 15, 'color': 'gray'}
        gl.ylabel_style = {'size': 15, 'color': 'gray'}


    title = '{} precipitation climatology ({})'.format(model, season)
    plt.title(title)
    # print("\n\n{}\n\n".format(clim.mean()))



def main(pr_file, season="DJF", output_file="output.png", gridlines=False, mask=None, cbar_levels=None, countries={"United Kingdom": "GB"}):
    """Run the program."""

    dset = xr.open_dataset(pr_file)

    plot_zonal(dset)
    plot_enso(dset)
    get_country_ann_avg(dset, countries)

    
    clim = dset['pr'].groupby('time.season').mean('time', keep_attrs=True)

    try:
        input_units = clim.attrs['units']
    except KeyError:
        raise KeyError("Precipitation variable in {pr_file} must have a units attribute")

    if input_units == 'kg m-2 s-1':
        clim = convert_pr_units(clim)
    elif input_units == 'mm/day':
        pass
    else:
        raise ValueError("""Input units are not 'kg m-2 s-1' or 'mm/day'""")

    create_plot(clim, dset.attrs['source_id'], season, mask=mask,
                gridlines=gridlines, levels=cbar_levels)
                
    plt.savefig(output_file, dpi=200)  # Save figure to file

if __name__ == '__main__':
    input_file = "../../data/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc"
    # season_to_plot = "DJF"
    # season_to_plot = "MAM"
    season_to_plot = "JJA"
    # season_to_plot = "SON"
    output_filename = "output.png"
    gridlines_on = True
    mask_id = "ocean"
    cbar_levels = None
    countries = {"United Kingdom": "GB", "United States of America": "US", "Antarctica": "AQ",
                 "South Africa": "ZA"}

    main(input_file, season=season_to_plot, mask=mask_id, gridlines=gridlines_on, countries=countries)
