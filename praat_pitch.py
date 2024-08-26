import parselmouth


def praat_pitch(x, Fs, time_step, f0min, f0max):
    '''
    Extracts the fundamental frequency (F0) using the Praat algorithm.

    Parameters:
        x : np.ndarray
            Input audio signal
        Fs : int
            Sampling rate of x
        time_step : float
            The time step used for the pitch analysis
        f0min : int
            Minimum expected F0 in Hz
        f0max : int
            Maximum expected F0 in Hz
    Returns:
        f0 : np.ndarray
            Array of the estimated F0 values at every time interval
    '''
    sound = parselmouth.Sound(x, Fs)    # convert audio into a Praat Sound object
    pitch = sound.to_pitch(time_step, f0min, f0max) # convert sound into a Praat Pitch object
    f0 = pitch.selected_array["frequency"]
    return f0
