import numpy as np

def CPP(x, Fs, f0min, f0max):
    '''
    *Credits to Mark Skowronski for developing the original function in matlab.
    This function calculates cepstral peak prominence (CPP) according to Hillenbrand et al. (1994).
    
    Parameters:
        x : np.ndarray
            Input audio signal
        Fs : int
            Sampling rate of x
        f0min : int
            Minimum frequency to search for cepstral peak
        f0max : int
            Maximum frequency to search for cepstral peak
    Returns:
        P : float
            Cepstral peak prominence value in dB

    Reference:
    Hillenbrand, Cleveland, and Erickson, "Acoustic Correlates of Breathy Vocal Quality," JSHR, vol.
    37, pp. 769-778, Aug. 1994    
    '''
    fft_size = 2**15
    Xabs = np.abs(np.fft.fft(x, fft_size))  # spectrum magnitude
    
    Hsmooth = [0.5, 1, 0.5]
    Xabs = np.convolve(Xabs, Hsmooth, 'same')   # smooth spectrum

    X = np.log(Xabs)    # log spectrum

    X = X-X.mean()  # zero mean

    c = np.fft.ifft(X)  # real cepstrum 
    C = 20*np.log10(np.abs(c))

    # Determine limits over which to search for peak in C and to perform cepstral baseline regression
    tRange = [np.ceil(Fs/f0max),np.floor(Fs/f0min)+1]
    tRange = [int(tRange[0]),int(min(fft_size/2,tRange[1]))]

    CRange = C[tRange[0]:tRange[1]]

    Cmax = max(CRange)
    CmaxIndex = np.argmax(CRange)
    
    # Find regression of C in tRange
    R = np.column_stack((np.arange(len(CRange)), np.ones_like(CRange)))
    m, b = np.linalg.lstsq(R, CRange)[0]    # m = slope, b = y-intercept
    
    Cbaseline = m*(CmaxIndex)+b
    P = Cmax - Cbaseline    # normalize with baseline value
 
    return P