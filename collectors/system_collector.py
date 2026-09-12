import os
import psutil
from datetime import datetime


def get_cpu_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    physical_cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)

    frequency = psutil.cpu_freq()

    if frequency:
        current_frequency = round(frequency.current)
    else:
        current_frequency = "Unavailable"

    return {
        "Usage": f"{cpu_usage}%",
        "Physical Cores": physical_cores,
        "Logical Cores": logical_cores,
        "Current Frequency": f"{current_frequency} MHz",
    }


def get_memory_info():
    memory = psutil.virtual_memory()

    total_gb = memory.total / (1024 ** 3)
    used_gb = memory.used / (1024 ** 3)
    available_gb = memory.available / (1024 ** 3)

    return {
        "Total": f"{total_gb:.2f} GB",
        "Used": f"{used_gb:.2f} GB",
        "Available": f"{available_gb:.2f} GB",
        "Usage": f"{memory.percent}%",
    }


def get_disk_info():
    disk = psutil.disk_usage(os.path.abspath(os.sep))

    total_gb = disk.total / (1024 ** 3)
    used_gb = disk.used / (1024 ** 3)
    free_gb = disk.free / (1024 ** 3)

    return {
        "Total": f"{total_gb:.2f} GB",
        "Used": f"{used_gb:.2f} GB",
        "Free": f"{free_gb:.2f} GB",
        "Usage": f"{disk.percent}%",
    }


def get_process_info():
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_percent"]
    ):
        try:
            process_data = process.info

            processes.append({
                "PID": process_data["pid"],
                "Name": process_data["name"],
                "CPU": process_data["cpu_percent"],
                "Memory": round(process_data["memory_percent"], 2),
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes.sort(
        key=lambda process: process["Memory"] or 0,
        reverse=True
    )

    return processes[:10]


def get_battery_info():
    battery = psutil.sensors_battery()

    if battery is None:
        return {
            "Status": "Battery information unavailable"
        }

    battery_level = battery.percent

    if battery.power_plugged:
        status = "Charging"
    else:
        status = "Not Charging"

    return {
        "Level": f"{battery_level}%",
        "Status": status,
    }


def get_network_info():
    network = psutil.net_io_counters()

    sent_mb = network.bytes_sent / (1024 ** 2)
    received_mb = network.bytes_recv / (1024 ** 2)

    return {
        "Data Sent": f"{sent_mb:.2f} MB",
        "Data Received": f"{received_mb:.2f} MB",
    }


def get_boot_info():
    boot_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_timestamp)

    uptime = datetime.now() - boot_time
    uptime = str(uptime).split(".")[0]

    return {
        "Last Boot": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        "Uptime": uptime,
    }


def get_disk_partitions():
    partitions = []

    for partition in psutil.disk_partitions():
        try:
            disk = psutil.disk_usage(partition.mountpoint)

            free_gb = disk.free / (1024 ** 3)

            partitions.append({
                "Drive": partition.device,
                "Mount Point": partition.mountpoint,
                "Free": f"{free_gb:.2f} GB",
                "Usage": f"{disk.percent}%",
            })

        except (PermissionError, OSError):
            continue

    return partitions


def get_temperature_info():
    try:
        temperatures = psutil.sensors_temperatures()
    except AttributeError:
        return {
            "Status": "Temperature information unavailable"
        }

    if not temperatures:
        return {
            "Status": "Temperature information unavailable"
        }

    return temperatures


def collect_system_data(required_data):
    available_data = {
        "CPU information": get_cpu_info,
        "Memory information": get_memory_info,
        "Disk information": get_disk_info,
        "Running processes": get_process_info,
        "Battery information": get_battery_info,
        "Network information": get_network_info,
        "Boot and uptime information": get_boot_info,
        "Disk partition information": get_disk_partitions,
        "Temperature information": get_temperature_info,
    }

    system_data = {}

    for data_name in required_data:
        if data_name in available_data:
            system_data[data_name] = available_data[data_name]()

    return system_data

def display_system_data(data):
    print("\nSystem Data")

    for category, information in data.items():
        print(f"\n{category}")

        if category == "Running processes":
            for process in information:
                print(
                    f"  {process['Name']} — "
                    f"CPU: {process['CPU']}%, "
                    f"Memory: {process['Memory']}%"
                )

        elif isinstance(information, dict):
            for key, value in information.items():
                print(f"  {key}: {value}")

        else:
            print(f"  {information}")

if __name__ == "__main__":
    areas = ["CPU", "RAM", "Processes"]
    data = collect_system_data(areas)
    display_system_data(data)