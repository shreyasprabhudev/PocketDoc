import json
import matplotlib.pyplot as plt

with open('performance_metrics.json', 'r') as f:
    results = json.load(f)

common_times = [r['response_time'] for r in results if r['scenario'] == 'common']
specific_times = [r['response_time'] for r in results if r['scenario'] == 'specific']

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(common_times, marker='o', color='b')
plt.title('Response Times for Common Scenarios')
plt.xlabel('Request Number')
plt.ylabel('Response Time (seconds)')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(specific_times, marker='o', color='r')
plt.title('Response Times for Specific Scenarios')
plt.xlabel('Request Number')
plt.ylabel('Response Time (seconds)')
plt.grid(True)

plt.tight_layout()
plt.savefig('performance_graph.png')
plt.show()

print("Graph generated and saved as performance_graph.png.")
