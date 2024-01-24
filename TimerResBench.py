import subprocess
import re
import time
import ctypes
import psutil
from os import system

meilleure_moyenne = float('inf')

STR_executable = r"C:\bin\setup\STR.exe"
MeasureSleep_executable = r"C:\bin\setup\MeasureSleep.exe"

print(f"Ignore \"Resolution set to: x ms\" its wrong value.")
print(f"MAKE SURE TO CLOSE ALL APPLICATIONS BEFORE RUNNING THIS SCRIPT AND CLOSE YOUR ACTUAL TIMER RESOLUTION (SERVICE TOO).")
print(f"The process will be very very long, so please be patient.")
print()
wait = input("Press Enter to continue.")
def extraire_lignes_autour_avg(texte):
    matches = re.findall(r"Avg: (\d+(\.\d{1,4})?)", texte)
    if matches:
       
        ligne_avg = re.search(r"Avg:.*", texte)
        if ligne_avg:
            index_avg = texte.find(ligne_avg.group())
            debut = max(0, index_avg - 13) 
            fin = min(len(texte), index_avg + len(ligne_avg.group()) + 30)  
            lignes_autour_avg = texte[debut:fin].splitlines()
            return lignes_autour_avg
    return None

for resolution in range(5100, 4999, -1):
    
    for process in psutil.process_iter(['pid', 'name']):
        if "STR.exe" in process.info['name']:
            psutil.Process(process.info['pid']).terminate()
            print()
   
    time.sleep(1)

    print(f"Benchmarking... {resolution}/5000")
    str_process = subprocess.Popen([STR_executable, "--resolution", str(resolution)],subprocess.SW_HIDE, shell=True)                                   
    
    time.sleep(1)

    resultats = subprocess.check_output([MeasureSleep_executable, "--samples", "100"], universal_newlines=True)
    
    lignes_autour_avg = extraire_lignes_autour_avg(resultats)
    
    if lignes_autour_avg is not None:
        for ligne in lignes_autour_avg:
            print(ligne)  
            if "Avg:" in ligne:
                moyenne = float(re.search(r"Avg: (\d+(\.\d{1,4})?)", ligne).group(1))
                if moyenne < meilleure_moyenne:
                    meilleure_moyenne = moyenne
                    meilleure_resolution = resolution

    
    str_process.terminate()

if meilleure_moyenne == float('inf'):
    print("No valid averages were found.")
else:
    print()
    print(f"The best resolution is {meilleure_resolution} with a average of {meilleure_moyenne:.4f}")
    print()
    print(f"Made by @BIDOUNI on GitHub, or @KINGBOUDINI on Twitter.")
    print(f"You can reuse this script as long as you mention me.")
    print()
