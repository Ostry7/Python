import re
from collections import Counter

ip_reg = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

status_req_reg = r'"(?:GET|POST) .* (4\d{2}|5\d{2})'

f = open("apache-logs/apache_logs.txt")

with open("apache-logs/apache_logs.txt") as f:
    errors = []
    for line in f:
        ip_match = re.match(ip_reg,line)
        status_match = re.search(status_req_reg,line)
        if ip_match and status_match:
            errors.append(ip_match.group())
print (Counter(errors).most_common(10))

