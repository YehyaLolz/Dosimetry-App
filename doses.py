import numpy as np
from cpp import *

def doses(x, Fs, time, SPL, F0, gender, f0min, f0max, no_cal):
    '''
    Calculates vocal doses.

    Parameters:
        x : np.ndarray
            Input audio signal
        Fs : int
            Sampling rate of x
        time : np.ndarray
            Time vector corresponding to SPL and F0 values
        SPL : np.ndarray
            Array of SPL (Sound Pressure Level) values over time, in dB
        F0 : np.ndarray
            Array of F0 (Fundamental Frequency) values over time, in Hz
        gender : str
            Speaker's gender (male, female, other)
        f0min : int
            Minimum frequency to search for CPP (Cepstral Peak Prominence)
        f0max : int
            Maximum frequency to search for CPP (Cepstral Peak Prominence)
        no_cal : bool
            Truth value for whether the data is calibrated
    Returns:
        Dt : float
            Total duration of voicing, only considering voicing periods 
            with defined values of SPL and F0
        VLI : float
            Vocal Load Index, reflecting cumulative vocal effort over time
        Dd : float
            Dynamic Dose, indicates the amount of vocal fold activity
            Undefined if gender is "other" or no calibration file was provided
        De : float
            Energy Dose, quantifies the energy dose delivered to vocal folds
            Undefined if gender is "other" or no calibration file was provided
        Dr : float
            Radiated Dose, represents the sound energy radiated from vocal folds
            Undefined if gender is "other" or no calibration file was provided
        Dt_percentage : float
            Percentage of the total time during which voicing occurs
        Dd_norm : float
            Normalized Dynamic Dose, Dd normalized by total duration of voicing
            Undefined if gender is "other" or no calibration file was provided
        De_norm : float
            Normalized Energy Dose, De normalized by total duration of voicing
            Undefined if gender is "other" or no calibration file was provided
        Dr_norm : float
            Normalized Radiated Dose, Dr normalized by total duration of voicing
            Undefined if gender is "other" or no calibration file was provided
        SPL_mean : float
            Average SPL value during voicing periods
        F0_mean : float
            Average F0 value during voicing periods
        SPL_sd : float
            Standard deviation of SPL during voicing periods
        F0_sd : float
            Standard deviation of F0 during voicing periods
        cpp : float
            Cepstral Peak Prominence, higher CPP indicates a clearer and more
            resonate voice.
    '''
    # Make sure that F0 and SPL are np arrays
    F0 = np.array(F0)
    SPL = np.array(SPL)

    time_step = time[1]-time[0]
    n = len(time)
    Pth=np.zeros(n)         # Threshold pressure
    Pl=np.zeros(n)          # Lung pressure
    A=np.zeros(n)           # Amplitude of oscillation
    T=np.zeros(n)           # Tension coefficient
    eta=np.zeros(n)         # Efficiency factor
    omega=np.pi*2*F0        # Angular frequency
    Dt_partial=np.zeros(n)
    SPL_partial=time_step*SPL
    F0_partial=time_step*F0
    VLI_partial=F0*time_step
    De_partial=np.zeros(n)
    Dr_partial=np.zeros(n)

    for i in range(n):
        # Skip if the current values of F0 or SPL are undefined
        if F0[i] < 1e-10 or SPL[i] < 1e-10:
            continue

        if gender == "male":
            Pth[i]=0.14+0.06*(F0[i]/120)**2
            Pl[i]=Pth[i]+10**((SPL[i]-72.48)/27.3)
            
            A[i]=time_step*0.016*((Pl[i]-Pth[i])/Pth[i])**0.5
            T[i]=0.0158/(1+2.15*(F0[i]/120)**0.5)

            eta[i]=5.4/F0[i]
        else:
            Pth[i]=0.14+0.06*(F0[i]/190)**2
            Pl[i]=Pth[i]+10**((SPL[i]-72.48)/27.3)

            A[i]=time_step*0.010*((Pl[i]-Pth[i])/Pth[i])**0.5
            T[i]=0.01063/(1+1.69*(F0[i]/190)**0.5)

            eta[i]=1.4/F0[i]
        
        Dt_partial[i]= time_step
        De_partial[i]=eta[i]*(A[i]/T[i])**2*omega[i]**2*time_step/1000
        Dr_partial[i]=10**((SPL[i]-120)/10)*1000*time_step

    Dd_partial=time_step*F0*A
    Dt = sum(Dt_partial)
    VLI=sum(VLI_partial)/1000
    Dd=4*sum(Dd_partial)
    De=0.5*sum(De_partial)
    Dr=4*np.pi*sum(Dr_partial)
    Dt_percentage=100*Dt/(time[-1]-time[0])
    Dd_norm=Dd/Dt
    De_norm=De/Dt
    Dr_norm=Dr/Dt
    SPL_mean=sum(SPL_partial)/Dt
    F0_mean=sum(F0_partial)/Dt

    SPL_sd=np.std(SPL_partial, ddof=1)
    F0_sd=np.std(F0_partial, ddof=1)

    if no_cal or gender == "other":
        Dd = "--UNDEFINED--"
        De = "--UNDEFINED--"
        Dr = "--UNDEFINED--"
        Dd_norm = "--UNDEFINED--"
        De_norm = "--UNDEFINED--"
        Dr_norm = "--UNDEFINED--"

    cpp = CPP(x, Fs, f0min, f0max)

    return Dt, VLI, Dd, De, Dr, Dt_percentage, Dd_norm, De_norm, Dr_norm, SPL_mean, F0_mean, SPL_sd, F0_sd, cpp