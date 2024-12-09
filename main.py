#!/usr/bin/python3

import subprocess
import time
import json
import sys
import os

aliases = [
    ['-d', '--databases'],   # Specify databases
    ['-v', '--verbose'],   # Show more information
    ['-g', '--goal'],   # Specify value to search for
    ['-a', '--all'],   # Go through all databases
    ['-l', '--list'],   # List all available databases
    ['-t', '--no-time'],   # Do not measure time of execution
    ['-h', '--help']   # Show help
]

class dbmg:
    def __init__(self):
        self.CONFIGURATION = json.load(open('db-magnifier-glass.conf'))
        #self.check_mount_point()
        self.process_command()

    def check_mount_point(self):
        mounted_partitions = subprocess.run('df', shell=True, capture_output=True, text=True).stdout.split('\n')
        for partition in mounted_partitions:
            if self.CONFIGURATION['mount_point'][0] in partition and self.CONFIGURATION['mount_point'][1] in partition:
                print('Mount point found')
                return
        print('Mount point not found')
    
    def search_databases(self, command_options):
        general_start = time.time()

        for database in command_options['databases']:
            
            individual_start = time.time()
            print(f'Searching in {database}...', end=('\n' if command_options['verbose'] else '\r'))
            command = f'grep -H -r -n -b -o "{command_options["target"]}" "{self.CONFIGURATION["mount_point"][1]}/{database}"'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            for hit in result.stdout.split('\n'):
                if hit != '':
                    with open(hit.split(':')[0], 'rb') as file:
                        file.seek(int(hit.split(':')[2])-300)
                        hit_before = file.read(300).decode('utf-8', errors='replace')
                        hit_before = hit_before[::-1][:hit_before.find('\n')][::-1]
                        hit_after = file.read(300).decode('utf-8', errors='replace')
                        hit_context = hit_before + hit_after[:hit_after.find("\n")].replace(command_options['target'], f'\033[31;1m{command_options["target"]}\033[0m')

                    print(f'\033[0m{hit.split(":")[0]}:\033[33m{hit.split(":")[1]}\033[0m:\033[32m{hit.split(":")[2]}\033[0m:{hit_context}')
            
            if command_options['time']:
                print(f'{database} search time: {round(float(time.time()-individual_start), 3)}s')

        if command_options['time']:
            print(f'General search time: {round(float(time.time()-general_start), 3)}s')

    def process_command(self):
        command_options = {
            'databases': [],
            'verbose': False,
            'time': True,
            'target': ''
        }
        
        for arg in sys.argv[1:]:
            if arg == '-h' or arg == '--help':
                self.show_help()
                return
            if arg == '-l' or arg == '--list':
                os.system('ls ' + self.CONFIGURATION['mount_point'][1])
                return
            if arg == '-a' or arg == '--all':
                command_options['databases'] = os.listdir(self.CONFIGURATION['mount_point'][1])
            elif arg.startswith('--databases'):
                command_options['databases'] = arg.split('=')[1].split(',')
            if arg == '-v' or arg == '--verbose':
                command_options['verbose'] = True
            if arg.startswith('--target'):
                command_options['target'] = arg.split('=')[1]
            if arg == '-t' or arg == '--no-time':
                command_options['time'] = False

        if command_options['databases'] == []:
            print('Specify databases with --databases or search all with --all')
            return
        if command_options['target'] == '':
            print('Specify a value to look for with --target')
            return
        
        self.search_databases(command_options)
            

        





if __name__ == '__main__':
    dbmg()