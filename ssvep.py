import numpy as np

def ssvep(fft, freqs):
    # Filter only positive frequencies
    positive_indices = np.where((freqs > 0) & (freqs <= 35))[0]
    positive_fft = fft[positive_indices]
    positive_freqs = freqs[positive_indices]

    # Find the frequency with the maximum power
    max_power = np.max(np.abs(positive_fft))
    max_power_index = np.argmax(np.abs(positive_fft))

    # Get the corresponding frequency
    max_freq = positive_freqs[max_power_index]

    return max_freq, max_power
