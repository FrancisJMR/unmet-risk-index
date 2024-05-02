# Unmet Risk Index - Code Repository

This is the code repository for the Unmet Risk Index research work.

The unmet risk index (UMRI) is the secondary risk adjusted to the baseline risk, or the SMART score by the ASCVD score. 
This work demonstrates that the creation of synthetic cohorts from medical risk calculators can be used to provide insights into the correlation between risk estimations, clinical reasoning, data driven subgrouping, and risk calculator score confidence estimation. 
The existence of non-uniformly distributed prediction variables in iteration-derived synthetic cohort can be used for clustering, revealing natural groupings that can provide a different understanding of cohort behavior. 
The variability in prediction confidence among the calculators was shown to depend on patient attributes, suggesting the potential value of including a "normalized confidence" score in future calculator versions for clinicians. 
This concept will be explored further in subsequent research.

## Code

"generate-umri-profiles.py": Generate Unmet Risk Index profiles. You will need to create your own ASCVD and SMART risk score generators based on the code and documentation available:

- ASCVD @ https://tools.acc.org/ASCVD-Risk-Estimator-Plus/#!/calculate/estimate/
  - Model coefficients are available in the following publication: https://doi.org/10.1161/01.cir.0000437741.48606.98
- SMART @ https://www.escardio.org/Education/ESC-Prevention-of-CVD-Programme/Risk-assessment/SMART-Risk-Score
  - Model coefficients are available in the following publication: https://doi.org/10.1136/heartjnl-2013-303640

"clustering.py": Compute the clusters using KPrototypes and plot them.

"confidence.py": Compute and plot the normalized confidence score, as well as compute and plot standard deviation of variables as risk scores increase.

## Data

ASCVD, SMART, and UMRI profiles generated for this work is available at https://doi.org/10.5281/zenodo.8241872

## Publication

The publication details related to this work will be updated here once available.

## Contributors
Francis Jeanson, PhD 1; Michael E. Farkouh, MD, MSc 2; Lucas C. Godoy, MD 2; Sa’ar Minha, MD 3; Oran Tzuman, MD 3; Gil Marcus, MD 3
1. Datadex Inc., Toronto, Ontario, Canada
2. Peter Munk Cardiac Centre and Heart and Stroke Richard Lewar Centre, University of Toronto, Toronto, Ontario, Canada
3. Department of Cardiology, Shamir Medical Center, Zeriffin, Israel; and Sackler School of Medicine, Tel-Aviv University, Ramat-Aviv, Israel.
