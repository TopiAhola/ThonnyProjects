import os
import ujson as json

def save_raw_data(kubios_data, ppi_list):
    base_path = "summary"

    # Luo hakemisto, jos puuttuu
    try:
        os.listdir(base_path)
    except OSError:
        try:
            os.mkdir(base_path)
            print("Created directory:", base_path)
        except Exception as e:
            print("Error creating directory:", e)
            return

    # Selvitä seuraava vapaa tiedostonumero
    files = os.listdir(base_path)
    next_index = 1
    for name in files:
        if name.startswith("raw_") and name.endswith(".json"):
            try:
                num = int(name[4:7])
                if num >= next_index:
                    next_index = num + 1
            except:
                pass

    # Luo tiedostonimi
    file_name = "raw_{:03d}.json".format(next_index)
    path = base_path + "/" + file_name

    # Tallennettava data
    data_to_save = {
        "response": kubios_data,
        "measurement": ppi_list
    }

    try:
        with open(path, "w") as f:
            json.dump(data_to_save, f)
        print("Saved file:", path)
    except Exception as e:
        print("Error saving file:", e)

def read_and_print_files():
    base_path = "summary"
    file_contents = []  # TEhdään lista

    try:
        files = os.listdir(base_path)
    except Exception as e:
        print("Directory not found:", e)
        return file_contents

    for name in files:
        full_path = base_path + "/" + name
        try:
            stat = os.stat(full_path)
            if not stat[0] & 0x4000:  # Varmistetaan ettei ole hakemisto
                with open(full_path, "r") as f:
                    content = f.read()
#                 print("File:", full_path)
#                 print(content)
#                 print("-" * 40)

                # Tallennetaan tiedoston  sanakirjana listaan
                file_contents.append(content)
        except Exception as e:
            print("Error with file", name, ":", e)

    return file_contents

if __name__ == "__main__":
    # esimerkkidata
    response = {
        'id': 123,
        'data': {
            'status': 'ok',
            'analysis': {
                'artefact': 100,
                'mean_rr_ms': 805,
                'rmssd_ms': 42.90517,
                'freq_domain': {
                    'LF_power_prc': 21.00563,
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
                    'LF_HF_power': 0.2730352
                },
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
                'analysis_segments': {
                    'analysis_length': [30],
                    'analysis_start': [0],
                    'noise_length': [16.1],
                    'noise_start': [0]
                },
                'sns_index': 1.767119
            }
        }
    }

    ppi = [828, 836, 852, 760, 800, 796, 856, 824, 808]

    save_raw_data(response, ppi)

    files_data = read_and_print_files()

    print("\nReturned data:", files_data)

    print(files_data)
    print(response['id'])  
    print(response['data']['analysis']['stress_index'])  

