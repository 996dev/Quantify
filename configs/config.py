from iniconfig import IniConfig

ini = IniConfig('../config_test.ini')

db_host = ini.get('Database', 'host')

print(f"Database host {db_host}")
db_host_1 = ini['Database']['host']
print(f"Database host {db_host_1}")

for key in ini.sections:
    print(f"sections key={key} keys={list(ini[key])}")
    for value in list(ini[key]):
        print(f"sections key={key} {value}={ini[key][value]}")

class Configs(object):
    def init_config(self):
        ini = IniConfig('../config_test.ini')
        db_host = ini.get('Database', 'host')
