MAIN LIBRARIES

OpenCV     --- breaking down the uploaded optimal shooting form into frames <br>
MediaPipe  --- analyzes the frames, extracts the positions of the different joins <br>
NumPy      --- calculate angles of joint + stabilize/normalize the values of joint positions <br>
SciPy      --- calculate angles of joint + stabilize/normalize the values of joint positions <br>

*********************************************************************************************************************************************************

HOW TO SETUP PROJECT DIRECTORY:

*****YOU MUST INSTALL PYTHON 3.11.9 AND RUN ALL COMMANDS IN POWERSHELL INSIDE THE ROOT DIRECTORY*****

Step 1. Clone the repo


Step 2. Go to the root directory of the cloned project in PowerShell


Step 3. Setup and then run virtual environment

*create environment
Command: `py -3.11 -m venv .venv`

*start environment
Command: `.\.venv\Scripts\Activate.ps1`


Step 4. Setup pip

Command: `python -m pip install --upgrade pip setuptools wheel`


Step 5. Install all dependencies

Command: `pip install -e .`


Step 6. Verify setup succeeded. The following command will print "Ready" if it succeeds

Command: `python -c "import jumpcoach_ml; print('Ready')"`


Step 7. Always run/test the program in the virtual environment because that's where you install the dependencies.

Command: `.\.venv\Scripts\Activate.ps1`

**********************************************************************************************************************


<img width="543" height="700" alt="AnalyzeUploadedVidFlowChart" src="https://github.com/user-attachments/assets/0d9fca3b-73be-4335-916b-320782eeac0b" />




