import subprocess
import time

def get_battery_percentage():
    command = "upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep percentage | awk '{print $2}'"
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    percentage = int(output.strip().replace("%", ""))
    return percentage

def get_power_consumption():
    command = "upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep energy-rate | awk '{print $2}'"
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    power_consumption = float(output.strip().replace("W", ""))
    return power_consumption

def get_process_power_consumption():
    command = "upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -A 10 'time to empty' | grep -v 'time to empty' | grep -v 'percentage' | grep -v 'energy-rate' | awk '{$1=$1};1'"
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    processes = output.strip().split("\n")
    process_power_consumption = {}
    for process in processes:
        process_name, process_consumption = process.split(":")
        process_power_consumption[process_name.strip()] = float(process_consumption.strip().replace("W", ""))
    return process_power_consumption

def main():
    battery_percentage = get_battery_percentage()
    power_consumption = get_power_consumption()
    process_power_consumption = get_process_power_consumption()

    print("Battery Percentage:", battery_percentage)
    print("Power Consumption:", power_consumption, "W")
    print("Process Power Consumption:")
    for process, consumption in process_power_consumption.items():
        print(process + ":", consumption, "W")

    remaining_time = battery_percentage / power_consumption
    print("Estimated time remaining:", remaining_time, "hours")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)  # Обновление информации каждую минуту