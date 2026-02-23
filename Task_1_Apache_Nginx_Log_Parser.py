import re

txt = "192.168.68.1, QWERTY, 1234, 1235 13274"
f = open("apache-logs/apache_logs.txt")

ipregex = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", txt)
print(ipregex)

