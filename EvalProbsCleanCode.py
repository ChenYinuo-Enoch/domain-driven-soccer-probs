# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Domain model

# %%
inverse_bets_map = {
    'WIN__P1': ['WIN__PX', 'WIN__P2'],
    'WIN__1X': ['WIN__P2'],
    'WIN__12': ['WIN__PX'],
    'WIN__X2': ['WIN__P1'],
    'TOTALS__OVER(0.5)': ['TOTALS__UNDER(0.5)'],
    'TOTALS__OVER(1.5)': ['TOTALS__UNDER(1.5)'],
    'TOTALS__OVER(2.5)': ['TOTALS__UNDER(2.5)'],
    'TOTALS__OVER(3.5)': ['TOTALS__UNDER(3.5)'],
    'TOTALS__OVER(4.5)': ['TOTALS__UNDER(4.5)'],
    'TOTALS__OVER(5.5)': ['TOTALS__UNDER(5.5)'],
    'TOTALS__OVER(6.5)': ['TOTALS__UNDER(6.5)'],
    'TOTALS__OVER(7.5)': ['TOTALS__UNDER(7.5)'],
    'TOTALS__OVER(8.5)': ['TOTALS__UNDER(8.5)'],
    'P1__TOTALS__OVER(0.5)': ['P1__TOTALS__UNDER(0.5)'],
    'P1__TOTALS__OVER(1.5)': ['P1__TOTALS__UNDER(1.5)'],
    'P1__TOTALS__OVER(2.5)': ['P1__TOTALS__UNDER(2.5)'],
    'P1__TOTALS__OVER(3.5)': ['P1__TOTALS__UNDER(3.5)'],
    'P1__TOTALS__OVER(4.5)': ['P1__TOTALS__UNDER(4.5)'],
    'P1__TOTALS__OVER(5.5)': ['P1__TOTALS__UNDER(5.5)'],
    'P1__TOTALS__OVER(6.5)': ['P1__TOTALS__UNDER(6.5)'],
    'P1__TOTALS__OVER(7.5)': ['P1__TOTALS__UNDER(7.5)'],
    'P2__TOTALS__OVER(0.5)': ['P2__TOTALS__UNDER(0.5)'],
    'P2__TOTALS__OVER(1.5)': ['P2__TOTALS__UNDER(1.5)'],
    'P2__TOTALS__OVER(2.5)': ['P2__TOTALS__UNDER(2.5)'],
    'P2__TOTALS__OVER(3.5)': ['P2__TOTALS__UNDER(3.5)'],
    'P2__TOTALS__OVER(4.5)': ['P2__TOTALS__UNDER(4.5)'],
    'P2__TOTALS__OVER(5.5)': ['P2__TOTALS__UNDER(5.5)'],
    'P2__TOTALS__OVER(6.5)': ['P2__TOTALS__UNDER(6.5)'],
    'P2__TOTALS__OVER(7.5)': ['P2__TOTALS__UNDER(7.5)'],
    'HANDICAP__P1(0.5)': ['HANDICAP__P2(-0.5)'],
    'HANDICAP__P1(1.5)': ['HANDICAP__P2(-1.5)'],
    'HANDICAP__P1(2.5)': ['HANDICAP__P2(-2.5)'],
    'HANDICAP__P1(3.5)': ['HANDICAP__P2(-3.5)'],
    'HANDICAP__P1(4.5)': ['HANDICAP__P2(-4.5)'],
    'HANDICAP__P1(5.5)': ['HANDICAP__P2(-5.5)'],
    'HANDICAP__P1(-0.5)': ['HANDICAP__P2(0.5)'],
    'HANDICAP__P1(-1.5)': ['HANDICAP__P2(1.5)'],
    'HANDICAP__P1(-2.5)': ['HANDICAP__P2(2.5)'],
    'HANDICAP__P1(-3.5)': ['HANDICAP__P2(3.5)'],
    'HANDICAP__P1(-4.5)': ['HANDICAP__P2(4.5)'],
    'HANDICAP__P1(-5.5)': ['HANDICAP__P2(5.5)'],
    'BOTH_TEAMS_TO_SCORE__NO': ['BOTH_TEAMS_TO_SCORE__YES'],
    'TOTALS__ODD': ['TOTALS__EVEN'],
    'P1__TOTALS__ODD': ['P1__TOTALS__EVEN'],
    'P2__TOTALS__ODD': ['P2__TOTALS__EVEN'],
}

def prepare_all_markets(event_markets):
    res = []

    for bet in event_markets:
        if bet not in inverse_bets_map:
            #print(bet)
            continue

        market_bets = []
        bet_cf = event_markets[bet]
        market_bets.append((bet_cf, bet))
        if not bet_cf:
            continue

        missing_bet = False
        inverse_bets = inverse_bets_map[bet]
        for inv_bet in inverse_bets:
            if inv_bet not in event_markets:
                missing_bet = True
                break

            inv_bet_cf = event_markets[inv_bet]
            market_bets.append((inv_bet_cf, inv_bet))
            if not inv_bet_cf:
                missing_bet = True

        if missing_bet:
            continue

        res.append(market_bets)

    return res


