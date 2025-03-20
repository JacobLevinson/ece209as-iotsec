import os
import time
import sounddevice as sd
import numpy as np
import pynput.mouse
import pynput.keyboard
from scipy.io.wavfile import write
from datetime import datetime
import pyautogui
pyautogui.FAILSAFE = False

# Configure microphone index and recording settings
MICROPHONE_INDEX = 29  # Yeti Stereo Microphone
SAMPLERATE = 44100
CHANNELS = 2  # Record in stereo
RECORD_DURATION = 1.0  # Stop recording automatically after 1 second

# Directories for saving files
MONO_DIR = "displacements_new"
STEREO_DIR = "displacements_stereo_new"
os.makedirs(MONO_DIR, exist_ok=True)
os.makedirs(STEREO_DIR, exist_ok=True)

# Recording state and buffers
recording = []
recording_active = False
start_time = None  # Track when recording starts
last_mono_filepath = None  # Store the last recorded mono file path
last_stereo_filepath = None  # Store the last recorded stereo file path

# Mouse tracking
mouse_start_x, mouse_start_y = None, None
mouse_final_x, mouse_final_y = None, None

# Audio recording callback


def callback(indata, frames, time, status):
    if status:
        print(status)
    if recording_active:
        recording.append(indata.copy())

# Mouse movement listener


def on_move(x, y):
    global mouse_final_x, mouse_final_y
    mouse_final_x, mouse_final_y = x, y

# Function to stop recording automatically


def stop_recording():
    global recording_active, recording, mouse_start_x, mouse_start_y, mouse_final_x, mouse_final_y
    global last_mono_filepath, last_stereo_filepath

    # Stop recording
    recording_active = False
    print("Recording stopped automatically after 1 second.")

    # Calculate mouse displacement
    x_displacement = (mouse_final_x or mouse_start_x) - mouse_start_x
    y_displacement = (mouse_final_y or mouse_start_y) - mouse_start_y

    # Generate timestamp and filenames
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{x_displacement}_{y_displacement}.wav"
    mono_filepath = os.path.join(MONO_DIR, filename)
    stereo_filepath = os.path.join(STEREO_DIR, filename)

    # Save audio if recorded
    if recording:
        audio_data = np.concatenate(recording, axis=0)

        # Save stereo file
        write(stereo_filepath, SAMPLERATE, audio_data)
        print(f"Stereo audio saved: {stereo_filepath}")

        # Convert to mono by averaging both channels
        audio_mono = np.mean(audio_data, axis=1, dtype=np.float32)
        write(mono_filepath, SAMPLERATE, audio_mono)
        print(f"Mono audio saved: {mono_filepath}")

        # Update last recorded file paths
        last_mono_filepath = mono_filepath
        last_stereo_filepath = stereo_filepath
    else:
        print("No audio recorded.")

# Function to delete last recorded file


def delete_last_recording():
    global last_mono_filepath, last_stereo_filepath

    if last_mono_filepath and os.path.exists(last_mono_filepath):
        os.remove(last_mono_filepath)
        print(f"Deleted last mono recording: {last_mono_filepath}")
        last_mono_filepath = None  # Clear reference after deletion
    else:
        print("No mono recording to delete.")

    if last_stereo_filepath and os.path.exists(last_stereo_filepath):
        os.remove(last_stereo_filepath)
        print(f"Deleted last stereo recording: {last_stereo_filepath}")
        last_stereo_filepath = None  # Clear reference after deletion
    else:
        print("No stereo recording to delete.")

# Keyboard event listener


def on_press(key):
    global recording_active, recording, mouse_start_x, mouse_start_y, start_time

    try:
        if key.char == 'q':  # Start recording
            if not recording_active:
                # Start recording
                recording.clear()
                recording_active = True
                start_time = time.time()  # Record the start time

                # Center mouse
                screen_width, screen_height = pyautogui.size()
                pyautogui.moveTo(screen_width // 2, screen_height // 2)

                # Set initial mouse position
                mouse_start_x, mouse_start_y = pyautogui.position()
                print("Recording started...")

                # Wait for 1 second, then stop automatically
                while time.time() - start_time < RECORD_DURATION:
                    time.sleep(0.01)  # Short sleep to avoid blocking

                stop_recording()

        elif key.char == 'd':  # Delete last recording
            delete_last_recording()

        elif key.char == 'c':  # Quit program
            print("Exiting...")
            stream.stop()
            mouse_listener.stop()
            keyboard_listener.stop()
            exit(0)

    except AttributeError:
        pass


# Setup recording stream
stream = sd.InputStream(samplerate=SAMPLERATE, channels=CHANNELS,
                        callback=callback, device=MICROPHONE_INDEX)

# Start mouse listener
mouse_listener = pynput.mouse.Listener(on_move=on_move)
mouse_listener.start()

# Start keyboard listener
keyboard_listener = pynput.keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# Start recording stream
with stream:
    keyboard_listener.join()
