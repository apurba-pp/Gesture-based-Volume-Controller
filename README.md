# Gesture-based-Volume-Controller
#### The project uses openCV to detect the distances between "the tip of thumb" and "the tip of index finger" (in further discussion refered as "finger tips"). Then pycaw is used to proportionate the previously mentioned distance with our system volume.<br> The [Handtrackmodule](https://github.com/apurba-pp/Gesture-based-Volume-Controller/blob/6c0948ef3a5d25144141543a1a2f8ead63f46bed/src/Handtrackmodule.py) in src helps to return back the live location of any of the 21 points present in our hand.<br><br>

### ***How is this project unique?***
#### In this project the volume depends on the real world distance of finger tips and not the on-screen distance of finger tips.<br> ***Example:*** _If the real world distance of finger tips is "x" then the volume remains almost the same with any on-screen distance of finger tips i.e. "y1, y2, y3, etc._"
