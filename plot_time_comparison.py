import matplotlib.pyplot as plt

# Your actual measured values
labels = ["Encryption", "Decryption"]
times = [27.611, 15.255]  # in milliseconds

# Custom colors (NOT blue)
colors = ["#FF6F61", "#6B5B95"]  # coral + purple

plt.figure(figsize=(6, 4))

bars = plt.bar(labels, times, color=colors)

# Add values on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.5,
             f"{height:.2f}", ha='center')

plt.title("Encryption vs Decryption Time Comparison")
plt.xlabel("Operation")
plt.ylabel("Time (ms)")

plt.tight_layout()

plt.savefig("time_comparison.png")
plt.show()