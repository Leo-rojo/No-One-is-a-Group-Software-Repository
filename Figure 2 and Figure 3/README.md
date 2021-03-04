## Description
`data_flow` folder is composed by:

 * MYKSQI folder: python [code](https://github.com/zduanmu/ksqi), with minimum modification in order to be runned in my set-up, that let you train and test various QoE models as described in the paper.

 * data folder: contains data processed through all the pipeline, results and plots 

 * dati_input_1.py: it takes as input the original dataset modified with individual vote for each user in the relative column (example of the file can be found inside datain folder) and 
   creates one file per each person where its individual scores are copyed and pasted into mos column (which is the input data for the original MYKSQI code)

 * run_models_2.py: it takes as input the generated files from the above script and then it run the already trained models (on [WaterlooII](https://github.com/zduanmu/ksqi/tree/master/data/WaterlooSQoE-II) and [WaterlooI](https://github.com/zduanmu/ksqi/tree/master/data/WaterlooSQoE-I) datasets) with 
   individual scores and the output is the performance and scores for each user

 * aggregate_result_3.py: it aggregates the results of each person inside the same file and then copy the results for the mos performances
   and calculate the differences between the individual performances and the mos ones.

 * plot_cdf_4.py: file used to plot the Figure 2 and Figure 3 of the paper


### Replicate the plots
* step 1 ("hdtv mos performance"):
	* put original dataset in `MYKSQI\data\WaterlooSQoE-IV` with only hdtv users info (example can be already found in the folder)
	* run the original code with command:
		* `python main.py --set DATASET WaterlooSQoE-IV INPUT_DIR data/WaterlooSQoE-IV MODEL FTW:Mok2011QoE:Liu2012QoE:Xue2014QoE:Yin2015QoE:Spiteri2016QoE:Bentaleb2016QoE:SQI:P1203:VideoATLAS:KSQI`

performance results will be in `MYKSQI\results\WaterlooSQoE-IV`. Copy the performance data in `data_flow\data\final_results.xlsx` from row 16 (example is already provided).

* step 2 ("individual and mos difference performance"):
	* run `python data_input_1.py` Results will be added to `data_flow\data\dataout`
	* run `python run_models_2.py` Results will be added to `data_flow\data\resultsmixture`
	* run `python aggregate_result_3.py` Results can be found in `data_flow\data\final_results_with_mos_and_difference.xlsx`
	* run `python plot_cdf_4.py` Plots can be found in `data_flow\data\plots`




