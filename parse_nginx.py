import csv
import re

source = './nginx.log'
output = './nginx_log.csv'

regex = re.compile(r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<date>.*)  \"(?P<method>.*) (?P<path>.*) H')

with open(source) as file:
    with open(output, 'w', newline='') as csv_file:
        write_to_csv = csv.writer(csv_file, delimiter=',')
        for index, line in enumerate(file):
            res = regex.search(line)
            if res is not None:
                res = res.groupdict()
                ip = res['ip']
                date = res['date']
                method = res['method']
                path = res['path']
                write_to_csv.writerow([ip, date, method, path])