# %%
def get_all_overrounds(all_markets):
    all_overrounds = {}

    for markets_group in all_markets:
        markets_group_overrounds = sum(1/cf for cf, bet in markets_group) - 1

        for cf, bet in markets_group:
            old_overround = all_overrounds.get(bet, float('inf'))

            if markets_group_overrounds < old_overround:
                all_overrounds[bet] = markets_group_overrounds
    
    return all_overrounds


# %%
import itertools
import re
import numpy as np


def get_winning_scores(bet: str, score1, score2, max_team_score: int) -> list[tuple[int, int]]:
    all_scores = list(itertools.product(range(score1, score1+max_team_score+1), range(score2, score2+max_team_score+1)))
    
    predicate = lambda s: False
    if bet == 'WIN__P1':
        predicate = lambda s: s[0] > s[1]
    elif bet == 'WIN__P2':
        predicate = lambda s: s[0] < s[1]
    elif bet == 'WIN__PX':
        predicate = lambda s: s[0] == s[1]
    elif bet == 'WIN__1X':
        predicate = lambda s: s[0] >= s[1]
    elif bet == 'WIN__12':
        predicate = lambda s: s[0] != s[1]
    elif bet == 'WIN__X2':
        predicate = lambda s: s[0] <= s[1]
    elif bet.startswith('TOTALS__OVER'):
        [points_str] = re.findall('\((\d\.5)\)', bet)
        predicate = lambda s: (s[0] + s[1]) > float(points_str) 
    elif bet.startswith('TOTALS__UNDER'):
        [points_str] = re.findall('\((\d\.5)\)', bet)
        predicate = lambda s: (s[0] + s[1]) < float(points_str) 
    elif bet.startswith('P1__TOTALS__OVER'):
        [points_str] = re.findall('\((\d\.5)\)', bet)
        predicate = lambda s: s[0] > float(points_str) 
    elif bet.startswith('P2__TOTALS__OVER'):
        [points_str] = re.findall('\((\d\.5)\)', bet)
        predicate = lambda s: s[1] > float(points_str) 
    elif bet.startswith('P1__TOTALS__UNDER'):
        [points_str] = re.findall('\((\d\.5)\)', bet)
        predicate = lambda s: s[0] < float(points_str) 
    elif bet.startswith('P2__TOTALS__UNDER'):
        [points_str] = re.findall('\((\d\.5)\)', bet)
        predicate = lambda s: s[1] < float(points_str) 
    elif bet == 'BOTH_TEAMS_TO_SCORE__NO':
        predicate = lambda s: (s[0] == 0) or (s[1] == 0)
    elif bet == 'BOTH_TEAMS_TO_SCORE__YES':
        predicate = lambda s: (s[0] != 0) and (s[1] != 0)
    elif bet == 'TOTALS__ODD':
        predicate = lambda s: ((s[0] + s[1]) % 2 == 1)
    elif bet == 'TOTALS__EVEN':
        predicate = lambda s: ((s[0] + s[1]) % 2 == 0)
    elif bet == 'P1__TOTALS__ODD':
        predicate = lambda s: ((s[0]) % 2 == 1)
    elif bet == 'P1__TOTALS__EVEN':
        predicate = lambda s: ((s[0]) % 2 == 0)
    elif bet == 'P2__TOTALS__ODD':
        predicate = lambda s: ((s[1]) % 2 == 1)
    elif bet == 'P2__TOTALS__EVEN':
        predicate = lambda s: ((s[1]) % 2 == 0)
    elif bet.startswith('HANDICAP__P1'):
        [points_str] = re.findall('\((-?\d\.5)\)', bet)
        predicate = lambda s: (s[0] + float(points_str)) > s[1] 
    elif bet.startswith('HANDICAP__P2'):
        [points_str] = re.findall('\((-?\d\.5)\)', bet)
        predicate = lambda s: s[0] < (s[1] + float(points_str))
    elif bet == '*':
        predicate = lambda s: True
        
    return [s for s in all_scores if predicate(s)]


# %%
# Create numpy system
import numpy as np

