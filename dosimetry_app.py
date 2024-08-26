import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from analysis import *
import os
import threading
import webbrowser

def gender_interface(user_input, root):
    '''
    GUI for gender selection.

    Parameters:
        user_input : dict
            Dictionary containing user input
        root : tk.Frame
            The root widget where this interface will be placed
    '''
    label = tk.Label(root)
    label.pack(anchor=tk.W, padx=20, pady=5)
    label.config(text="Select the speaker's gender:")

    male = tk.Radiobutton(root, text="Male", variable=user_input["gender"], value="male")
    male.pack(anchor = tk.W, padx=20)
    female = tk.Radiobutton(root, text="Female", variable=user_input["gender"], value="female")
    female.pack(anchor=tk.W, padx=20)
    
    frame = tk.Frame(root)  # create a frame to hold the "Other" button and its associated entry field
    frame.pack(anchor=tk.W)
    other = tk.Radiobutton(frame, text="Other:", variable=user_input["gender"], value="other")
    other.pack(side=tk.LEFT, padx=20)

    other_entry = tk.Entry(frame, width=20, textvariable=None)
    other_entry.pack(side=tk.LEFT)

def calibration_interface(user_input, root):
    '''
    GUI for the "Add calibration" button

    Parameters:
        user_input : dict
            Dictionary containing user input
        root : tk.Frame
            The root widget where this interface will be placed
    '''
    main_frame = tk.Frame(root)
    main_frame.pack(anchor=tk.W)
    cal_button = tk.Button(main_frame, text="Add Calibration File", command=lambda: new_cal_file(user_input, main_frame))
    cal_button.pack(anchor=tk.W, side=tk.BOTTOM, padx=20, pady=10)

def new_cal_file(user_input, root):
    '''
    GUI for calibration file upload interface.

    Parameters:
        user_input : dict
            Dictionary containing user input
        root : tk.Frame
            The root widget where this interface will be placed
    '''
    # Create Tkinter variables for holding calibration level and file and add them to user_input
    cal_level = tk.StringVar(value="")
    user_input["cal_levels"].append(cal_level)
    cal_file = tk.StringVar(value="")
    user_input["cal_files"].append(cal_file)
    frame = tk.Frame(root)

    # Create a frame to hold the calibration level entry and upload button
    frame.pack(anchor=tk.W)
    cal_label = tk.Label(frame, text="Calibration level (dB):")
    cal_label.pack(side=tk.LEFT, padx=20, pady=10)

    cal_entry = tk.Entry(frame, width=10, textvariable=cal_level)
    cal_entry.pack(side=tk.LEFT)

    upload_interface(cal_file, "Calibration File", frame)

def upload_interface(file, file_type, root, dir=False):
    '''
    GUI for upload and directory selection buttons.

    Parameters:
        file : tk.StringVar
            Tkinter variable that stores the path of the selected file or folder
        file_type : str
            String that describes the type of file to be uploaded (e.g. "Calibration File", "Monitoring File")
        root : tk.Frame
            The root widget where this interface will be placed
        dir : bool
            Boolean to indicate whether to select a directory instead of a file
    '''
    # Create a label text indicating the file or folder status 
    file_label_var = tk.StringVar(value=file_type+(":    Not Uploaded" if not dir else ":    Not Selected"))
    file_label = tk.Label(root, textvariable=file_label_var)
    file_label.pack(side=tk.LEFT, padx=20, pady=10)

    if not dir:
        button_command = lambda:upload_file(file, file_type, file_label_var)
    else:
        button_command = lambda:select_folder(file, file_type, file_label_var)

    upload_button = tk.Button(root, text="Browse", command=button_command)
    upload_button.pack(side=tk.LEFT, pady=10)

def upload_file(file, file_type, label_text):
    '''
    GUI for a file dialog that asks the user to select a file.

    Parameters:
        file : tk.StringVar
            Tkinter variable that stores the path of the selected file
        file_type : str
            String that describes the type of file to be uploaded (e.g. "Calibration File", "Monitoring File")
        label_text : tk.StringVar
            Tkinter variable that stores the text displaying the file status
    ''' 
    file.set(filedialog.askopenfilename())
    label_text.set(file_type + ":    " 
                   + os.path.basename(file.get() if file.get() else "Not Uploaded"))
    
def select_folder(folder, folder_type, label_text):
    '''
    GUI for a file dialog that asks the user to select a folder.

    Parameters:
        file : tk.StringVar
            Tkinter variable that stores the path of the selected folder
        file_type : str
            String that describes the type of folder to be selected (e.g. "Save Folder")
        label_text : tk.StringVar
            Tkinter variable that stores the text displaying the folder status
    ''' 
    folder.set(filedialog.askdirectory())
    label_text.set(folder_type + ":    " 
                   + os.path.basename(folder.get() if folder.get() else "Not Selected"))
    
def on_frame_configure(event):
    '''
    Ensures that all widgets are accessible via scrolling
    '''
    canvas.configure(scrollregion=canvas.bbox("all"))

