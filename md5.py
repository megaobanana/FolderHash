# -- coding: utf-8 --
import os
import time
import sys
import traceback
from hashlib import md5
import unicodedata


def general_md5(target):
    def output_length_crop(src_str: str) -> str:
        max_length = int(os.get_terminal_size().columns / 2)
        real_length = 0
        for i in src_str:
            if unicodedata.east_asian_width(i) in ('F', 'W', 'A'):
                real_length += 2
            else:
                real_length += 1
        if real_length == max_length:
            return src_str
        elif real_length < max_length:
            return (" " * (max_length - real_length)) + src_str
        else:
            length = 0
            index = 0
            for i in range(len(src_str) - 1, -1, -1):
                if unicodedata.east_asian_width(src_str[i]) in ('F', 'W', 'A'):
                    length += 2
                else:
                    length += 1
                if length < max_length - 1:
                    index += 1
            return ".." + src_str[-index:]

    print("⌛ Counting Overall Size ...")
    total_bytes = CountSize(target).run()
    print("💾 Total Size: {0} MiB".format(total_bytes / 1048576))
    processed_bytes = 0
    processed_bytes_last = 0
    process_time_last = time.perf_counter()
    md5_hash = md5()
    overall_md5 = ""

    print("⚙️ Initializing MD5 Calculator")
    if os.path.isfile(target):
        src_file = target
        # =========计算哈希=========
        with open(src_file, "rb") as f1:
            filename_cropped = output_length_crop(src_file)
            current_file_size = os.path.getsize(src_file)
            current_file_processed_bytes = 0
            for byte_block in iter(lambda: f1.read(4096), b""):
                processed_bytes += len(byte_block)
                current_file_processed_bytes += len(byte_block)
                if (processed_bytes - processed_bytes_last) > 10485760 or (current_file_processed_bytes == current_file_size):
                    delta_time = time.perf_counter() - process_time_last
                    progress = processed_bytes / total_bytes * 100
                    progress_current = current_file_processed_bytes / current_file_size * 100
                    speed = ((processed_bytes - processed_bytes_last) / 1048576) / delta_time
                    processed_bytes_last = processed_bytes
                    process_time_last = time.perf_counter()
                    print("\033[1K", end="")
                    print("\033[0G", end="")
                    print("{0} -- {1}% | Overall -- {2}% | Speed -- {3}MiB/s".format(filename_cropped, format(progress_current, '.3f'), format(progress, '.3f'), format(speed, '.3f')), end="")
                    sys.stdout.flush()
                md5_hash.update(byte_block)
        overall_md5 = md5_hash.hexdigest()
        print()
    elif os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            for file in files:
                src_file = os.path.join(root, file)
                # =========计算哈希=========
                with open(src_file, "rb") as f1:
                    filename_cropped = output_length_crop(src_file)
                    current_file_size = os.path.getsize(src_file)
                    current_file_processed_bytes = 0
                    for byte_block in iter(lambda: f1.read(4096), b""):
                        processed_bytes += len(byte_block)
                        current_file_processed_bytes += len(byte_block)
                        if (processed_bytes - processed_bytes_last) > 10485760 or (current_file_processed_bytes == current_file_size):
                            delta_time = time.perf_counter() - process_time_last
                            progress = processed_bytes / total_bytes * 100
                            progress_current = current_file_processed_bytes / current_file_size * 100
                            speed = ((processed_bytes - processed_bytes_last) / 1048576) / delta_time
                            processed_bytes_last = processed_bytes
                            process_time_last = time.perf_counter()
                            print("\033[1K", end="")
                            print("\033[0G", end="")
                            print("{0} -- {1}% | Overall -- {2}% | Speed -- {3}MiB/s".format(filename_cropped, format(progress_current, '.3f'), format(progress, '.3f'), format(speed, '.3f')), end="")
                            sys.stdout.flush()
                        md5_hash.update(byte_block)
        overall_md5 = md5_hash.hexdigest()
        print()

    print("🧾 Calculated MD5: {0}".format(overall_md5))
    return overall_md5


class CountSize:  # 统计文件大小
    def __init__(self, directory):
        self.root = directory
        self.Num = 0

    def countfile(self, path):
        if not os.path.isdir(path):
            return
        file_list = os.listdir(path)
        for file_name in file_list:
            file_name = os.path.join(path, file_name)
            if os.path.isdir(file_name):
                self.countfile(file_name)
            else:
                self.Num += os.path.getsize(file_name)

    def run(self):
        if os.path.isfile(self.root):
            return os.path.getsize(self.root)
        elif os.path.isdir(self.root):
            self.countfile(self.root)
        return self.Num


def print_headline(title):
    print("." * int((os.get_terminal_size().columns -
                     len(title)) / 2) +
          title + "." *
          (os.get_terminal_size().columns - len(title) -
           int((os.get_terminal_size().columns -
                len(title)) / 2)))


if __name__ == "__main__":
    print("💡 Hint: In win 11, you can use [Ctrl+Shift+C] to copy the path of an file/directory")
    print("💡 Hint: this script can automatically crop the quotes and blank spaces in your inputed path")
    print(r"""💡 Hint: Use [ New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" ` -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force ] to disable path limit""")
    print("-" * os.get_terminal_size().columns)
    startup_arg_files = sys.argv[1:]
    if len(startup_arg_files) == 1:
        print("📃 object 1 path: {0}".format(startup_arg_files[0]))
        Target1 = startup_arg_files[0]
        Target2 = input("⌨️ Please input the (absolute) path of compare object2 (press enter to skip): ").strip(' "\'\t\n\r')
    else:
        Target1 = input("⌨️ Please input the (absolute) path of compare object1: ").strip(' "\'\t\n\r')
        Target2 = input("⌨️ Please input the (absolute) path of compare object2 (press enter to skip): ").strip(' "\'\t\n\r')
    try:
        if Target2 == "":
            general_md5(Target1)
        else:
            print_headline("Processing target 1")
            MD5_1 = general_md5(Target1)
            print_headline("Processing target 2")
            MD5_2 = general_md5(Target2)
            print("-" * os.get_terminal_size().columns)
            if MD5_1 == MD5_2:
                print(r"""
  _____ __ __    __    __    ___  _____ _____ __ 
 / ___/|  |  |  /  ]  /  ]  /  _]/ ___// ___/|  |
(   \_ |  |  | /  /  /  /  /  [_(   \_(   \_ |  |
 \__  ||  |  |/  /  /  /  |    _]\__  |\__  ||__|
 /  \ ||  :  /   \_/   \_ |   [_ /  \ |/  \ | __ 
 \    ||     \     \     ||     |\    |\    ||  |
  \___| \__,_|\____|\____||_____| \___| \___||__|
                                                 
""")
            else:
                print(r"""
   ___  ____   ____   ___   ____   __ 
  /  _]|    \ |    \ /   \ |    \ |  |
 /  [_ |  D  )|  D  )     ||  D  )|  |
|    _]|    / |    /|  O  ||    / |__|
|   [_ |    \ |    \|     ||    \  __ 
|     ||  .  \|  .  \     ||  .  \|  |
|_____||__|\_||__|\_|\___/ |__|\_||__|
                                      
""")
    except:
        traceback.print_exc(file=sys.stdout)
    input("press enter to exit")