def get_equations_matrix(score1, score2, all_markets_by_bk, max_score):
    all_scores = get_winning_scores('*', score1, score2, max_score)
    score_idx = {f"{s1}:{s2}": i for i, (s1, s2) in enumerate(all_scores)}
    num_vars = len(score_idx)

    A_rows = []
    b_vals = []
    weights = []

    for bk, all_markets in all_markets_by_bk.items():
        for market in all_markets:
            margin = sum(1 / odd for odd, _ in market) - 1

            for odd, bet in market:
                win_scores = get_winning_scores(bet, score1, score2, max_score)
                if not win_scores:
                    continue

                cf = odd
                inv_coef = 1 / (margin + 1 - 1 / cf)
                assert inv_coef >= 1, 'Wrong inv_coef'

                #bet_prob = inv_coef / (cf + inv_coef)
                #bet_prob = 1 / cf
                #bet_prob = (2 - margin * cf) / (2 * cf)
                
                #b1, b2 = 1/(cf-1), (inv_coef-1)
                #bet_prob = (b1 + b1*b2) / (2*b1 + b1*b2 + 1)  # Gandar
                
                b1, b2 = 1/(cf-1), (inv_coef-1)
                bet_prob = ((b1 + b2) / 2) / ((b1 + b2) / 2 + 1)  # Knowles
                
                #weight = bet_prob
                #weight = bet_prob / margin
                weight = 1

                row = np.zeros(num_vars)
                for s1, s2 in win_scores:
                    key = f"{s1}:{s2}"
                    if key in score_idx:
                        row[score_idx[key]] += 1.0

                A_rows.append(row)
                b_vals.append(bet_prob)
                weights.append(weight)

    A = np.array(A_rows)
    b = np.array(b_vals)
    weights = np.array(weights)

    return A, b, weights, list(score_idx.keys())


# %%
import time
from scipy.optimize import minimize
from scipy.stats import poisson


def compute_prob_vector(mu1, mu2, rho):
    max_s1 = np.max(s1_arr)
    max_s2 = np.max(s2_arr)

    ps1 = poisson.pmf(np.arange(max_s1 + 1), mu1)
    ps2 = poisson.pmf(np.arange(max_s2 + 1), mu2)

    valid_mask = (s1_arr >= 0) & (s2_arr >= 0)
    base_probs = np.zeros_like(s1_arr, dtype=float)

    base_probs[valid_mask] = ps1[s1_arr[valid_mask]] * ps2[s2_arr[valid_mask]]

    # Vectorized rho correction
    rho_corrections = np.ones_like(base_probs)

    idx_00 = (s1_arr == 0) & (s2_arr == 0)
    idx_01 = (s1_arr == 0) & (s2_arr == 1)
    idx_10 = (s1_arr == 1) & (s2_arr == 0)
    idx_11 = (s1_arr == 1) & (s2_arr == 1)

    rho_corrections[idx_00] = 1 - mu1 * mu2 * rho
    rho_corrections[idx_01] = 1 + mu1 * rho
    rho_corrections[idx_10] = 1 + mu2 * rho
    rho_corrections[idx_11] = 1 - rho

    return base_probs * rho_corrections


def equations(x):
    mu1, mu2, rho = x

    # Dixon-Coles constraint: rho ∈ [max(-1/m1, -1/m2), min(1, 1/(m1*m2))]
    if not (max(-1/mu1, -1/mu2) <= rho <= min(1, 1/(mu1*mu2))):
        return np.inf

    p_vector = compute_prob_vector(mu1, mu2, rho)  # shape: (num_terms,)
    pred_probs = A @ p_vector  # shape: (num_equations,)

    errors = (pred_probs - b)
    weighted_error = np.sum(weights * errors**2) / np.sum(weights)

    return weighted_error


# %%

# %% [markdown]
# # Eval probs sysID

# %%
import pandas as pd
df2 = pd.read_parquet('./events_parquet')


