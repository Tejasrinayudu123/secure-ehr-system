import matplotlib.pyplot as plt
import random

# Simulated encryption times (replace later if needed)
times = [random.uniform(0.001, 0.01) for _ in range(200)]

plt.plot(times)
plt.title("Encryption Time per Record")
plt.xlabel("Record Index")
plt.ylabel("Time (seconds)")

plt.savefig("encryption_time.png")
plt.show()