import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 20, 1001)
noise = np.random.randn(1001)

a = 0.2  # 0 for linear
b = 1.
c = 2.

trend = a*t**2 + b*t + c

T = np.pi  # period

# Fourier series coefficients
a_0 = 1.

a_1 = 1.
a_2 = 2.
a_3 = 3.

b_1 = 4.
b_2 = 5.
b_3 = 6.

timeseries = a_0 \
    + a_1*np.cos(1*np.pi*t/T) \
    + a_2*np.cos(2*np.pi*t/T) \
    + a_3*np.cos(3*np.pi*t/T) \
    + b_1*np.sin(1*np.pi*t/T) \
    + b_2*np.sin(2*np.pi*t/T) \
    + b_3*np.sin(3*np.pi*t/T)

trended_timeseries = timeseries + trend

noisy_timeseries = trended_timeseries + noise

plt.plot(t, trended_timeseries)
plt.scatter(t, noisy_timeseries)
plt.show()

data = np.vstack((t, timeseries)).T
noisy_data = np.vstack((t, noisy_timeseries)).T


# np.savetxt(
#     "linear_trend_test_timeseries.csv",
#     data,
#     delimiter=","
# )

# np.savetxt(
#     "linear_trend_test_timeseries_noisy.csv",
#     noisy_data,
#     delimiter=","
# )

np.savetxt(
    "quadratic_trend_test_timeseries.csv",
    data,
    delimiter=","
)

np.savetxt(
    "quadratic_trend_test_timeseries_noisy.csv",
    noisy_data,
    delimiter=","
)
