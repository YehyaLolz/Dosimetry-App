# Dosimetry-App

This Python-based application has been developed to facilitate the vocal analysis of the audio files produced by the [Do-It-Yourself Voice Dosimeter Device](https://doi.org/10.1044/2023_JSLHR-23-00060) through an intuitive, user-friendly interface built with Tkinter. The interface allows users to input data such as gender, calibration files and levels, monitoring data, and a save location for results. Outputs are generated as Microsoft Excel files containing key acoustic voice parameters, including Sound Pressure Level (SPL), fundamental frequency (fo), and Cepstral Peak Prominence (CPP), along with a comprehensive set of vocal doses described briefly in [doses.py](./doses.py). While most calculations are handled by custom functions, fo is derived using Parselmouth, a Python interface for Praat software. Additionally, the application provides interactive plots of SPL and fo for users to visualize and explore the results.

## Getting Started

### Installation

To install the app:
1. [**Download the latest version**](https://github.com/YehyaS/Dosimetry-App/releases/download/v1.0/dosimetry_app.exe): The easiest and preferred method is to download the latest version directly.

Alternatively, if you'd like to build the app yourself from the source code:

1. Install [pyinstaller](https://pyinstaller.org/en/stable/installation.html).
2. Run: `pyinstaller ./dosimetry_app.py --windowed --onefile`.
3. The compiled app will be located in the `dist` directory as a standalone executable.

### Tutorials

Here are some visual tutorials to guide you through the process:
- [Calibration Tutorial](https://youtu.be/YO5r1BUESJ0) (credits to Pasquale Bottalico)
- [Software Demonstration](https://youtu.be/0-rT5NyHDTM) (credits to Charlie Nudelman)

### Usage

1. **Select Gender**: Choose the speaker's gender. If "Other" is selected, you may specify details.
2. **Add Calibration File**: Upload at least one calibration audio file and input the corresponding calibration level in decibels.
3. **Add Monitoring File**: Upload the monitoring session's audio file.
4. **Choose Save Folder**: Specify the folder where the analysis results will be saved.
5. **Run Analysis**: Click "Submit" to begin the analysis. Processing time depends on file size. Once complete, a window will display the vocal dose table (defined in the [doses.py](./doses.py) file) along with five additional plots.
6. **Reset**: To start a new analysis, close the plot window and repeat the steps. To fully reset the app, click "Reset."  

## Contact

For issues, suggestions, or questions, feel free to reach out via email at yehyas2@illinois.edu.

## References

Bottalico P, Nudelman CJ. Do-It-Yourself Voice Dosimeter Device: A Tutorial and Performance Results. J Speech Lang Hear Res. 2023 Jul 12;66(7):2149-2163. doi: [10.1044/2023_JSLHR-23-00060](https://doi.org/10.1044/2023_JSLHR-23-00060). Epub 2023 Jun 1. PMID: 37263017.