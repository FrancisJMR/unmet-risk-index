'''
This code generates the UMRI risk score from ASCVD and SMART risk scores and
generate a CSV file with all inputs and scores for all 26,880,000 profile combinations.

Example use from command line: 
> python generate-umri-profiles.py
Output: 'umri_profiles.csv'
'''

import csv
import itertools
import datetime

# Import ASCVD and SMART calculators
from ascvd import ascvd # From https://tools.acc.org/ASCVD-Risk-Estimator-Plus/#!/calculate/estimate/
from smart import smart # From https://www.escardio.org/Education/ESC-Prevention-of-CVD-Programme/Risk-assessment/SMART-Risk-Score

# Define risk calculator input values
age         = range(40, 80)
gender      = ['female', 'male']
race        = ['african', 'other']
systolic    = range(90, 201, 10)
cholesterol = [4.0, 5.0, 6.0, 7.0, 8.0] # in mmol/L
hdl         = [0.6, 1, 1.5, 2, 2.5] # in mmol/L
diabetes    = ['yes', 'no']
smoker      = ['current', 'no']
cad         = ['yes'] # Coronary Arterry Disease
cvd         = ['no']  # Cerebrocascular disease
aaa         = ['no']  # Abdominal aortic aneurism
pad         = ['no']  # Peripheral artery disease
tsld        = [0] # Time since last diagnosis
egfr        = [60, 70, 80, 90, 100, 110, 120] # Estimated GFR: filtration rate for assessment of renal/kidney function.
hscrp       = [0.1, 0.2, 0.6, 1, 3, 6, 8, 11, 13, 15] # high sensitivity C-reactive protein (inflamation test)  < 10mg/L is normal
hyper       = ['yes', 'no']     # Hypertension treament

# Output csv file to store the data rows
file_name = 'umri_profiles.csv'

def generate_umri_profiles():
    starttime = datetime.datetime.now()
    total = 0
    for xs in itertools.product(age, gender, race, systolic, cholesterol, hdl, diabetes, smoker, cad, cvd, aaa, pad, tsld, egfr, hscrp, hyper):
        total += 1
    print('total cases:', total)

    # Write the header row
    headers = ['race', 'gender', 'age', 'systolic', 'total_cholesterol', 'hdl', 'diabetes_history', 'smoker', 'on_hypertension_treatment', 'ASCVD 10 Y Risk Score', 'age', 'gender', 'smoking', 'systolic', 'diabetes', 'CAD', 'CVD', 'AAA', 'PAD', 'tsld', 'hdl', 'total_chol', 'eGFR', 'hsCRP', 'SMART 10 Y Risk Score', 'Unmet Risk']
    with open(file_name, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(headers)
    
    # Generate each data row
    count = 0
    for xs in itertools.product(age, gender, race, systolic, cholesterol, hdl, diabetes, smoker, cad, cvd, aaa, pad, tsld, egfr, hscrp, hyper):

        age_val         = xs[0]
        gender_val      = xs[1]
        race_val        = xs[2]
        systolic_val    = xs[3]
        cholesterol_val = xs[4]
        hdl_val         = xs[5]
        diabetes_val    = xs[6]
        smoker_val      = xs[7]
        cad_val         = xs[8]
        cvd_val         = xs[9]
        aaa_val         = xs[10]
        pad_val         = xs[11]
        tsld_val        = xs[12]
        egfr_val        = xs[13]
        hscrp_val       = xs[14]
        hyper_val       = xs[15]

        # Generate ASCVD scores
        pre_mi_risk10 = ascvd(race_val, gender_val, age_val, systolic_val, cholesterol_val, hdl_val, diabetes_val, smoker_val, hyper_val)
        pre_mi_risk10_str = '{:.5f}'.format(pre_mi_risk10)
        
        # Create the row with ASCVD inputs and score
        row = [race_val, gender_val, age_val, systolic_val, cholesterol_val, hdl_val, diabetes_val, smoker_val, hyper_val, pre_mi_risk10_str]
        
        # Generate SMART scores
        post_mi_risk10 = smart(age_val, gender_val, smoker_val, systolic_val, diabetes_val, cad_val, cvd_val, aaa_val, pad_val, tsld_val, hdl_val, cholesterol_val, egfr_val, hscrp_val)
        post_mi_risk10_str = '{:.5f}'.format(post_mi_risk10)
        
        # Add SMART inputs and score to the row
        row += [age_val, gender_val, smoker_val, systolic_val, diabetes_val, cad_val, cvd_val, aaa_val, pad_val, tsld_val, hdl_val, cholesterol_val, egfr_val, hscrp_val, post_mi_risk10_str]

        # Calculate and add the UNMET RISK INDEX SCORE (UMRI)
        unmet_risk = post_mi_risk10/pre_mi_risk10
        unmet_risk_str = '{:.5f}'.format(unmet_risk)
        
        # Add UMRI to the end of the row
        row += [unmet_risk_str]

        # Add the row to the CSV file
        with open(file_name, 'a') as fp:
            writer = csv.writer(fp)
            writer.writerow(row)

        count += 1
        print (count, '/', total)

    endtime = datetime.datetime.now()
    print ('Count:', count, 'Total:', total)
    print ('Start Time:', starttime, 'End Time:', endtime)
    return True

if __name__ == '__main__':
    generate_umri_profiles()