# %%
def get_probs_from_row_matrix(row):
    # Preparation
    final_score = row['final_score']
    final_score_tuple = tuple(int(s) for s in final_score.split(':'))
    score1, score2 = 0, 0

    raw_markets = row['markets']
    markets = {k: v for k, v in raw_markets.items() if v is not None}

    all_markets = prepare_all_markets(markets)
    all_markets_by_bk = {'betcity': all_markets}

    all_overrounds = get_all_overrounds(all_markets)
    max_score = 15

    try:
        A, b, weights, score_keys = get_equations_matrix(score1, score2, all_markets_by_bk, max_score)
        if A.shape[1] == 0 or len(score_keys) == 0:
            return None
    except:
        return None
        
    # Run once before optimization
    s1_arr = np.array([int(k.split(":")[0]) - score1 for k in score_keys])
    s2_arr = np.array([int(k.split(":")[1]) - score2 for k in score_keys])

    def compute_prob_vector(mu1, mu2, rho):
        max_s1 = np.max(s1_arr)
        max_s2 = np.max(s2_arr)

        ps1 = poisson.pmf(np.arange(max_s1 + 1), mu1)
        ps2 = poisson.pmf(np.arange(max_s2 + 1), mu2)

        valid_mask = (s1_arr >= 0) & (s2_arr >= 0)
        base_probs = np.zeros_like(s1_arr, dtype=float)
        base_probs[valid_mask] = ps1[s1_arr[valid_mask]] * ps2[s2_arr[valid_mask]]

        rho_corrections = np.ones_like(base_probs)
        idx_00 = (s1_arr == 0) & (s2_arr == 0)
        idx_01 = (s1_arr == 0) & (s2_arr == 1)
        idx_10 = (s1_arr == 1) & (s2_arr == 0)
        idx_11 = (s1_arr == 1) & (s2_arr == 1)

        rho_corrections[idx_00] = 1 - mu1 * mu2 * rho
        rho_corrections[idx_01] = 1 + mu1 * rho
        rho_corrections[idx_10] = 1 + mu2 * rho
        rho_corrections[idx_11] = 1 - rho

        return base_probs * rho_corrections

    def equations(x):
        mu1, mu2, rho = x
        if not (max(-1/mu1, -1/mu2) <= rho <= min(1, 1/(mu1*mu2))):
            return np.inf
        p_vector = compute_prob_vector(mu1, mu2, rho)
        pred_probs = A @ p_vector
        errors = (pred_probs - b)
        weighted_error = np.sum(weights * errors**2) / np.sum(weights)
        return weighted_error

    x0 = [1.0, 1.0, 0.0]
    bounds = [(1e-3, None), (1e-3, None), (-10, 10)]
    result = minimize(equations, x0, bounds=bounds, method="L-BFGS-B", jac="2-point")

    mu1, mu2, rho = result.x
    error = equations(result.x)

    # Compute final prob vector
    p_vector = compute_prob_vector(mu1, mu2, rho)
    prob_dict = {score: prob for score, prob in zip(score_keys, p_vector)}

    # Build output
    bet_idx, cnt = {}, 0
    for market in all_markets:
        for _, bet in market:
            if bet not in bet_idx:
                bet_idx[bet] = cnt
                cnt += 1

    res = []
    for bet, idx in sorted(bet_idx.items()):
        if bet not in markets:
            continue

        coef = markets[bet]
        win_scores = get_winning_scores(bet, score1, score2, max_score)
        prob = sum(prob_dict.get(f"{s1}:{s2}", 0.0) for s1, s2 in win_scores)
        roi = 100 * (coef * prob - 1)
        
        if not 0 <= prob <= 1:
            return None
        
        if not -25 <= roi <= 10:
            return None

        res.append({
            'event_id': row['id'],
            'event': row['event'],
            'bet': bet,
            'ovr': all_overrounds[bet],
            'coef': coef,
            'roi': roi,
            'prob': float(prob),
            'err': error,
            'is_win': (final_score_tuple in win_scores),
        })

    return res


# %%
from tqdm.auto import tqdm

tqdm.pandas()
res_df_raw = df2.progress_apply(get_probs_from_row_matrix, axis=1)

# %%
res_df = res_df_raw.dropna().explode().apply(pd.Series)

res_df['margin'] = 1 + res_df['ovr']
res_df['rw_prob_sysid'] = res_df['prob']


# %%
# Drop outliers
def get_inv_coef(row):
    margin = row['margin'] - 1
    cf = row['coef']
    
    inv_coef = 1 / (margin + 1 - 1 / cf)

    return inv_coef

df = res_df.dropna(subset=['prob']).copy()
df['inv_coef'] = df[['coef', 'margin']].apply(get_inv_coef, axis=1)
df = df[(df['inv_coef'] >= 1) & ((1 + 1 / df['coef'] - 1e-4) > df['margin']) & (df['roi'] >= -25)].copy()


# %% [markdown]
# # Eval other probs

# %%
def get_rw_prob_inverse(row):
    cf = row['coef']
    return 1 / (cf + 0)

df['rw_prob_inverse'] = df[['coef', 'margin']].apply(get_rw_prob_inverse, axis=1)


# %%
def get_rw_prob_prop(row):
    margin = row['margin'] - 1
    cf = row['coef']
    
    rw_prob = (2 - margin * cf) / (2 * cf)  # XXX: Same as shin for 2 outcomes

    return rw_prob

df['rw_prob_prop'] = df[['coef', 'margin']].apply(get_rw_prob_prop, axis=1)


# %%
def get_rw_prob_ratio(row):
    margin = row['margin'] - 1
    cf = row['coef']
    inv_coef = 1 / (margin + 1 - 1 / cf)
    #inv_coef = max(inv_coef, 1.01)
    
    x, y = 1 / cf, 1 / inv_coef
    a = (x + y) - (x * y) - 1
    c = x * y
    s2 = -(-4 * a * c)**0.5 / (2 * a)
    rw_prob = x / (s2 + x - (x * s2)) 

    return rw_prob

df['rw_prob_ratio'] = df[['coef', 'margin']].apply(get_rw_prob_ratio, axis=1)


# %%
def get_rw_prob_balance(row):
    margin = row['margin'] - 1
    cf = row['coef']
    
    rw_prob = (1/cf - margin) / (1 - margin) 
    return rw_prob

df['rw_prob_balance'] = df[['coef', 'margin']].apply(get_rw_prob_balance, axis=1)


# %%
def get_rw_prob_eig(row):
    margin = row['margin'] - 1
    cf = row['coef']
    inv_coef = 1 / (margin + 1 - 1 / cf)

    i1, i2 = 1/cf, 1/inv_coef
    denom = (i1**i1*(1-i1)**(1-i1))

    o = (i2**i2*(1-i2)**(1-i2)/denom)**(1/(i1+i2-1))

    rw_prob = 1/(o+1)
    return rw_prob

