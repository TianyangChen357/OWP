This repository is to automate reteriving the data from NOAA Atlas 15 Pilot developed by NOAA Office of Water Prediction (OWP).

Link to NOAA Atalas 15 Pilot web app:
 https://water.noaa.gov/precip-frequency/atlas15/pilot 

To run the code for demo, simply run OWP.py as follows:	**python OWP.py <resolution_for_grid_sampling> <Global_Temerature_Index>**

This example shows that resolution is 200KM and GTI is 5 degree C: **python OWP.py 200 5**
  
Directory:
1. OWP.py: the main script to automatically derive preciptation values for Montana with a user specified-resolution under user-specified configuration.
2. generate_points.py: A script to generate coordinates in Montana
3. precipitation_results_1d.csv: A demonstration of the output.

Python Dependencies:
1.	pandas
2.	tqdm
3.	playwright