def error_check(user_input):
    '''
    Checks for errors within the user_input before passing it for analysis.
    Errors include:
        1. Not selecting a gender
        2. Entering a calibration level without an associated calibration file and vice versa
        3. Entering a non-float calibration level
        4. Entering a file that is not of type .mp3 or .wav
        5. Not uploading a monitoring file
        6. Not selecting a save folder
        7. Having a plot window already open
    
    Parameter:
        user_input : dict
            Dictionary containing user input
    '''
    message = ""
    gender = user_input["gender"].get()
    if gender=="no_selection":
        message = "Please select a gender."
    else:
        cal_levels = [level.get() for level in user_input["cal_levels"]]
        cal_files = [file.get() for file in user_input["cal_files"]]
        for i in range(len(cal_levels)):
            # Remove any whitespace from calibration level input
            cal_levels[i] = "".join(cal_levels[i].split())

            if cal_levels[i] == "" and cal_files[i] == "":
                continue
            elif cal_levels[i] != "" and cal_files[i] == "":
                message = "Please enter all calibration files."
                break
            elif cal_levels[i] == "" and cal_files[i] != "":
                message = "Please enter all calibration levels."
                break
            try:
                cal_levels[i] = float(cal_levels[i])
            except ValueError:
                message = "Invalid Calibration level: " + cal_levels[i]
                break
            if os.path.splitext(cal_files[i])[1] not in [".MP3", ".mp3", ".wav", ".WAV"]:
                message = "Invalid audio file: " + os.path.basename(cal_files[i]) + ". Please upload .wav or .mp3 files."
                break
        if message == "":
            monitoring = user_input["monitoring"].get()
            save = user_input["save_folder"].get()
            if monitoring == "":
                message = "Please upload the monitoring audio file."
            elif os.path.splitext(monitoring)[1] not in [".MP3", ".mp3", ".wav", ".WAV"]:
                message = "Invalid audio file: " + os.path.basename(monitoring) + ". Please upload .wav or .mp3 files."
            elif save == "":
                message = "Please select a save folder."
    if message != "":
        messagebox.showwarning(title="Error", message=message)
    else:
        # If plot lock is locked, a plot window is already open so prevent the analysis from running
        if not plot_lock.locked():
            time_step, audio, windowTime, SPL, F0, vocal_doses = analysis(cal_files, cal_levels, monitoring, gender, save)
            message = "Analysis results have been saved under " + os.path.basename(save) + "."
            messagebox.showinfo(title="Data Saved", message=message)

            # Acquire the lock to prevent multiple plot windows
            plot_lock.acquire_lock()
            display_data(time_step, audio, windowTime, SPL, F0, vocal_doses)
            plot_lock.release_lock()
        else:
            messagebox.showerror(title="Error", message="Please close the existing plot window before opening a new one.")

def reset(root):
    '''
    Resets the root window if there is no plot window active.

    Parameters:
        root : tk.Tk
            The root window of the app
    '''
    if not plot_lock.locked():
        root.destroy()
        setup()
    else:
        messagebox.showerror(title="Error", message="Please close the existing plot window before resetting.")


def setup():
    '''
    Initializes and configures the main Tkinter GUI window for the Dosimetry App.
    '''
    master = tk.Tk()
    master.geometry("650x500")
    master.title("Dosimetry App")
    user_input = {"gender":tk.StringVar(value="no_selection"), 
                  "cal_levels":[],                      # List of calibration levels
                  "cal_files":[],                       # List of calibration files
                  "monitoring":tk.StringVar(value=""),  # Path to monitoring file
                  "save_folder":tk.StringVar(value="")} # Path to save folder
    
    # Create a global canvas widget, used for adding scrolling functionality 
    global canvas
    canvas = tk.Canvas(master, highlightthickness=0)
    scrollbar = tk.Scrollbar(master, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)  # Link the scrollbar with the canvas
    main_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=main_frame, anchor="nw")

    gender_interface(user_input, main_frame)
    calibration_interface(user_input, main_frame)
    frame = tk.Frame(main_frame)
    frame.pack(anchor=tk.W)
    upload_interface(user_input["monitoring"], "Monitoring File", frame)
    frame = tk.Frame(main_frame)
    frame.pack(anchor=tk.W)
    upload_interface(user_input["save_folder"], "Save Folder", frame, dir=True)
    next_button = tk.Button(main_frame, text="Submit", command=lambda:error_check(user_input))
    next_button.pack(side=tk.LEFT, padx=20, pady=10)

    reset_button = tk.Button(main_frame, text="Reset", command=lambda:reset(master))
    reset_button.pack(side=tk.LEFT, padx=20, pady=10)

    git_label = tk.Label(master, text="View on GitHub", fg="blue", cursor="hand2")
    git_label.pack(anchor=tk.W, padx=20, pady=10)
    git_label.bind("<Button-1>", lambda x: webbrowser.open_new_tab("https://github.com/YehyaS/Dosimetry-App"))

    # Allow the scroll region to adjust dynamically
    main_frame.bind("<Configure>", on_frame_configure)

    master.mainloop()

plot_lock = threading.Lock()
setup()