#     Returned data: ['{"response": {"id": 123, "data": {"analysis": {"pns_index": -0.3011305, "sns_index": 1.767119, "artefact": 100, "rmssd_ms": 42.90517, "version": "1.5.0", "freq_domain": {"LF_peak": 0.15, "tot_power": 836.9012, "LF_power": 175.7964, "LF_power_nu": 21.41622, "LF_power_prc": 21.00563, "VLF_power": 16.04525, "HF_power_prc": 76.93377, "HF_power_nu": 78.4376, "VLF_peak": 0.04, "HF_peak": 0.1966667, "VLF_power_prc": 1.917222, "HF_power": 643.8597, "LF_HF_power": 0.2730352}, "effective_time": 0, "mean_hr_bpm": 74.53416, "mean_rr_ms": 805, "readiness": 62.5, "type": "readiness", "sd1_ms": 31.17043, "stress_index": 18.45491, "artefact_level": "VERY LOW", "respiratory_rate": null, "physiological_age": 25, "effective_prc": 0, "sd2_ms": 31.7047, "create_timestamp": "2025-04-14T06:17:18.111239+00:00", "analysis_segments": {"analysis_length": [30], "analysis_start": [0], "noise_length": [16.1], "noise_start": [0]}, "sdnn_ms": 30.65533}, "status": "ok"}}, "data": [828, 836, 852, 760, 800, 796, 856, 824, 808]}', '{"response": {"id": 123, "data": {"analysis": {"pns_index": -0.3011305, "sns_index": 1.767119, "artefact": 100, "rmssd_ms": 42.90517, "version": "1.5.0", "freq_domain": {"LF_peak": 0.15, "tot_power": 836.9012, "LF_power": 175.7964, "LF_power_nu": 21.41622, "LF_power_prc": 21.00563, "VLF_power": 16.04525, "HF_power_prc": 76.93377, "HF_power_nu": 78.4376, "VLF_peak": 0.04, "HF_peak": 0.1966667, "VLF_power_prc": 1.917222, "HF_power": 643.8597, "LF_HF_power": 0.2730352}, "effective_time": 0, "mean_hr_bpm": 74.53416, "mean_rr_ms": 805, "readiness": 62.5, "type": "readiness", "sd1_ms": 31.17043, "stress_index": 18.45491, "artefact_level": "VERY LOW", "respiratory_rate": null, "physiological_age": 25, "effective_prc": 0, "sd2_ms": 31.7047, "create_timestamp": "2025-04-14T06:17:18.111239+00:00", "analysis_segments": {"analysis_length": [30], "analysis_start": [0], "noise_length": [16.1], "noise_start": [0]}, "sdnn_ms": 30.65533}, "status": "ok"}}, "data": [828, 836, 852, 760, 800, 796, 856, 824, 808]}',
#                 '{"response": {"id": 123, "data": {"analysis": {"pns_index": -0.3011305, "sns_index": 1.767119, "artefact": 100, "rmssd_ms": 42.90517, "version": "1.5.0", "freq_domain": {"LF_peak": 0.15, "tot_power": 836.9012, "LF_power": 175.7964, "LF_power_nu": 21.41622, "LF_power_prc": 21.00563, "VLF_power": 16.04525, "HF_power_prc": 76.93377, "HF_power_nu": 78.4376, "VLF_peak": 0.04, "HF_peak": 0.1966667, "VLF_power_prc": 1.917222, "HF_power": 643.8597, "LF_HF_power": 0.2730352}, "effective_time": 0, "mean_hr_bpm": 74.53416, "mean_rr_ms": 805, "readiness": 62.5, "type": "readiness", "sd1_ms": 31.17043, "stress_index": 18.45491, "artefact_level": "VERY LOW", "respiratory_rate": null, "physiological_age": 25, "effective_prc": 0, "sd2_ms": 31.7047, "create_timestamp": "2025-04-14T06:17:18.111239+00:00", "analysis_segments": {"analysis_length": [30], "analysis_start": [0], "noise_length": [16.1], "noise_start": [0]}, "sdnn_ms": 30.65533}, "status": "ok"}}, "data": [828, 836, 852, 760, 800, 796, 856, 824, 808]}', '{"response": {"id": 123, "data": {"analysis": {"pns_index": -0.3011305, "sns_index": 1.767119, "artefact": 100, "rmssd_ms": 42.90517, "version": "1.5.0", "freq_domain": {"LF_peak": 0.15, "tot_power": 836.9012, "LF_power": 175.7964, "LF_power_nu": 21.41622, "LF_power_prc": 21.00563, "VLF_power": 16.04525, "HF_power_prc": 76.93377, "HF_power_nu": 78.4376, "VLF_peak": 0.04, "HF_peak": 0.1966667, "VLF_power_prc": 1.917222, "HF_power": 643.8597, "LF_HF_power": 0.2730352}, "effective_time": 0, "mean_hr_bpm": 74.53416, "mean_rr_ms": 805, "readiness": 62.5, "type": "readiness", "sd1_ms": 31.17043, "stress_index": 18.45491, "artefact_level": "VERY LOW", "respiratory_rate": null, "physiological_age": 25, "effective_prc": 0, "sd2_ms": 31.7047, "create_timestamp": "2025-04-14T06:17:18.111239+00:00", "analysis_segments": {"analysis_length": [30], "analysis_start": [0], "noise_length": [16.1], "noise_start": [0]}, "sdnn_ms": 30.65533}, "status": "ok"}}, "data": [828, 836, 852, 760, 800, 796, 856, 824, 808]}',
#                 '{"response": {"id": 123, "data": {"analysis": {"pns_index": -0.3011305, "sns_index": 1.767119, "artefact": 100, "rmssd_ms": 42.90517, "version": "1.5.0", "freq_domain": {"LF_peak": 0.15, "tot_power": 836.9012, "LF_power": 175.7964, "LF_power_nu": 21.41622, "LF_power_prc": 21.00563, "VLF_power": 16.04525, "HF_power_prc": 76.93377, "HF_power_nu": 78.4376, "VLF_peak": 0.04, "HF_peak": 0.1966667, "VLF_power_prc": 1.917222, "HF_power": 643.8597, "LF_HF_power": 0.2730352}, "effective_time": 0, "mean_hr_bpm": 74.53416, "mean_rr_ms": 805, "readiness": 62.5, "type": "readiness", "sd1_ms": 31.17043, "stress_index": 18.45491, "artefact_level": "VERY LOW", "respiratory_rate": null, "physiological_age": 25, "effective_prc": 0, "sd2_ms": 31.7047, "create_timestamp": "2025-04-14T06:17:18.111239+00:00", "analysis_segments": {"analysis_length": [30], "analysis_start": [0], "noise_length": [16.1], "noise_start": [0]}, "sdnn_ms": 30.65533}, "status": "ok"}}, "data": [828, 836, 852, 760, 800, 796, 856, 824, 808]}', '{"response": {"id": 123, "data": {"analysis": {"pns_index": -0.3011305, "sns_index": 1.767119, "artefact": 100, "rmssd_ms": 42.90517, "version": "1.5.0", "freq_domain": {"LF_peak": 0.15, "tot_power": 836.9012, "LF_power": 175.7964, "LF_power_nu": 21.41622, "LF_power_prc": 21.00563, "VLF_power": 16.04525, "HF_power_prc": 76.93377, "HF_power_nu": 78.4376, "VLF_peak": 0.04, "HF_peak": 0.1966667, "VLF_power_prc": 1.917222, "HF_power": 643.8597, "LF_HF_power": 0.2730352}, "effective_time": 0, "mean_hr_bpm": 74.53416, "mean_rr_ms": 805, "readiness": 62.5, "type": "readiness", "sd1_ms": 31.17043, "stress_index": 18.45491, "artefact_level": "VERY LOW", "respiratory_rate": null, "physiological_age": 25, "effective_prc": 0, "sd2_ms": 31.7047, "create_timestamp": "2025-04-14T06:17:18.111239+00:00", "analysis_segments": {"analysis_length": [30], "analysis_start": [0], "noise_length": [16.1], "noise_start": [0]}, "sdnn_ms": 30.65533}, "status": "ok"}}, "data": [828, 836, 852, 760, 800, 796, 856, 824, 808]}']
