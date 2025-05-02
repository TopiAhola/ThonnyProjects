import math

test_measurement = { "id": 666,
              "type": "PPI",
                "data": [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 812, 756, 820, 812, 800],
                "analysis": { "type": "readiness" } }




def hrv_analysis(ppi_list):
    #Mean Heart Rate
    mean_hr = math.floor((len(ppi_list)) / (sum(ppi_list)/60000))
    
    #Mean peak-peak interval
    mean_ppi = math.floor(sum(ppi_list) / len(ppi_list))
    
    #Root mean square of successive differences (RMSSD):
    ppi_diff_squares = []
    for index in range(1,len(ppi_list)):
        ppi_diff = ppi_list[index] - ppi_list[index-1]
        ppi_diff_squares.append(ppi_diff**2)
    mean_ppi_diff_squares = sum(ppi_diff_squares)/len(ppi_diff_squares)
    rmssd = math.sqrt(mean_ppi_diff_squares)
    
    #standard deviation of ppi:
    ppi_mean_diff_squares = []
    for index in range(1,len(ppi_list)):
        ppi_mean_diff_squares.append((ppi_list[index]-mean_ppi)**2)
    average = sum(ppi_mean_diff_squares)/(len(ppi_mean_diff_squares))
    sdnn = math.sqrt(average) 
    
    return mean_hr,mean_ppi,rmssd,sdnn


mean_hr,mean_ppi,rmssd,sdnn = hrv_analysis(test_measurement["data"])
print(mean_hr,mean_ppi,rmssd,sdnn)



#Halutut arvot:
# mean PPI 		581
# mean HR   	103
# RMSSD 38.29
# SDNN 36.91


#Oikeat arvot:
'''
response = {'id': 123,
 'data': {'status': 'ok',
          'analysis': {'artefact': 100,
                       'mean_rr_ms': 805,
                       'rmssd_ms': 42.90517,
                       'freq_domain': {'LF_power_prc': 21.00563,
                                       'tot_power': 836.9012,
                                       'HF_peak': 0.1966667,
                                       'LF_power_nu': 21.41622,
                                       'VLF_power': 16.04525,
                                       'LF_peak': 0.15,
                                       'LF_power': 175.7964,
                                       'HF_power_nu': 78.4376,
                                       'VLF_power_prc': 1.917222,
                                       'HF_power': 643.8597,
                                       'HF_power_prc': 76.93377,
                                       'VLF_peak': 0.04,
                                       'LF_HF_power': 0.2730352},
                       'stress_index': 18.45491,
                       'type': 'readiness',
                       'mean_hr_bpm': 74.53416,
                       'version': '1.5.0',
                       'physiological_age': 25,
                       'effective_time': 0,
                       'readiness': 62.5,
                       'pns_index': -0.3011305,
                       'sdnn_ms': 30.65533,
                       'artefact_level': 'VERY LOW',
                       'sd1_ms': 31.17043,
                       'effective_prc': 0,
                       'sd2_ms': 31.7047,
                       'respiratory_rate': None,
                       'create_timestamp': '2025-04-14T06:17:18.111239+00:00',
                       'analysis_segments': {'analysis_length': [30],
                                             'analysis_start': [0],
                                             'noise_length': [16.1],
                                             'noise_start': [0]}, 
                                             'sns_index': 1.767119}}}
                                             
                    '''