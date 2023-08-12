'''
This code contains the functions to calculate the normalized confidence score for 
ASCVD, SMART, and UMRI risk scores, as required.
    def calc_vals
    def nc_model_weights
    def normalized_confidence

It also contains the function to plot variability of scores for 
each value within a variable of a risk calculator.
    def bar_plot_within_group

It also contains the function to plot the standard deviation of risk models
as their risk score increases.
    def std_risk_increasing
'''

import matplotlib.pyplot as plt
import numpy as np


def calc_vals(x, y):
    '''
    Compare score values variable by variable
    '''

    # First we group all the values in a target column e.g. UMRI scores
    # based on the categories or values in a source column e.g. gender:female/male
    sourceCol = x
    targetCol = y
    try:
        targetCol = [float(j) for j in targetCol]
    except:
        pass
    try:
        sourceCol = [float(j) for j in sourceCol]
    except:
        pass

    # Get all values from the sourceCol
    groups = {}
    for z in zip(sourceCol, targetCol):
        if z[0] not in groups:
            groups[z[0]] = [z[1]] 
        else:
            groups[z[0]].append(z[1]) 

    x_means = []
    x_counts = []
    x_ci_deltas = []
    x_stds = []
    x_keys = []
    for key in groups:
        t_dist = 1.960 # for conf_level 0.95: 1.96 is the approximate value of the 97.5 percentile point of the normal distribution:
        delta = t_dist * np.std(groups[key])/math.sqrt(len(groups[key]))
        x_counts.append(len(groups[key]))
        x_ci_deltas.append(delta)
        x_means.append(np.mean(groups[key]))
        x_stds.append(np.std(groups[key]))
        x_keys.append(key)
    print('keys', x_keys)
    print('means', x_means)
    print('stds', x_stds)
    print('counts', x_counts)
    return groups, x_means, x_stds, x_keys


def nc_model_weights(cols, col_list_filter, target_col):
    '''
    Pre-calculate weights for normalized confidence output normalized stds model for:
        ASCVD cols: 0 to 8 and target_col: 9 (ASCVD score)
        SMART: cols 10 to 23 and target_col: 24 (SMART score)
        UMRI: [cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[7], cols[8], cols[22], cols[23]] target_col: 25 (UMRI)
    '''
    headers = ['Race', 'Gender', 'Age', 'Systolic', 'Total Cholesterol', 'HDL', 'Diabetes', 'Smoker', 'On hypertension treatment', 'ASCVD 10 Y Risk Score', 'Age', 'Gender', 'Smoking', 'Systolic', 'Diabetes', 'CAD', 'CVD', 'AAA', 'PAD', 'Time since last diagnosis', 'HDL', 'Total cholesterol', 'eGFR', 'hsCRP', 'SMART 10 Y Risk Score', 'Unmet Risk']
    model = {}    
    for i in col_list_filter:
        # create dict friendly field labels based on each header item
        field_label = (headers[i]).lower().replace(' ', '-')
        # Compute basic stats of target col (e.g. ASCVD score) for each each 
        # independent variable (e.g. age) and their individual values.
        col = cols[i]
        groups, means, stds, keys = calc_vals(col, cols[target_col])
        maxstd = max(stds)
        nstds = []
        for std in stds:
            nstds.append(std/maxstd)
            model[field_label] = {}
            for j in range(len(nstds)):
                model[field_label].update({keys[j]: nstds[j]})
    return model


