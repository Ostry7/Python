### Task 1: Apache/Nginx Log Parser [v]

Create:
- Python script that parses Apache/Nginx access logs
- Extract IP addresses from failed requests (4xx/5xx status codes)
- Count top 10 IPs with most errors
- Export results to errors.json and errors.csv

### Key elements:

There are two key element in code:
```python
ip_reg = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
```
---> to match only max 3 digits from current line using regex (matching IP addresses)

and:
```python
status_req_reg = r'"(?:GET|POST) .* (4\d{2}|5\d{2})'
```
---> to match GET or POST with error code (4xx/5xx status codes)