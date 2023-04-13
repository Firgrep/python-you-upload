# Python YouUpload :: README

Python YouUpload is a script that uploads and schedules a video along with a custom thumbnail to YouTube and adds the new video to an existing playlist (optional) using OAuth 2.0 authentication. Made to eliminate repetitive actions (copy-pasting description, tags, etc.) during frequent YouTube uploads. This is primarily an educational project to learn about the YouTube Data API and OAuth procedures, but with utility in mind.

First use will prompt the user to log into the relevant google account in order to give the app credentials. These will then be stored as a local .pickle file which will be used retrieve tokens for future program execution. The script will refresh tokens as needed and update the .pickle file. Depending on permission expiry, renewed manual logins may be needed. 

The script does not currently come with error handling. Moreover, there is currently no possibility in the YouTube Data API to add information about video elements (such as end screens), such that these still need to be added manually after the script upload.

## Requirements

* Register your app with Google. Find the procedure here: https://developers.google.com/youtube/registering_an_application
* The scopes the script uses are "https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.upload" and "https://www.googleapis.com/auth/youtube", so make sure those scopes are added this the app's authentication. It may be that .readonly is not necessary at this stage, but if you plan on retrieving additional information, such as various playlist or video IDs, it can be handy to keep .readyonly. 
* In order to use the OAuth 2.0 steps with this script, a client_secrets.json file is required that contains information from the API Console. The file should be in the same directory as the script. Once downloaded from the API console, move the .json file into the local script folder (same place as script.py) and rename it so "client_secret.json" - the script will look for a file with this _exact name_ in the local directory. 


## Installing
* Copy project files into a new directory (using, for example, ```git clone https://github.com/Firgrep/python-you-upload.git```).
* It is _recommended_ to set up a virtual environment for the script and its dependencies. You can do this by making a new directory and then, when within that directory, run ```py -3 -m venv .venv``` and then open your code editor within that directory (or, if you're already in a code editor, open a new terminal to start using the virtual environment). 
    - If for some reason the virtual environment does not activate, manual activation is possible but it may differ depending on your machine and code editor:
        - On Unix or MacOS, using the bash shell: source /path/to/venv/bin/activate
        - On Unix or MacOS, using the csh shell: source /path/to/venv/bin/activate.csh
        - On Unix or MacOS, using the fish shell: source /path/to/venv/bin/activate.fish
        - On Windows using the Command Prompt: path\to\venv\Scripts\activate.bat
        - On Windows using PowerShell: path\to\venv\Scripts\Activate.ps1

* Run this command to install dependencies ```pip install -r requirements.txt```.
    - NOTE: A bug was encountered using the latest packages from the Google Python API client (2023/03/27), specifically to do with the flow object, therefore these exact depency versions were chosen since they function together right out the box. Future releases of the API client will likely patch this (if they haven't already). (For more information about this, see https://github.com/xyou365/AutoRclone/issues/101)


## Usage
This script is used to upload videos to the sPhil channel (https://www.youtube.com/channel/UC8n4PI9Niv8ksUM-NeVx1ig), so you may want to alter the initial data to fit your video upload, but feel free to use it as an example to inspire you!

Setting the parameters:
* Set the correct paths to your payload directory (media files to be uploaded). For this, it is required to set the relative path to the payload directory as the absolute path is set based on where the script is located on your machine. To seperate concerns, the payload folder is initially moved two levels up to move it out of development directories, but you may feel free to put it wherever you like, even within this project directory should you prefer. You may also rename the payload directory to something else or do away with it altogether (untested).
* Set the generic-related data to what you prefer. The idea behind these constants is that they will likely stay unchanged between repeated uploads, eliminating the need to input repeated data. Said otherwise, this is the data you will frequently share between videos.
* Set the file names for the video and thumbnail to be uploaded. The idea is that one will rename the files themselves and dump them into the payload folder and then run the script instead of changing the file names and path in the script. But you may want to change the file names for other reasons so you can do that here. 
* Set the instance-related data--title, scheduled publish data, unique description, etc.--for the particular executition. Two unique description constants are present which will be added to the main description constant, one for the beginning and one for the end respectively. The idea behind this is that although you may have a bulk of data that you will use between video uploads, you may also want a short description particularly for _this_ video and perhaps a credit acknowledgement.
    - Additional note about scheduling video publication: The script is built with scheduling video publications in mind, but if you would like to publish instantly, set ```S_PUBLISH_DATE``` to somewhere in the past (using the same datetime format) and YouTube will publish it instantly upon upload. Do this instead of setting the privacy status to "public". 
* If you would like the new video to be added to a playlist (currently set to be appended as the last element of the list), provide ```S_PLAYLIST_ID``` with a Playlist ID (string). This can be retrieved in the URL information of a playlist after the "=" in https://www.youtube.com/playlist?list={playlistId}. Currently, an ID is retrieved from a local machine using environmental variables. You can do the same or just set the string directly. If not playlist is provided, the script will skip this part of the process.

Running the script:
* To run the script, execute in the terminal ```python script.py``` .
* First-time usage will prompt a link to follow in order to gain permissions. Make sure you are logged into the relevant Google account on the browser and select it from the list. Once permissions have been granted, return to the terminal and copy-paste the required authentication key (try right-clicking with the mouse to paste contents) and press enter. If successful, the script will run through its requests and print to the console when it completes its steps. 
* When the script is done, the video and thumbnail have been uploaded to YouTube. 


## Errors
While no error handling has been programmed, the google api client is usually pretty good printing to the terminal what is wrong in the case of an error. For more info on this, see https://developers.google.com/youtube/v3/docs/errors .


## Resources
This script was build with the use of the resources below. 
* YouTube Data API Documentation. Includes guides, samples and references. https://developers.google.com/youtube/v3 
* OAuth tutorial by Corey Schafer. Extremely helpful in understanding how OAuth work and how to pickle credentials with Python. https://www.youtube.com/watch?v=vQQEaSnQ_bs 
