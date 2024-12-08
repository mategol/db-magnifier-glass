#!/usr/bin/python3

import subprocess
import time
import json
import sys


class dbmg:
    def __init__(self):
        self.CONFIGURATION = json.load(open("db-magnifier-glass.conf"))
        self.check_mount_point()
        

    def check_mount_point(self):
        mounted_partitions = subprocess.run('df', shell=True, capture_output=True, text=True).stdout.split('\n')
        print(mounted_partitions)
    





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