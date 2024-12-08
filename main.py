#!/usr/bin/python3

import subprocess
import time
import json
import sys


class dbmg:
    def __init__(self):
        self.CONFIGURATION = json.load(open("db-magnifier-glass.conf"))
        #self.check_mount_point()
        print(sys.argv)

    def check_mount_point(self):
        mounted_partitions = subprocess.run('df', shell=True, capture_output=True, text=True).stdout.split('\n')
        for partition in mounted_partitions:
            if self.CONFIGURATION['mount_point'][0] in partition and self.CONFIGURATION['mount_point'][1] in partition:
                print("Mount point found")
                return
        print("Mount point not found")
    





if __name__ == "__main__":
    dbmg()





input()


file_path = sys.argv[1]
pattern = sys.argv[2]

command = f'grep -n -b -o "{pattern}" "{file_path}"'
result = subprocess.run(command, shell=True, capture_output=True, text=True)

if result.stdout:
    #byte_offsets = [int(line.split(':')) for line in result.stdout.splitlines()]
    print("Byte offsets:", result.stdout)
else:
    print("No matches found.")

with open(file_path, "rb") as file:
    for offset in byte_offsets:
        file.seek(offset-50)
        snippet = file.read(100)
        print("Match at offset", offset, ":", snippet.decode(errors="replace"))