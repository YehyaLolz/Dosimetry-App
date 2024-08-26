import numpy as np

def estimate_energy_level(x, Fs, C):
    '''
    Computes the average energy level of an audio signal in dB.

    Parameters:
        x : np.ndarray
            Audio signal
        Fs : int
            Sampling rate of x
        C : int
            Calibration constant added to the final dB level.
    Returns:
        dB : float
            The average energy level in dB, after adding the calibration constant.  
    '''
    X = np.abs(np.fft.fft(x))   # Compute the magnitude of the Fourier Transform of X
    X[X == 0] = 1e-17   # Avoid log(0) issues
    f = (Fs / len(X)) * np.arange(len(X))   # frequency vector

    # Extract the FFT values corresponding to the positive frequencies
    ind = np.where(f < Fs / 2)
    X = X[ind]

    total_energy = np.sum(X**2) / len(X)
    avg_energy = total_energy / ((1 / Fs) * len(x))

    # Convert average energy level to dB and add the calibration constant
    dB = 10 * np.log10(avg_energy) + C
    return dB   