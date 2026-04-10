#Firmware

This file describes how to update the Engi 1020 firmware to work with the TM1637 segmented display for our Engi 1020 bomb defusal project:

First, open up the engi 1020 library you have pip installed. On Windows, it is in %appdata%, which is a hidden folder, so you need to do extra work to find it. Once you locate it, find the api.py file. Replace this with the file on GitHub (You could also just open up the file on the github in VS Code,  and then open up the declaration in VS Code for api.py and change it there by copying and pasting the changes, as for this file, the only change is on line 10, where tm1637_write is also imported).

Then, find the io.py file and replace it with the one on GitHub.  Or do the same as for api.py: Just copy and paste the changes. The changes for this file are a bit more; there’s just another function defined at the bottom of the file from lines 89 to 104, so just copy and paste this function, and you should be good.

Now that's it for the front end. Now flash the new firmware on the Grove Kit. First, install PlatformIO for your VS Code as an extension. Then download the firmware (also on GitHub), unzip it and open it up in VS Code. Then simply upload it to the Grove Kit using the PlatformIO extension, and the timer module should be good to go :)
