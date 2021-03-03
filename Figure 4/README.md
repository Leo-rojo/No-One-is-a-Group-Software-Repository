## Description
The input to the `nestedkfold.py` script is a .csv file which contains the individual scores and the average and variance of vmaf and sum of rebuffering_duration for each of the hdtv video (example file is already provided under the name `users_data_regression.csv`).

### Replicate the plots
run the command `python nestedkfold.py`. It will perform 15 round of the same experiments (there is a randomic shuffle of data that makes the results a bit variable, so it is possible to compare the results for each shuffle) 
and results will be added to Figure 4 folder. 