df['rw_prob_eig'] = df[['coef', 'margin']].apply(get_rw_prob_eig, axis=1)

# %%
from scipy.optimize import fsolve

def get_rw_prob_jsd(row):
    margin = row['margin'] - 1
    cf = row['coef']
    inv_coef = 1 / (margin + 1 - 1 / cf)
    
    def kl(p, q):
        return (p-q) * np.log((p/(1-p)) / (q/(1-q)))

    def equation(p):
        return [
            (sum(p) - 1),
            (kl(p[0], 1/cf) - kl(p[1], 1/inv_coef))
        ]

    rw_prob = fsolve(equation, x0=(1/cf, 1/inv_coef))[0]
    
    return rw_prob

df['rw_prob_jsd'] = df[['coef', 'margin']].apply(get_rw_prob_jsd, axis=1)


# %%
def get_rw_prob_rascher(row):
    margin = row['margin'] - 1
    cf = row['coef']
    inv_coef = 1 / (margin + 1 - 1 / cf)

    b1, b2 = 1/(cf-1), (inv_coef-1)
    rw_prob = ((b1 / (1 + b1)) + (b2 / (1 + b2))) / 2
    
    return rw_prob

df['rw_prob_rascher'] = df[['coef', 'margin']].apply(get_rw_prob_rascher, axis=1)


# %%
def get_rw_prob_knowles(row):
    margin = row['margin'] - 1
    cf = row['coef']
    inv_coef = 1 / (margin + 1 - 1 / cf)

    b1, b2 = 1/(cf-1), (inv_coef-1)
    rw_prob = ((b1 + b2) / 2) / ((b1 + b2) / 2 + 1)

    return rw_prob

df['rw_prob_knowles'] = df[['coef', 'margin']].apply(get_rw_prob_knowles, axis=1)


# %%
def get_rw_prob_gandar(row):
    margin = row['margin'] - 1
    cf = row['coef']
    inv_coef = 1 / (margin + 1 - 1 / cf)

    b1, b2 = 1/(cf-1), (inv_coef-1)
    rw_prob = (b1 + b1*b2) / (2*b1 + b1*b2 + 1)

    return rw_prob

df['rw_prob_gandar'] = df[['coef', 'margin']].apply(get_rw_prob_gandar, axis=1)

# %%
# #!pip install goto-conversion
import goto_conversion
def get_rw_prob_goto(row):
    margin = row['margin'] - 1
    cf = row['coef']
    inv_coef = 1 / (margin + 1 - 1 / cf)

    rw_prob = goto_conversion.goto_conversion([cf, inv_coef], multiplicativeIfUnprudentOdds=True)[0]
    return rw_prob

df['rw_prob_goto'] = df[['coef', 'margin']].apply(get_rw_prob_goto, axis=1)

# %%

# %%
# Total amount of unique events
df.groupby(['event_id', 'event']).ngroups

# %%

# %% [markdown]
# # Generate plots and tables

# %%
df['event'] = df['event'].astype('category')
df['bet'] = df['bet'].astype('category')

# %% code_folding=[0]
# Persistent lines styling
import hashlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib

# Define a list of linestyles
LINESTYLES = ['-', '--', '-.']
MARKERS = ['.', 'o', 'v', '^', '<', '>', 's', 'X']

def get_style(label):
    """Generate a consistent color and linestyle for a given label"""
    # Hash the label
    if 'sysid' in label:
        label += 'salt123'
        
    hash_val = int(hashlib.sha256(label.encode()).hexdigest(), 16)

    # Generate color using a colormap
    cmap = matplotlib.colormaps['tab10']  # Change to "viridis", "plasma", etc., if needed
    color = cmap((hash_val % 10) / 10)  # Normalize within colormap range

    # Select linestyle
    linestyle = LINESTYLES[hash_val % len(LINESTYLES)]
    marker = MARKERS[hash_val % len(MARKERS)]
    
    return cmap, color, linestyle, marker


# %%
NAMES_MAP = {
    'rw_prob_sysid': 'sysID (Proposed)',
    'rw_prob_inverse': 'naive',
    'rw_prob': 'norm',
    'rw_prob_prop': 'prop',
    'rw_prob_ratio': 'ratio',
    'rw_prob_balance': 'balance',
    'rw_prob_eig': 'EIG',
    'rw_prob_jsd': 'JSD',
    'rw_prob_rascher': 'Rascher',
    'rw_prob_knowles': 'Knowles',
    'rw_prob_gandar': 'Gandar',
    'rw_prob_goto': 'goto',
}

# %%
import os
os.makedirs('Figures', exist_ok=True)

# %% [markdown]
# ## ECE Instability

# %%
# ECE instablility
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import brier_score_loss, log_loss
from tqdm.auto import tqdm