def normalized_confidence(model_weights, race, gender, age, systolic, total_cholesterol, hdl, diabetes, smoker, hypertension):
    '''
    Calculate the Normalized Confidence score based on model_weights created by: 
        def nc_model_weights(cols, col_list, target_col)
    '''
    
    def get_closest_key(keys, val):
        '''
        Get the closest value key to the input val
        '''
        diff = 0.0
        return_key = list(keys)[0]
        for key in keys:
            if abs(key - val) == 0:
                diff = 1.0
                return_key = key
            elif 1 / abs(key - val) > diff:
                diff = 1 / abs(key - val)
                return_key = key
        # print('val', val, 'key', return_key)
        return return_key

    # Get the normalized Standard Deviations for each variable (NSTD)
    r_nstd = model_weights['race'][race]
    g_nstd = model_weights['gender'][gender]

    age = get_closest_key(model_weights['age'].keys(), age)
    a_nstd = model_weights['age'][age]

    systolic = get_closest_key(model_weights['systolic'].keys(), systolic)
    sy_nstd = model_weights['systolic'][systolic]

    total_cholesterol = get_closest_key(model_weights['total-cholesterol'].keys(), total_cholesterol)
    t_nstd = model_weights['total-cholesterol'][total_cholesterol]

    hdl = get_closest_key(model_weights['hdl'].keys(), hdl)
    hd_nstd = model_weights['hdl'][hdl]

    d_nstd = model_weights['diabetes'][diabetes]
    sm_nstd = model_weights['smoker'][smoker]
    hy_nstd = model_weights['on-hypertension-treatment'][hypertension]

    # Subtract from 1 to get positive confidence score.
    norm_conf = 1.0 - (r_nstd * g_nstd * a_nstd * sy_nstd * t_nstd * hd_nstd * d_nstd * sm_nstd * hy_nstd)
    return norm_conf

def bar_plot_within_group(cols, i, j, cols2=[]):
    '''
    Compare counts between two lists in a given group.
    e.g. 'male' versus 'female'
    '''
    headers = ['Race', 'Gender', 'Age', 'Systolic', 'Total Cholesterol', 'HDL', 'Diabetes', 'Smoker', 'On hypertension treatment', 'ASCVD 10 Y Risk Score', 'Age', 'Gender', 'Smoking', 'Systolic', 'Diabetes', 'CAD', 'CVD', 'AAA', 'PAD', 'Time since last diagnosis', 'HDL', 'Total cholesterol', 'eGFR', 'hsCRP', 'SMART 10 Y Risk Score', 'Unmet Risk']
    x = cols[i]
    y = cols[j]
    x_label = headers[i]
    y_label = headers[j]

    # Create blue bars
    groups1, bars1, yerr1, keys1 = calc_vals(x, y)
    barWidth = 0.3
    r1 = np.arange(len(bars1))
    plt.errorbar(r1, bars1, yerr=yerr1, marker='s', mfc='red', mec='red', ms=5, mew=5, linestyle='--', elinewidth=1, ecolor='black')

    if len(cols2) > 0:
        r2 = [x + barWidth for x in r1]
        groups2, bars2, yerr2 = calc_vals(cols2[i], cols2[j])
        plt.bar(r2, bars2, width = barWidth, color = 'blue', edgecolor = 'black', yerr=yerr2, capsize=7, label='B')

    # Plot it
    plt.xticks([r for r in range(len(bars1))], list(groups1.keys()))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def std_risk_increasing(cols):
    ''' 
    Group and plot the stdandard deviation of a risk model (e.g. ASCVD) 
    as the risk score increase from 0 to 1 by increments of 0.001.
    '''
    scol = sorted(cols[9]) 
    groups = {}
    inc = 0.001
    lastinc = round(inc, 3)
    for i in range(len(scol)):
        val = scol[i]
        if val <= lastinc:
            if lastinc in groups.keys():
                groups[lastinc].append(val)
            else:
                groups[lastinc] = [val]
        else:
            lastinc += inc
            lastinc = round(lastinc, 3)
            groups[lastinc] = [val]
    group_sizes = []
    group_stds = []
    for group in groups:
        group_sizes.append(len(groups[group]))
        group_stds.append(np.std(groups[group]))
    scores = list(groups.keys())

    ''' Plot standard deviation of risk model (e.g. ASCVD) scores as scores increase'''
    plt.plot(scores, group_stds, 'b.')
    plt.xlabel('Risk Model Score', fontsize=12)
    plt.ylabel('STD of Risk Model Score', fontsize=12)
