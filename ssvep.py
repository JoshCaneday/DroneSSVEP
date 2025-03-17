import numpy as np
def ssvep(fft, freqs):
    # Find the frequency with the maximum power
    max_power = np.max(np.abs(fft))
    max_power_index = np.argmax(np.abs(fft))

    # Get the corresponding frequency
    max_freq = freqs[max_power_index]

    return max_freq, max_power