def ece_score(y_true, y_prob, n_bins=10):
    try:
        bins = pd.qcut(y_prob, q=n_bins, duplicates='drop', retbins=True)[1]
    except ValueError:
        bins = np.linspace(0, 1, n_bins + 1)
    
    bin_indices = np.digitize(y_prob, bins, right=True) - 1
    ece = 0.0
    for i in range(len(bins) - 1):
        bin_mask = bin_indices == i
        if np.any(bin_mask):
            bin_prob = y_prob[bin_mask].mean()
            bin_true = y_true[bin_mask].mean()
            bin_size = bin_mask.sum() / len(y_prob)
            ece += bin_size * np.abs(bin_true - bin_prob)
    return ece

# Settings
bins_range = list(range(10, 121, 15))
methods = [col for col in df.columns if col.startswith('rw_prob')]
mask = (1.01 <= df['coef']) & (df['coef'] <= 25) & (df['err'] < df['err'].quantile(0.99))

# Compute ECEs
ece_results = {method: [] for method in methods}

for n_bins in tqdm(bins_range):
    for method in methods:
        if method == 'rw_prob_inverse':
            continue
            
        eces = []
        frac = 0.05
        correction = 1 / np.sqrt(frac)
        for seed in range(1):
            sub_df = df[mask].sample(frac=frac, replace=True, random_state=seed)
            y_true = sub_df['is_win'].astype(bool).values
            y_prob = sub_df[method].values
            ece = ece_score(y_true, y_prob, n_bins=n_bins)
            eces.append(ece)
        ece_results[method].append(np.mean(eces))

        
# Plot
plt.figure(figsize=(8, 5))
for method, scores in reversed(ece_results.items()):
    if method == 'rw_prob_inverse':
        continue
        
    cmap, color, linestyle, marker = get_style(method)

    plt.plot(bins_range, scores, label=NAMES_MAP[method], color=color, linestyle=linestyle, marker=marker)

plt.xlabel('Number of bins (quantile-based)', fontsize=15)
plt.ylabel('ECE', fontsize=15)
plt.title('ECE vs Number of Bins for Different Methods', fontsize=17)
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', framealpha=1)
#plt.yscale('log')

plt.tick_params(axis='both', labelsize=12)

plt.tight_layout()

# Save figure in EPS format with 600 DPI
output_path = os.path.join("Figures", "ece-instability.eps")
plt.savefig(output_path, format='eps', dpi=600, bbox_inches='tight')

plt.show()

# %% [markdown]
# ## Brier score and logloss

# %%
# Brier Score and LogLoss boxplot with bootstrap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from tqdm.auto import tqdm

from sklearn.metrics import (
    brier_score_loss,
    log_loss,
)

mask = (1.01 <= df['coef']) & (df['coef'] <= 25) & (df['err'] < df['err'].quantile(0.99))
frac = 1
correction_factor = 1 / np.sqrt(frac)  # for frac=0.5

# Dictionary to collect errors for each method
error_dict = {}
error_dict_logloss = {}

for method in tqdm([col for col in df.columns if col.startswith('rw_prob')]):
    sub_errs = []
    sub_errs_logloss = []
    for i in tqdm(range(100)):
        sub_df = df[mask].sample(frac=frac, replace=True, random_state=i)
        y_prob, y_true = sub_df[method], sub_df['is_win'].astype(bool)
        err_brier = brier_score_loss(y_true, y_prob)
        err_log_loss = log_loss(y_true, y_prob)
        
        sub_errs.append(err_brier)
        sub_errs_logloss.append(err_log_loss)
        
    error_dict[method] = sub_errs
    error_dict_logloss[method] = sub_errs_logloss

print('Done eval')

# %%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Corrected Brier Scores
corrected_error_dict_brier = {
    NAMES_MAP[method]: (
        np.mean(vals) + (np.array(vals) - np.mean(vals)) * correction_factor
    )
    for method, vals in error_dict.items()
}
corrected_df_brier = pd.DataFrame(corrected_error_dict_brier)

# Corrected LogLoss
corrected_error_dict_logloss = {
    NAMES_MAP[method]: (
        np.mean(vals) + (np.array(vals) - np.mean(vals)) * correction_factor
    )
    for method, vals in error_dict_logloss.items()
}
corrected_df_logloss = pd.DataFrame(corrected_error_dict_logloss)

# Create subplots
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

# Plot Brier Score
corrected_df_brier[
    corrected_df_brier.median().sort_values(ascending=False).index
].boxplot(
    vert=False, grid=False, showfliers=False, ax=axes[0]
)
axes[0].set_title("Bootstrap Brier Score Distribution", fontsize=17)
axes[0].set_xlabel("Brier Score", fontsize=15)
#axes[0].set_ylabel("Method")

# Plot LogLoss
corrected_df_logloss[
    corrected_df_logloss.median().sort_values(ascending=False).index
].boxplot(
    vert=False, grid=False, showfliers=False, ax=axes[1]
)
axes[1].set_title("Bootstrap LogLoss Distribution", fontsize=17)
axes[1].set_xlabel("LogLoss", fontsize=15)
axes[1].set_ylabel("")  # Don't repeat "Method" label on the second subplot

