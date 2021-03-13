import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import numpy as np
from scipy import stats


def main(season=88, matchDay=15, data=None, ax=None):
    if not data:
        title = 'LL' + str(season) + ' Leaguewide MD' + str(matchDay)
        path = 'LL' + str(season) + '_Leaguewide_' + title.split(' ')[-1] + '.csv'
        try:
            data = pd.read_csv(path, encoding='ISO-8859-1', index_col=2)
        except FileNotFoundError:
            try:
                data = pd.read_csv('C:/users/wbeattie/downloads/' + path, encoding='ISO-8859-1', index_col=2)
            except FileNotFoundError:
                print('File not found')
                return

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(12, 7))

    # Plot a league-wide histogram
    ax.hist(data['QPct'], bins=np.linspace(0, 1, matchDay * 6), cumulative=True, density=True, histtype='step',
            label='All', color='black', linewidth=2, align='right')

    rundles = ['A', 'B', 'C', 'D', 'E', 'R']
    rData = []
    rDivData = []
    for rundle in rundles:
        run = data['Rundle']

        inRundle = [x[0] == rundle for x in run]
        rData.append(data[inRundle])

        inRundleDiv = [x[:6] == rundle + ' Mesa' for x in run]
        rDivData.append(data[inRundleDiv])

    # Plot rundle-specific histograms
    for r, d, dDiv in zip(rundles, rData, rDivData):
        ax.hist(d['QPct'], bins=np.linspace(0, 1, matchDay * 6), cumulative=True, density=True, label='Rundle ' + r,
                histtype='step', linewidth=0.75, align='mid', color='C' + str(rundles.index(r)))
        # ax.hist(dDiv['QPct'], bins=np.linspace(0, 1, matchDay * 6), cumulative=True, density=True, label='Rundle ' +
        #  r + ' Mesa', histtype='step', linewidth=1, linestyle=':', align='mid', color='C' + str(rundles.index(r)))

    # Plot individuals on their rundle's percentile curve, along with a vertical line to show how they'd do in other
    # rundles
    pals = {'GeorgasP': '$\P$', 'GrekF': '$\Finv$', 'GrekL': '*', 'QuinlanK': '$K_Q$', 'BeattieW': '$\u263C$',
            'ReynenG': '$\mathrm{\mathbb{G}}$', 'ReynenM':'$\mathcal{M}$', 'MillsH':r'$\hslash$', 'ThompsonA5':'$@$',
            'BaechlerC': '$\copyright$', 'JenningsK': 'P', 'SimpsonF': '$\oiiint$', 'Bohr-LeeD':'$\\flat$',
            'deGrootD':'$\spadesuit$'}
    for i, pal in enumerate(pals):
        if pal not in list(data.index.values):
            continue
        myRundle = data.loc[pal]['Rundle'][0]
        myRundleData = rData[rundles.index(myRundle)]
        myScore = data['QPct'][pal]
        myPercent = 0.01 * stats.percentileofscore(myRundleData['QPct'].to_list(), myScore, kind='weak')
        ax.scatter(myScore, myPercent, color='C' + str(rundles.index(myRundle)), marker=pals[pal], label=pal, s=200)
        ax.axvline(myScore, color='C' + str(rundles.index(myRundle)), alpha=0.5)
        print(pal, round(myScore, 3), round(data['QPct'][pal], 3), round(myPercent, 3))

    # Patches indicating relegation and promotion
    ps = [Rectangle((0, 0), 1, 0.2, color='red'), Rectangle((0, 0.8), 1, 0.2, color='green')]
    col = PatchCollection(ps, alpha=0.1, match_original=True)
    ax.add_collection(col)

    title = 'LL' + str(season) + ' Leaguewide MD' + str(matchDay)
    xticks = [0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]
    yticks = [0.1 * n for n in range(11)]

    ax.set_title(title)
    ax.legend(loc=2)
    ax.set_xlabel('Correct Answers (%)')
    ax.set_xlim(0, 1)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_yticks(np.linspace(0, 1, 11))
    ax.set_ylabel('Percentile')
    ax.set_ylim(0, 1)
    ax.yaxis.grid(linestyle=':')

    # Express labels as percentages, not fractions
    ax.set_xticklabels([round(100 * x) for x in xticks])
    ax.set_yticklabels([round(100 * y) for y in yticks])

    # plt.tight_layout()
    # plt.savefig(title+'.png', dpi=200)

    return data


def DE(data):
    rundles = ['A', 'B', 'C', 'D', 'E', 'R']
    rData = []
    for rundle in rundles:
        run = data['Rundle']
        inRundle = [x[0] == rundle for x in run]
        rData.append(data[inRundle])
    for r, d in zip(rundles, rData):
        x, y = d['CAA'], d['DE']

        x = [caa + np.random.rand() for caa in x]
        y = [de + (0.5 - np.random.rand()) * .1 for de in y]
        plt.scatter(x, y, label='Rundle ' + r, s=10, alpha=0.5)
    pals = ['GeorgasP', 'GrekF', 'GrekL', 'QuinlanK', 'BeattieW', 'ReynenG', 'JenningsK']

    markers = ['^', 'o', '*', 'h', 'p', '.', 'P']
    for m, pal in zip(markers, pals):
        plt.scatter(data['CAA'][pal], data['DE'][pal], s=100, marker=m, color='black', label=pal)

    run = data['Rundle']
    notR = [x[0] != 'R' for x in run]
    notR = data[notR]
    bestFit = np.polyfit(notR['CAA'], notR['DE'], 1)
    print(bestFit)
    plt.plot(np.linspace(0, max(data['CAA']), 10), [bestFit[1] + x * bestFit[0] for x in np.linspace(10, 50, 10)],
             color='black')
    ax.legend()
    ax.set_xlabel('Correct Answers Allowed')
    ax.set_ylabel('Defensive Efficiency')
    ax.set_title('Does Defense Get Easier with Strong Opponents?')


def multiPlot():
    days = ['9', '10', '11', '12', '13']
    fig, ax = plt.subplots(1, len(days))

    for i, day in enumerate(days):
        data = pd.read_csv('LL84_Leaguewide_MD' + day + '.csv', encoding='ISO-8859-1', index_col=2)
        main(data, ax=ax[i])


if __name__ == "__main__":
    """
    fig, ax = plt.subplots(3, 1, figsize=(12, 14))
    for i, n in enumerate([84, 85, 86]):
        data = main(season=n, matchDay=25, ax=ax[i])
    """
    main()
