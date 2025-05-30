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

def kubios_string(dic):
    list = []
    for key, value in dic.items():
        if isinstance(value, dict):
            list.append("") # Tyhjä rivi alidictien alkuun.
            list.append(key)
            sublist = kubios_string(value)
            for sub in sublist:
                list.append(sub)
        else:
            list.append(f"{key}: {value}")
    return list


print (kubios_string(response))