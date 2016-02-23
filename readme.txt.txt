Required Libraries and Modules:

-MoviePy: https://github.com/Zulko/moviepy
	Numpy,imageio,Decorator, and tqdm are necessary but installed along with MoviePy

-ImageMagick: http://www.imagemagick.org/script/binary-releases.php 
	Install according to operating system and python version
	If operating system is windows, go into moviepy/config_defaults.py and provide path to
	ImageMagick (IMAGEMAGICK_BINARY = "C:\\Program Files\\ImageMagick_VERSION\\convert.exe")

-PyGame: http://www.pygame.org/download.shtml
	Install according to operating system and python version

PIL: http://www.pythonware.com/products/pil/
	Install according to operating system and python version

SciPy: http://www.scipy.org/install.html
	Install according to operating system and python version

scikit: http://www.lfd.uci.edu/~gohlke/pythonlibs/#scikit-image
	Install according to operating system and python version
	Use pip to install the wheel file.
	run cmd or terminal and use command: pip install _______.whl

Documentation:

This video editor works best when you keep everything in the local directory, but it is not
necessary. 

Features include:
-Clip insertion
-Clip replacement
-Audio insertion
-Audio replacement
-Text insertion
-Audio removal
-Audio retrieval
-Masking
-Filter
-Changing speeds
-Video resizing
-Previewing videos
-Incremental editing
-Browse for files

Important: If anything out of the ordinary occurs, simply press q to try again.
Watch out for a "Please Try Again" sign that may come up at the top every now and then
if it does come up it may mean that you chose wrong values or wrong files.

For the most part it would be ideal to work with .mp4 and .mp3 files. However, it is not 
necessary and most audio/video files should work. 

Clip Insertion - This allows for the insertion of a clip at a certain time in the original
video. The user can then decide what portion of the second clip they would like to insert 
via a slider.

Clip Replacement - This allows for the replacement of a clip at a certain interval of time in
the original video. The user can choose a start and end time for the original video and replace it
with a clip from a different video, also choosing the start and end time for that video.

Audio Insertion - Allows the user to insert an audio track into the video at a chosen start time.
The user can choose how much of the new audio file they want to insert

Audio Replacement - Similar to clip replacement, allows for the replacement of a period of audio
using a period from a new audio track.

Text Insertion - Allows for the insertion of text at any x/y position in the video starting at a
chosen time and ending at another chosen time.

Audio Removal - Returns video file without audio

Audio Retrieval - Retrieves the audio file from a video in .mp3 format

Masking - Places on video on top of another one allowing for the user to resize the second video
appropriately as well as choose the position, time, and duration to place it at/for.

Filter - Currently only one filter is available due to some trouble with scikit, but allows for
freezing and sharpening of contours at a chosen time interval

Changing Speeds - Allows user to change the speed at which a video plays.

Video Resizing - Allows the user to change the original video's dimensions to better fit their needs

Previewing Video - Allows the user to preview the video to see how their changes have affected it. However,
needs to be after they manually select a new video and before it is edited. Has to do with file path vs file name implementations

Incremental Editing - Allows user to go back on mistakes and see their process of editing by creating a new video for
every edit made and automatically switching the original video to the freshly edited one if the user wishes to keep editing

Browse for Files - For most decisions allows user to browse for a file to use rather than write it out themselves. Handy in saving time
and is convenient.

Things to watch out for* 
- If two videos resolutions differ too much, it could possibly be a mismatch and it is possible that they will not combine together smoothly
- If the length of video is too long it potentially take a bit of time to process. 
- If the length of a video is too long, the slider sometimes malfunctions as event.x/event.y lack float values so it is not possible to implement
consistent intervals for the slider to track on if the duration of a clip is too long.
- Audio files generally will not work if you choose it as the original video. The program is meant to be a video editor, not an audio one.
- For masking, or layovers, if multiple position boxes are clicked, more than one might highlight, however the last selected position will be the one chosen.
- For masking, or layovers, if a position box is clicked and then a text box is clicked, the highlighting might disappear, but the last selected position will still be chosen.
- When applying filter, try not to start at t=0 or t=duration as it needs a wiggle room of about 1-2 seconds to operate.

Demo clips are provided that work well together 
