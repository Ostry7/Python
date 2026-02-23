import re, csv
from collections import Counter

ip_reg = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

status_req_reg = r'"(?:GET|POST) .* (4\d{2}|5\d{2})'

f = open("apache-logs/apache_logs.txt")

#parse logs
with open("apache-logs/apache_logs.txt") as f:
    errors = []
    for line in f:
        ip_match = re.search(ip_reg,line)
        status_match = re.search(status_req_reg,line)
        if ip_match and status_match:
            errors.append((ip_match.group(), status_match.group()))

top_errors = (Counter(errors).most_common(10))  #TOP 10
print ("TOP 10 errors:")
for (ip,status), count in top_errors:
    print(f"{ip}, ({status}): {count}")


#export csv
with open ("errors.csv", 'w', newline='') as errorfile:
        writer = csv.writer(errorfile)
        writer.writerow(['IP', 'Status_code', 'Occurrences'])
        writer.writerows(top_errors)


