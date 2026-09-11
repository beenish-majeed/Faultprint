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


def collect_system_data(areas):
    system_data = {}

    if "CPU" in areas:
        system_data["CPU"] = get_cpu_info()

    if "RAM" in areas:
        system_data["Memory"] = get_memory_info()

    if "Disk" in areas:
        system_data["Disk"] = get_disk_info()

    if "Processes" in areas:
        system_data["Top Processes"] = get_process_info()

    if "Battery" in areas:
        system_data["Battery"] = get_battery_info()

    if "Network" in areas:
        system_data["Network"] = get_network_info()

    if "Boot" in areas:
        system_data["Boot"] = get_boot_info()

    if "Disk Partitions" in areas:
        system_data["Disk Partitions"] = get_disk_partitions()

    if "Temperature" in areas:
        system_data["Temperature"] = get_temperature_info()

    return system_data


def display_system_data(data):
    print("              COMPUTER HEALTH REPORT")
    print("_" * 55)

    for category, information in data.items():
        print(f"\n[{category}]")

        if isinstance(information, list):
            for item in information:
                print(f"  {item}")
        else:
            for key, value in information.items():
                print(f"  {key}: {value}")

    print("\n" + "_" * 55)


if __name__ == "__main__":
    areas = ["CPU", "RAM", "Processes"]
    data = collect_system_data(areas)
    display_system_data(data)