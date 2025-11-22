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
    """Filter the dataset."""
    ## filter the data according to the cuts above
    # ### Previous manual approach (replaced by pandas query)
    # filtered = []
    # for idx, row in df.iterrows():
    #     if (row['SNR_4000_4100'] > SNRlim or row['SNR_5000_5100'] > SNRlim2) and \
    #        row['chi2'] < chi2lim and row['double'] == "no" and \
    #        row['starname'] not in sgr['starname'].values and \
    #        abs(row['b']) < 10.0 and (row['b'] < 0 or row['l'] < 0):
    #         filtered.append(row)
    # dataq = pd.DataFrame(filtered)
    # print("Manual filter length:", len(dataq))

    dataq = df[
        ((df.SNR_4000_4100 > 10.0) | (df.SNR_5000_5100 > 30.0))
        & (df.chi2 < -2.39)
        & (df.double == "no")  # Chi_sq limit of -2.39
        & ~(df["starname"].isin(sgr["starname"]))
        & (df.b.abs() < 10.0)
        & ((df.b < 0) | (df.l < 0))
    ]
    return dataq


def giants(dataq, highlogggrens, lowlogggrens):
    data = dataq[(dataq.logg < highlogggrens) & (dataq.Teff > lowlogggrens)].copy()
    return data


def hrfeh(dataq, highlogggrens, lowlogggrens, my_cmap):
    ## PLOTTING OF THE HR DIAGRAM AND [Fe/H] DISTRIBUTION HISTOGRAM

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
    ax1.axhline(highlogggrens, linewidth=1.5, linestyle="--", color="grey")
    ax1.axhline(lowlogggrens, linewidth=1.5, linestyle="--", color="grey")

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
    # from astropy.coordinates import SkyCoord
    # c = SkyCoord(l=data.l*u.deg, b=data.b*u.deg, frame='galactic')

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
    data, data2, highlogggrens, lowlogggrens, plot_labels=None
):
    """
    Plot velocity stats as a function of Galactic longitude for different [Fe/H] bins.

    Figure saved as velocities.png

    Parameters
    ----------
    data : pandas.DataFrame
        The input stellar dataset with computed Galactocentric velocities.
    data2 : pandas.DataFrame
        Reference survey data for comparison.

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

            for l in llist:
                b_l = data[
                    (data.FeH <= maxfeh)
                    & (data.FeH >= minfeh)
                    & (data.l > l)
                    & (data.l < l + lwidth)
                ]
                ls.append(l + lwidth / 2)

                if len(b_l) >= 10:
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
            data2.l,
            data2.rv_mean,
            color="black",
            label="a typical survey",
            linestyle="--",
            zorder=7,
        )
        if kolom == 0:
            ax[kolom].legend(fontsize=15)
        ax[kolom].plot([-12, 12], [0, 0], linestyle="-.", color="grey", linewidth=1)
        # ax[kolom].set_xlim([-14.0, 12.0])
        # ax[kolom].set_xlim([-16.0, 16.0])
        # ax[kolom].set_xlim([-12.0, 16.0])
        ax[kolom].set_xlim([-12.0, 12.0])
        ax[kolom].set_ylim([-100, 100])
        ax[kolom].yaxis.set_ticks_position("both")
        ax[kolom].xaxis.set_ticks_position("both")
        # ax[kolom].xaxis.set_ticks([-12, -6, 0, 6, 12])
        ax[kolom].xaxis.set_ticks([-9, -6, -3, 0, 3, 6, 9])
        # ax[kolom].xaxis.set_ticks([-15, -12, -9, -6, -3, 0, 3, 6, 9, 12, 15])
        ax[kolom].yaxis.set_ticks([-100, -75, -50, -25, 0, 25, 50, 75, 100])
        ax[kolom].yaxis.set_ticklabels(
            ["", "", "$-50$", "", "$0$", "", "$50$", "", "$100$"]
        )
        ax[kolom].tick_params(axis="both", direction="in", labelsize=s2)
        ax[kolom].set_xlabel(r"$l~\mathrm{(degrees)}$", fontsize=s2)
        ax[kolom].set_ylabel("projected velocity [km/s]", fontsize=s2)
        ax[kolom].invert_xaxis()
        FeHdat = data[
            (data.FeH <= maxfeh)
            & (data.FeH >= minfeh)
            & (data.logg > lowlogggrens)
            & (data.logg < highlogggrens)
        ]
        ax[kolom].text(11, -90, r"$N_\mathrm{*} =\,$" + str(len(FeHdat)), fontsize=18)

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


def pigs():
    """
    Load the PIGS stellar dataset.
    """
    return pd.read_csv("../../data/pigsdata.csv")


def load_sgr_members():
    ## stars that need to be removed because they are Sagittarius dwarf galaxy stars
    return pd.read_csv("../../data/sgr-members.dat")


def brava():
    ## BRAVA data guidance line
    return pd.read_csv(
        "../../data/brava-survey.dat", sep=r"\s+", names=["l", "rv_mean", "rv_sig"]
    )


def main():
    df = pigs()
    sgr = load_sgr_members()
    vb_8 = brava()
    ## limits on log g, to only take a subset of giants into account
    highlogggrens = 3.7
    lowlogggrens = 1.0

    dataq = filter_data(df, sgr)
    data = giants(dataq, highlogggrens, lowlogggrens)
    print("All good data (incl. dwarfs): ", len(dataq))
    print("All good data (only giants):  ", len(data))
    hrfeh(dataq, highlogggrens, lowlogggrens, my_cmap="jet")
    data = compute_rv_gc(data)
    plot_velocity_stats(
        data,
        vb_8,
        highlogggrens,
        lowlogggrens,
        plot_labels=["typical stars", "older stars", "the oldest stars"],
    )


if __name__ == "__main__":
    main()
