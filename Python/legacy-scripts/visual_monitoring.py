import matplotlib.pyplot as plt
import csv


csv_file = 'container_stats.csv'


container_name = []
cpu_usage = []
ram_usage = []


with open(csv_file, mode='r') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        if len(row) == 3:  # Sprawdź, czy są 3 kolumny
            name, cpu, ram = row[0], float(row[1]), float(row[2])
            container_name.append(name)
            cpu_usage.append(cpu)
            ram_usage.append(ram)
        else:
            print(f"Pominięto nieprawidłowy wiersz: {row}")

plt.figure(figsize=(12, 7))

#CPU
plt.bar(container_name, cpu_usage, color='skyblue', label='CPU usage (%)')

#RAM
plt.plot(container_name, ram_usage, color='green', marker='o', label='RAM usage (MB)')

#labels
plt.xlabel('Container name')
plt.ylabel('Usage')
plt.title('Container CPU and RAM usage')
plt.legend()
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