axes[0].tick_params(axis='both', labelsize=15)
axes[1].tick_params(axis='both', labelsize=15)

plt.tight_layout()

# Save figure in EPS format with 600 DPI
output_path = os.path.join("Figures", "boxplot-brier-logloss.eps")
plt.savefig(output_path, format='eps', dpi=600, bbox_inches='tight')

plt.show()

# %%

# %% [markdown]
# ## Probability correlation

# %%
# Correlation bootstrap
import numpy as np
probs_df = df[[col for col in df.columns if col.startswith('rw_prob')]]

n_samples = 10
min_corrs = []
for i in range(n_samples):
    res = probs_df.sample(frac=1, replace=True, random_state=i).corr().min().min()
    min_corrs.append(res)
    
np.mean(min_corrs) * 100, np.std(min_corrs) * 100 * 10

# %%

# %% [markdown]
# ## Brier score improvement

# %%
# Brier Score improvement across bins
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from tqdm.auto import tqdm

from sklearn.metrics import (
    brier_score_loss,
    log_loss,
)

n_bins = 5
bins = np.linspace(0, 1, n_bins + 1)
bin_centers = [(bins[i] + bins[i+1]) / 2 for i in range(len(bins)-1)]

mask_common = (1.01 <= df['coef']) & (df['coef'] <= 25) & (df['err'] < df['err'].quantile(0.99))
baseline_method = 'rw_prob_inverse'

# Compute implied probability
implied_probs = 1 / df['coef']

# Initialize results
results = []

for method in tqdm([col for col in df.columns if col.startswith('rw_prob')]):
    for i in range(len(bins) - 1):
        bin_mask = (
            (implied_probs >= bins[i]) &
            (implied_probs < bins[i+1]) &
            mask_common
        )

        if bin_mask.sum() <= 1:
            continue

        y_true = df.loc[bin_mask, 'is_win'].astype(bool)
        y_pred_method = df.loc[bin_mask, method]
        y_pred_baseline = df.loc[bin_mask, baseline_method]

        method_brier = brier_score_loss(y_true, y_pred_method)
        baseline_brier = brier_score_loss(y_true, y_pred_baseline)

        improvement = ((baseline_brier - method_brier) / baseline_brier) * 100

        results.append({
            'method': method,
            'bin': bin_centers[i],  # Use bin center as numeric value
            'brier_loss': method_brier,
            'baseline_brier': baseline_brier,
            'improvement_pct': improvement,
            'bss': 1 - method_brier / baseline_brier,
        })

bin_df = pd.DataFrame(results)

# Pivot by numeric bin
pivot_df = bin_df.pivot_table(
    index='bin',
    columns='method',
    #values='improvement_pct',
    values='bss',
    aggfunc='mean'
).reindex(bin_centers)

# Bin counts using same binning strategy
bin_counts = pd.cut(
    implied_probs[mask_common],
    bins=bins,
    labels=bin_centers,
    ordered=True
).value_counts().reindex(bin_centers).fillna(0)



# %%
# Plotting
fig, ax = plt.subplots(figsize=(7, 5))
ax2 = ax.twinx()

for method in pivot_df.columns:
    if method == 'rw_prob_inverse':
        continue

    cmap, color, linestyle, marker = get_style(method)

    ax.plot(
        bin_centers,
        pivot_df[method],
        color=color, 
        linestyle=linestyle, 
        marker=marker,
        label=NAMES_MAP[method],
    )

# Bar plot
ax2.bar(
    bin_centers,
    bin_counts.values,
    width=(bins[1] - bins[0]) * 0.7,  # narrow bar
    alpha=1,
    color='none',
    label='Sample Count',
    edgecolor='lightblue',
    linestyle='-',
    linewidth=2,
)

ax.set_zorder(ax2.get_zorder()+1)
ax.patch.set_visible(False)

# Labels
ax.set_title('Brier Skill Score Over Naive Baseline', fontsize=17)
ax.set_xlabel('Implied Probability (Mean of Bin)', fontsize=15)
ax.set_ylabel('BSS', fontsize=15)
ax2.set_ylabel('Sample Count', fontsize=15)
ax.axhline(0, color='gray', linestyle='--', label='naive baseline')

ax.legend(title='Method', bbox_to_anchor=(1.15, 1), framealpha=1)
plt.xticks(bin_centers)  # Set tick positions

ax.tick_params(axis='both', labelsize=15)
ax2.tick_params(axis='both', labelsize=15)

#plt.tight_layout()

# Save figure in EPS format with 600 DPI
output_path = os.path.join("Figures", "brier-improvement.eps")
plt.savefig(output_path, format='eps', dpi=600, bbox_inches='tight')

plt.show()

# %%

# %% [markdown]
# ## MDS Projection

# %%
# MDS projection
import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import MDS

# Prepare MDS
probs_df = df[[col for col in df.columns if col.startswith('rw_prob')]]
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=0)
coords = mds.fit_transform(1 - probs_df.corr())

