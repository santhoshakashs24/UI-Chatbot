# UI-Chatbot
___________________________
This Challenge has been completed through Kivy an open-source, cross-platform Python framework designed for developing multi-touch applications with a natural user interface (NUI).

# File Structure
_________________
lseg_Chatbot.py - Main py file logic for parsing and displaying data and chatbot logic
Chats.Kv - Styling using Kivy Framework

Dependencies - Inside Resources folder - fonts, Images(LSEG Icon, Chatbot Icon), Stock Exchange Json data.

# Code Execution
python -m venv env  
env\Scripts\activate.bat **or**
env\Scripts\activate.ps1 
pip install -r requirements.txt

python lseg_Chatbot.py
This brings up the UI, as per the challenge following the best practices, error handling, logging etc.
ps: sometimes, we need to setup the env variable with 'KIVY_GL_BACKEND:angle_sdl2' in windows.


# Pre-Compiled
Have attached pre-compiled exe, which can be executed directly through unzipping, navigate to dist->LsegChatbot.exe directly


# Docker

Also you can pull the docker image from akashl21/ui-chatbot and run it with the help of X11 forwarding on Linux.




