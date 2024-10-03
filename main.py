import base64
import io
import pickle
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import numpy as np
from scipy import stats
import argparse


def main(season=88, matchDay=15, data=None, ax=None, pals=None):
    if not data:
        title = 'LL' + str(season) + ' Leaguewide MD' + str(matchDay)
        path = 'LL' + str(season) + '_Leaguewide_' + title.split(' ')[-1] + '.csv'
        try:
            data = pd.read_csv(path, encoding='ISO-8859-1', index_col=2)
        except FileNotFoundError:
            try:
                data = pd.read_csv('./res/' + path, encoding='ISO-8859-1', index_col=2)
            except FileNotFoundError:
                print(f'File {path} not found')
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
    if not pals:
        pals = {'GeorgasP': '$\P$',
                'GrekF': '$\Finv$',
                'GrekL': '*',
                'QuinlanK': '$K_Q$',
                'BeattieW': '$\u263C$',
                'ReynenG': '$\mathrm{\mathbb{G}}$',
                'ReynenM': '$\mathcal{M}$',
                'MillsH': r'$\hslash$',
                'ThompsonA5': '$@$',
                'BaechlerC': '$\copyright$',
                'JenningsK': 'P',
                'SimpsonF': '$\oiiint$',
                'Bohr-LeeD': '$\\flat$',
                'deGrootD': '$\spadesuit$',
                'ChurchM2': r'$\yen$',
                'SchacterC': 'r$\mathbb{U}$',
                'BarratA': '$\\forall$',
                'ChalykoffN': '$\u2118$',
                'FoxA6': '$\u26BE$',
                'JainA1933': r'$\$$',
                }
    else:
        ucs = [[char for char in pal if char.isupper()] for pal in pals]
        pals = {p: f'${U[0]}_{U[1]}$' for p, U in zip(pals, ucs)}

    active_players = [p for p in pals.keys() if p in list(data.index.values)]

    def alphanum_key(s):
        return [(0, char.lower()) if char.isalpha() else (1, char) for char in s]

    active_players = sorted(active_players, key=alphanum_key)

    active_players = sorted(active_players, key=lambda x: (data.loc[x, 'Rundle'], alphanum_key(x)))
    for i, pal in enumerate(active_players):
        myRundle = data.loc[pal]['Rundle'][0]
        myRundleData = rData[rundles.index(myRundle)]
        myScore = data['QPct'][pal]
        myPercent = 0.01 * stats.percentileofscore(myRundleData['QPct'].to_list(), myScore, kind='weak')
        ax.scatter(myScore, myPercent, color='C' + str(rundles.index(myRundle)), marker=pals[pal], label=pal, s=200)
        ax.axvline(myScore, color='C' + str(rundles.index(myRundle)), alpha=0.35, linestyle=':')

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

    plt.tight_layout()
    img_io = io.BytesIO()

    fig.savefig(img_io, format='png', dpi=200)
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close()
    return img_base64


def annotate(season=88, matchDay=15):
    title = 'LL' + str(season) + ' Leaguewide MD' + str(matchDay)
    path = 'LL' + str(season) + '_Leaguewide_' + title.split(' ')[-1] + '.p'
    try:
        fig = pickle.load(f'res/{path}', 'rb')
    except FileNotFoundError:
        print('Error, no pickled Figure available')


if __name__ == "__main__":
    path = './res/'
    pattern = 'LL[0-9]*_Leaguewide_MD[0-9]*.csv'
    parser = argparse.ArgumentParser()
    parser.add_argument('--season', '-s', type=int)
    parser.add_argument('--day', '-d', type=int)
    args = parser.parse_args()
    print(args.season, args.day)
    main(season=args.season, matchDay=args.day)
