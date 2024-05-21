import pandas as pd

path_to_data = 'C:/Users/Alexander/Desktop/bachelor/data/baseline_[CSV]'
model = ''
cpu_path1 = path_to_data + '/AMD Ryzen 9 3900X CCX #0 Utilization.csv'
cpu_path2 = path_to_data + '/AMD Ryzen 9 3900X CCX #1 Utilization.csv'
cpu_path3 = path_to_data + '/AMD Ryzen 9 3900X CCX #2 Utilization.csv'
cpu_path4 = path_to_data + '/AMD Ryzen 9 3900X CCX #3 Utilization.csv'
gpu_path = path_to_data + '/NVIDIA GeForce RTX 3060 GPU Utilization.csv'
mem_path = path_to_data + '/ASRock B550M-ITXac System Memory Utilization.csv'
baseline_compare_path = 'C:/Users/Alexander/Desktop/bachelor/data/baseline_compare.csv'

baseline_compare = pd.DataFrame()

def find_max_and_mean(file_path):
    file = pd.read_csv(file_path)
    max = file[file.columns[1]].max()
    avg = file[file.columns[1]].mean()
    return max, avg

def cpu_max_and_mean(cpu_path1, cpu_path2, cpu_path3, cpu_path4):
    cpumax1, cpuavg1 = find_max_and_mean(cpu_path1)
    cpumax2, cpuavg2 = find_max_and_mean(cpu_path2)
    cpumax3, cpuavg3 = find_max_and_mean(cpu_path3)
    cpumax4, cpuavg4 = find_max_and_mean(cpu_path4)
    cpumax = max(cpumax1, cpumax2, cpumax3, cpumax4)
    cpuavg = (cpuavg1 + cpuavg2 + cpuavg3 + cpuavg4)/4
    return cpumax, cpuavg

cpumax, cpuavg = cpu_max_and_mean(cpu_path1, cpu_path2, cpu_path3, cpu_path4)
gpumax, gpuavg = find_max_and_mean(gpu_path)
memmax, memavg = find_max_and_mean(mem_path)

baseline_line = {'cpu max': cpumax, 
              'cpu avg': cpuavg, 
              'gpu max': gpumax, 
              'gpu avg': gpuavg,
              'mem max': memmax,
              'mem avg': memavg,
               }

baseline_compare = pd.concat([baseline_compare, pd.DataFrame([baseline_line])], ignore_index=True)
baseline_compare.to_csv(baseline_compare_path, index=False)