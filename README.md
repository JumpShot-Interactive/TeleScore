# TeleScore
![TeleScore Build](https://github.com/JumpShot-Interactive/TeleScore/actions/workflows/python-app.yml/badge.svg)</br>
TeleScore is an open-source PyQt-based customizable livestream scoring utility. Designed to be flexible to accommodate scoring and timing different sports, both TeleScore's controls and outputs can be modified to best fit your needs. The program will allow for both text outputs as well as, eventually, graphical output to simplify setup and operation. TeleScore aims to be easy enough for the beginner, but feature-rich enough for professionals.  
TeleScore is currently undergoing a full rewrite to fully utilize the flexible PyQt toolset. The end-goal for development will include external plugin support, browser-source output in addition to legacy text output, custom components, and a scoreboard "projector" mode in addition to the stream scorebug.
## How to build
1. Make sure you have Python v3.10.6 installed.
2. Using command line, head to the root directory of the project (Not src folder, folder above it)
3. Using pip, install the dependencies by using "pip install -r requirements.txt"
4. If no errors are shown, use "python src/main.py" to build the software
