import psutil
from datetime import datetime
from psutil._common import bytes2human
from userge import userge, Message


async def generate_sysinfo(workdir):
    # uptime
    info = {
        'BOOT': (datetime.fromtimestamp(psutil.boot_time())
                 .strftime("%Y-%m-%d %H:%M:%S"))
    }
    # CPU
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)}MHz"
    info['CPU'] = (
        f"{psutil.cpu_percent(interval=1)}% "
        f"({psutil.cpu_count()}) "
        f"{cpu_freq}"
    )
    # Memory
    vm = psutil.virtual_memory()
    sm = psutil.swap_memory()
    info['RAM'] = (f"{bytes2human(vm.total)}, "
                   f"{bytes2human(vm.available)} available")
    info['SWAP'] = f"{bytes2human(sm.total)}, {sm.percent}%"
    # Disks
    du = psutil.disk_usage(workdir)
    dio = psutil.disk_io_counters()
    info['DISK'] = (f"{bytes2human(du.used)} / {bytes2human(du.total)} "
                    f"({du.percent}%)")
    if dio:
        info['DISK I/O'] = (f"R {bytes2human(dio.read_bytes)} | W {bytes2human(dio.write_bytes)}")
    # Network
    nio = psutil.net_io_counters()
    info['NET I/O'] = (f"TX {bytes2human(nio.bytes_sent)} | RX {bytes2human(nio.bytes_recv)}")
    # Sensors
    sensors_temperatures = psutil.sensors_temperatures()
    if sensors_temperatures:
        temperatures_list = [
            x.current
            for x in sensors_temperatures['coretemp']
        ]
        temperatures = sum(temperatures_list) / len(temperatures_list)
        info['TEMP'] = f"{temperatures}\u00b0C"
    info = {f"{key}:": value for (key, value) in info.items()}
    max_len = max(len(x) for x in info)
    return ("```"
            + "\n".join([f"{x:<{max_len}} {y}" for x, y in info.items()])
            + "```")


@userge.on_cmd("sysinfo", about="Get system info of your host machine.")
async def get_sysinfo(message: Message):
    await message.edit("Getting system information ...")
    response = await generate_sysinfo(userge.workdir)
    await message.edit("<u>**System Information**</u>:\n" + response)
