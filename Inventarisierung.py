import psutil
import platform
import cpuinfo
import shutil
import logging
import datetime
############################################## Strings ##############################################
drive_not_found = "Laufwerk nicht gefunden:"
Gigabyte = "GB"
############################################## Variablen ##############################################
pc_name = ""
############################################## Funktionen ##############################################
def get_time():
    current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S ")
    return current_time
def get_pc_name():
    pc_name = platform.node()
    return pc_name
def get_cpu_name():
    cpu_name = cpuinfo.get_cpu_info()['brand_raw']
    return cpu_name
def get_memory_size():
    memory_size = psutil.virtual_memory().total
    memory_size = memory_size / 1024 / 1024 / 1024
    memory_size = round(memory_size, 2)
    return str(memory_size) + Gigabyte
def get_free_space(Path):
    try:
        total, used, free = shutil.disk_usage(Path + ":\\")
        print("##############################################")
        print("Laufwerk: %s" % Path)
        print("Total: %d GiB" % (total // (2 ** 30)))
        print("Used: %d GiB" % (used // (2 ** 30)))
        print("Free: %d GiB" % (free // (2 ** 30)))
    except:
        logging.error(msg=get_time() + drive_not_found + Path)

if __name__ == '__main__':
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)


#for i in range(65, 91):
    #get_free_space(chr(i))