# Unique markers
markers = ['o', 's', 'D', '^', 'v', '<', '>', 'P', 'X', '*', 'h', 'H', '+', 'x', 'd', '|', '_']
colors = plt.cm.get_cmap('tab20', len(probs_df.columns))

# Plot
plt.figure(figsize=(7, 5))
for i, method in reversed(list(enumerate(probs_df.columns))):
    cmap, color, linestyle, marker = get_style(method)
    
    plt.scatter(coords[i, 0], coords[i, 1], 
                marker=marker, 
                color=color, 
                label=NAMES_MAP[method], 
                s=100)

plt.title("MDS Projection of Method Dissimilarities")
plt.xlabel("MDS1")
plt.ylabel("MDS2")
plt.grid(True)

plt.legend(title="Method", bbox_to_anchor=(1.025, 1), loc='upper left', framealpha=1)
plt.locator_params(axis='x', nbins=6)
plt.tight_layout()

# Save figure in EPS format with 600 DPI
output_path = os.path.join("Figures", "mds-projection.eps")
plt.savefig(output_path, format='eps', dpi=600)

plt.show()

# %%

# %% [markdown]
# ## Monte Carlo profit simulation

# %%
# Eval delta profits
df['delta_profit'] = -1.0
df.loc[df['is_win'] == True, 'delta_profit'] = df.loc[df['is_win'] == True, 'coef'] - 1

# %%
import numpy as np

coef = sub_df['coef'].to_numpy()
dp = sub_df['delta_profit'].to_numpy()

new_delta_profit = np.where(
    dp > 0, 
    1,
    np.where(
        dp == 0, 
        0,
        -1 / coef
    )
)

sub_df['new_delta_profit'] = new_delta_profit

# %%
coefs = sub_df['coef'].values
profits = 1
loss = -1 / sub_df['coef'].values
observed_profit = sub_df['new_delta_profit'].sum()

# %%
import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm
from math import ceil

mask = (1.01 <= df['coef']) & (df['coef'] <= 25) & (df['err'] < df['err'].quantile(0.99))
sub_df = df[mask].reset_index(drop=True)
methods = [col for col in df.columns if col.startswith('rw_prob')]

n_simulations = 1000
batch_size = 100  # you can tune this depending on available RAM

coef = sub_df['coef'].to_numpy()
dp = sub_df['delta_profit'].to_numpy()
bet_sizes = 1 / coef

new_delta_profit = np.where(
    dp > 0, 
    (coef - 1) * bet_sizes,
    np.where(
        dp == 0, 
        0,
        -bet_sizes
    )
)
sub_df['new_delta_profit'] = new_delta_profit
observed_profit = new_delta_profit.sum()

results = []

for method in tqdm(methods, desc='Computing MSE'):
    probs = sub_df[method].to_numpy()
    simulated_profits_all = []

    # Run simulations in smaller batches
    for i in range(ceil(n_simulations / batch_size)):
        this_batch = min(batch_size, n_simulations - i * batch_size)

        random_matrix = np.random.rand(this_batch, len(sub_df))
        wins = random_matrix <= probs
        sim_matrix = np.where(wins, 1 - 1 / coef, -1 / coef)
        simulated_profits = sim_matrix.sum(axis=1)
        simulated_profits_all.append(simulated_profits)

    simulated_profits_all = np.concatenate(simulated_profits_all)
    #mse = (simulated_profits_all.mean() - observed_profit) ** 2
    mse = ((simulated_profits_all - observed_profit) ** 2).mean()
    results.append((method, mse, simulated_profits_all))

# %%
# Sort methods by MSE ascending (smallest MSE first)
results.sort(key=lambda x: x[1])
min_mse = min([mse for m, mse, _ in results])

# Layout for plots
n_methods = len(results)
n_cols = ceil(sqrt(n_methods))
n_rows_plot = ceil(n_methods / n_cols)

fig, axes = plt.subplots(n_rows_plot, n_cols, figsize=(4 * n_cols, 3.5 * n_rows_plot))
axes = axes.flatten()

# Plot sorted
for idx, (method, mse, simulated_profits) in enumerate(results):
    ax = axes[idx]
    ax.hist(simulated_profits, bins=17, alpha=1, histtype='step', density=False)
    ax.axvline(observed_profit, color='red', linestyle='--', linewidth=2)
    ax.set_title(f'{NAMES_MAP[method]}\nScaled MSE = x{mse / min_mse:.2f}', fontsize=18)
    ax.set_xlabel('Profit', fontsize=14)
    ax.set_ylabel('Freq', fontsize=14)
    ax.locator_params(axis='x', nbins=3)
    ax.tick_params(axis='both', labelsize=12)
    plt.tight_layout()

# Remove unused axes
for j in range(len(results), len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()

# Save figure in EPS format with 600 DPI
output_path = os.path.join("Figures", "monte-carlo-pdf.eps")
plt.savefig(output_path, format='eps', dpi=600)

plt.show()

# %%
