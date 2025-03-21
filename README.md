# Mouse Movement Tracking via Audio Side Channel

Code repository for final project of [**W25 ECE 209AS: Secure and Trustworthy Edge Computing Systems**](https://ssysarch.ee.ucla.edu/courses/W25/index.html).

## Files

- [displacement.py](displacement.py) is the Python script to record mouse movement and audio.
- [requirements.txt](requirements.txt) lists the Python dependencies needed for our Python script.
- [finalproject.ipynb](finalproject.ipynb) is the Jupyter notebook downloaded from our Google Colaboratory. It contains the code and output for data pre-processing and machine learning.
- Raw audio recordings are in the various `displacements*/` directories.

## Setup

Create a Python virtual environment and install dependencies:

<table>
<tr>
  <th>Windows / PowerShell</th>
  <th>Unix / Bash</th>
</tr>
<tr>
  <td>

  ```sh
  python -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
  ```

  </td>
  <td>

  ```sh
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

  </td>
</tr>
</table>

If starting a new shell session, re-enter the virtual environment with the second command.

## Usage

Connect the Blue Yeti microphone and mouse to the computer. Set the `MONO_DIR` and `STEREO_DIR` variables in [displacement.py](displacement.py) to point towards your desired output directories, if different.

Start the program loop (recording does not start yet):

<table>
<tr>
  <th>Windows / PowerShell</th>
  <th>Unix / Bash</th>
</tr>
<tr>
  <td>

  ```sh
  python displacement.py
  ```

  </td>
  <td>

  ```sh
  python3 displacement.py
  ```

  </td>
</tr>
</table>

Use the following keyboard shortcuts:

- `q`: Starts recording for exactly 1 second. Press this and then make your mouse motion. Note that this automatically resets the mouse cursor to the center of the screen, so you do not need to manually reposition it between recordings.
- `d`: Delete the last recording. Press this when you made a mistake in the last recording (e.g. accidental background noise).
- `c`: Quit the program loop. Use this instead of `^C`, which does not work for some reason.

Recordings are automatically saved as `{timestamp}_{x}_{y}.wav` files in the output directories. `timestamp` is in `YYYY-mm-ss_HH-MM-SS` format and `x` and `y` are (possibly negative) integers representing *relative displacement* from the center $x, y$ of the screen, in pixels.
