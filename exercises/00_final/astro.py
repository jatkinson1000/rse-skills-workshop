"""
Astrophysical data analysis and plotting - stellar kinematics and populations.

This script filters stellar data, plotting HR diagrams and velocity statistics, after
loading relevant datasets for analysis.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rc
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.stats import chi2, norm

font = {"family": "sans-serif", "weight": "normal", "size": 15}
mpl.rc("font", **font)
rc("text", usetex=True)
rc("text.latex", preamble=r"\usepackage{cmbright}")


def filter_data(df, sgr):
    """
    Filter stellar dataset based on quality cuts and exclusion of Sagittarius members.

    Parameters
    ----------
    df : pandas.DataFrame
        The input stellar dataset.
    sgr : pandas.DataFrame
        DataFrame containing Sagittarius member star names to exclude.

    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame after applying quality cuts and removing Sagittarius members.
    """
    chi2lim = -2.39
    SNRlim = 10.0
    SNRlim2 = 30.0

    dataq = df[
        ((df.SNR_4000_4100 > SNRlim) | (df.SNR_5000_5100 > SNRlim2))
        & (df.chi2 < chi2lim)
        & (df.double == "no")
        & ~(df["starname"].isin(sgr["starname"]))
        # Select stars within 10 degrees of the Galactic plane
        & (df.b.abs() < 10.0)  # noqa:PLR2004
        & ((df.b < 0) | (df.l < 0))
    ]
    return dataq


def select_giants(dataq, logg_upper, logg_lower):
    """
    Select giant stars from the dataset based on log(g) and Teff limits.

    Parameters
    ----------
    dataq : pandas.DataFrame
        The input stellar dataset.
    logg_upper : float
        Upper limit for log(g) to select giants.
    logg_lower : float
        Lower limit for Teff to select giants.

    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame containing only giant stars.
    """
    data = dataq[(dataq.logg < logg_upper) & (dataq.Teff > logg_lower)].copy()
    return data


def plot_hr_and_feh(dataq, logg_upper, logg_lower, my_cmap):
    """
    Plot the Hertzsprung-Russell (HR) diagram and [Fe/H] distribution histogram.

    Figure saved as HR+FeHhist_forkinematics.png

    Parameters
    ----------
    dataq : pandas.DataFrame
        The input stellar dataset.
    logg_upper : float
        Upper limit for log(g) to indicate giants on the HR diagram.
    logg_lower : float
        Lower limit for Teff to indicate giants on the HR diagram.
    my_cmap : str or matplotlib Colormap
        Colormap to use for the HR diagram.

    Returns
    -------
    None
    """
    font = {"size": 18}
    mpl.rc("font", **font)

    cmap = my_cmap

    fig = plt.figure(figsize=(6.5, 7))

    gs = GridSpec(2, 1, height_ratios=[1.7, 1])  # 1 rows, 2 columns
    ax1 = fig.add_subplot(gs[0, 0])  # First row, first column
    ax2 = fig.add_subplot(gs[1, 0])  # First row, first column

    gs.update(hspace=0.3)

    divider1 = make_axes_locatable(ax1)
    cax1 = divider1.append_axes("right", size="4%", pad=0.05)
    plot1 = ax1.scatter(
        dataq.Teff, dataq.logg, c=dataq.FeH, vmax=0.5, vmin=-2.8, cmap=cmap, s=5
    )
    plt.colorbar(plot1, cax=cax1, label=r"$\mathrm{[Fe/H]}$")
    ax1.set_xlabel(r"$T_\mathrm{eff}$")
    ax1.set_ylabel(r"$\log g$")
    ax1.set_xlim([4000, 7500])
    ax1.set_ylim([0.5, 4.9])
    ax1.tick_params(axis="both", which="both", right=True, direction="in")
    ax1.invert_xaxis()
    ax1.invert_yaxis()
    ax1.axhline(logg_upper, linewidth=1.5, linestyle="--", color="grey")
    ax1.axhline(logg_lower, linewidth=1.5, linestyle="--", color="grey")

    ax2.hist(
        dataq.FeH,
        bins=np.arange(-3.0, 0.501, 0.1),
        label=r"$\mathrm{all}$",
        histtype="step",
        linewidth=2.0,
        color="grey",
    )
    ax2.legend(loc=1)
    ax2.set_xlim([-3.0, 0.5])
    ax2.set_xticks(np.arange(-3.0, 0.51, 0.5))
    ax2.set_xlabel(r"$\mathrm{[Fe/H]}$")
    ax2.set_ylabel(r"$\mathrm{Number~of~stars}$")

    ax1.xaxis.set_ticks_position("both")
    ax1.yaxis.set_ticks_position("both")
    ax1.tick_params(axis="both", direction="in")
    ax2.yaxis.set_ticks_position("both")
    ax2.xaxis.set_ticks_position("both")
    ax2.tick_params(axis="both", direction="in")

    plt.savefig("HR+FeHhist_forkinematics.png", bbox_inches="tight")


def compute_rv_gc(data):
    """
    Compute the Galactocentric radial velocity for each star.

    Parameters
    ----------
    data : pandas.DataFrame
        The input stellar dataset with columns 'rv', 'l', and 'b'.

    Returns
    -------
    pandas.DataFrame
        DataFrame with an added 'rv_gc' column for Galactocentric radial velocity.
    """
    rv_gc = (
        data.rv
        + 220 * np.sin(data.l * np.pi / 180) * np.cos(data.b * np.pi / 180)
        + 16.5
        * (
            np.sin(data.b * np.pi / 180) * np.sin(25 * np.pi / 180)
            + np.cos(data.b * np.pi / 180)
            * np.cos(25 * np.pi / 180)
            * np.cos((data.l - 53) * np.pi / 180)
        )
    )
    data["rv_gc"] = rv_gc
    return data


def plot_velocity_stats(
    stellar_data, vb_8_data, logg_upper, logg_lower, plot_labels=None
):
    """
    Plot velocity stats as a function of Galactic longitude for different [Fe/H] bins.

    Figure saved as velocities.png

    Parameters
    ----------
    stellar_data : pandas.DataFrame
        The input stellar dataset with computed Galactocentric velocities.
    vb_8_data : pandas.DataFrame
        Reference survey data for comparison.
    logg_upper : float
        Upper limit for log(g) to select giants.
    logg_lower : float
        Lower limit for log(g) to select giants.
    plot_labels : list of str, optional
        Labels for the different [Fe/H] bins.

    Returns
    -------
    None
    """
    if plot_labels is None:
        plot_labels = ["typical", "older", "oldest"]

    s2 = 18

    fig, ax = plt.subplots(1, 3, figsize=(13, 4))
    for minfeh, maxfeh, kolom, description in zip(
        [-1.0, -1.5, -2.5], [0.0, -1.0, -1.5], [0, 1, 2], plot_labels, strict=True
    ):
        factor = 1.0

        for gr in ["-", "+"]:
            ls = []
            v_avs = []
            v_avs_err = []
            v_disps = []
            v_hists = []
            v_disp_low_errs = []
            v_disp_high_errs = []
            nbin2 = []

            lwidth = 2.5
            if gr == "-":
                llist = np.arange(1.0, 13.1, lwidth)
            elif gr == "+":
                llist = np.arange(-12.0, -1.0, lwidth)

            for l_value in llist:
                b_l = stellar_data[
                    (stellar_data.FeH <= maxfeh)
                    & (stellar_data.FeH >= minfeh)
                    & (stellar_data.l > l_value)
                    & (stellar_data.l < l_value + lwidth)
                ]
                ls.append(l_value + lwidth / 2)

                # Only use data for which there are 10 values
                MIN_BIN_SIZE = 10
                if len(b_l) >= MIN_BIN_SIZE:
                    v_disp = b_l.rv_gc.std()
                    v_av = b_l.rv_gc.mean() * factor
                    interval = 0.32
                    v_err = norm.isf(interval / 2) * v_disp / np.sqrt(len(b_l.rv_gc))

                    N = len(b_l.rv_gc)
                    X2low = chi2.isf(interval / 2, N - 1)
                    X2high = chi2.isf(1 - interval / 2, N - 1)
                    lowlim = np.sqrt(((N - 1) / X2low) * v_disp**2)
                    highlim = np.sqrt(((N - 1) / X2high) * v_disp**2)

                    v_avs.append(v_av)
                    v_avs_err.append(v_err)
                    v_disps.append(v_disp)
                    v_hists.append(b_l.rv_gc)
                    v_disp_low_errs.append(v_disp - lowlim)
                    v_disp_high_errs.append(highlim - v_disp)

                    nbin2.append(len(b_l.rv_gc))

                else:
                    v_avs.append(np.nan)
                    v_avs_err.append(np.nan)
                    v_disps.append(np.nan)
                    v_hists.append(np.nan)
                    v_disp_low_errs.append(np.nan)
                    v_disp_high_errs.append(np.nan)

            ax[kolom].scatter(
                np.array(ls),
                v_avs,
                color="grey",
                zorder=9,
                marker="o",
                s=60,
                edgecolors="black",
                linewidths=1,
            )
            ax[kolom].errorbar(
                np.array(ls),
                v_avs,
                yerr=v_avs_err,
                linestyle="None",
                capsize=2,
                mew=1,
                zorder=8,
                color="grey",
            )

        ax[kolom].plot(
            vb_8_data.l,
            vb_8_data.rv_mean,
            color="black",
            label="a typical survey",
            linestyle="--",
            zorder=7,
        )
        if kolom == 0:
            ax[kolom].legend(fontsize=15)
        ax[kolom].plot([-12, 12], [0, 0], linestyle="-.", color="grey", linewidth=1)
        ax[kolom].set_xlim([-12.0, 12.0])
        ax[kolom].set_ylim([-100, 100])
        ax[kolom].yaxis.set_ticks_position("both")
        ax[kolom].xaxis.set_ticks_position("both")
        ax[kolom].xaxis.set_ticks([-9, -6, -3, 0, 3, 6, 9])
        ax[kolom].yaxis.set_ticks([-100, -75, -50, -25, 0, 25, 50, 75, 100])
        ax[kolom].yaxis.set_ticklabels(
            ["", "", "$-50$", "", "$0$", "", "$50$", "", "$100$"]
        )
        ax[kolom].tick_params(axis="both", direction="in", labelsize=s2)
        ax[kolom].set_xlabel(r"$l~\mathrm{(degrees)}$", fontsize=s2)
        ax[kolom].set_ylabel("projected velocity [km/s]", fontsize=s2)
        ax[kolom].invert_xaxis()
        FeHdat = stellar_data[
            (stellar_data.FeH <= maxfeh)
            & (stellar_data.FeH >= minfeh)
            & (stellar_data.logg > logg_lower)
            & (stellar_data.logg < logg_upper)
        ]
        ax[kolom].text(11, -90, rf"$N_\mathrm{{*}} = {len(FeHdat)}$", fontsize=18)

        ax[kolom].set_title(
            "$"
            + str(minfeh)
            + r" < \mathrm{[Fe/H]} < "
            + str(maxfeh)
            + "$ \n ({})".format(description),
            fontsize=s2,
        )

        if kolom in {1, 2, 3}:
            ax[kolom].set_yticklabels([])
            ax[kolom].set_ylabel("")

    fig.subplots_adjust(hspace=0.0, wspace=0.0, right=0.91)
    plt.savefig("velocities.png", bbox_inches="tight")
    plt.close()


def load_pigs_data():
    """
    Load the PIGS stellar dataset.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the PIGS data.
    """
    return pd.read_csv("../../data/pigsdata.csv")


def load_sgr_members():
    """
    Load the list of Sagittarius dwarf galaxy member stars.

    These stars need to be removed because they are Sagittarius dwarf galaxy stars


    Returns
    -------
    pandas.DataFrame
        DataFrame containing Sagittarius member star names.
    """
    return pd.read_csv("../../data/sgr-members.dat")


def load_brava_data():
    """
    Load the BRAVA survey data for guidance lines.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing BRAVA survey data with cols 'l', 'rv_mean', and 'rv_sig'.
    """
    return pd.read_csv(
        "../../data/brava-survey.dat", sep=r"\s+", names=["l", "rv_mean", "rv_sig"]
    )


def main():
    """
    Run main function with data loading, filtering, analysis, and plotting.

    Loads datasets, applies filters, computes velocities, and generates plots for
    HR diagrams and velocity statistics.

    Returns
    -------
    None
    """
    df = load_pigs_data()
    sgr = load_sgr_members()
    vb_8_data = load_brava_data()
    ## limits on log g, to only take a subset of giants into account
    logg_upper = 3.7
    logg_lower = 1.0

    dataq = filter_data(df, sgr)
    data = select_giants(dataq, logg_upper, logg_lower)
    print(f"All good data (incl. dwarfs): {len(dataq)}")
    print(f"All good data (only giants):  {len(data)}")
    plot_hr_and_feh(dataq, logg_upper, logg_lower, my_cmap="jet")
    data = compute_rv_gc(data)
    plot_velocity_stats(
        data,
        vb_8_data,
        logg_upper,
        logg_lower,
        plot_labels=["typical stars", "older stars", "the oldest stars"],
    )


if __name__ == "__main__":
    main()
