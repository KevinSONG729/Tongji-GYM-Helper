# Badminton Reservation Script for Tongji University Gymnasium

Scripted login using selenium to emulate a browser, implementing a crack for raw character authentication at login.

## Project documents

* config.json

    Parameter settings, including login platform, student number and password, time selection, peer student number, etc.

* STZHONGS.TTF

    Generate the font files needed to match the image, which can be changed according to subsequent changes in requirements.

    The fonts can not be used directly under linux system, you need to install the fonts:

```
sudo apt update && sudo apt install ttf-mscorefonts-installer
sudo fc-cache -f -v
```

* decorators.py

    Function decorators for enhanced code robustness and error debugging.

* word_detection_and_match.py

    Login validation core module for secluded character localization and matching.

    Algorithm flow: image hsv->threshold constraints->kmeans clustering->outlier detection->fine kmeans clustering->target box creation->labeled image generation->SIFT feature point extraction and matching->post-processing.

* workflow.py

    A workflow for the badminton reservation process, where the login module can remain unchanged and the workflow functions and destination ip can be adapted to your needs.

## Libraries to install

opencv-python、selenium、scikit-learn、matplotlib

## Running Instructions

Run workflow.py.If you need a timed task, choose for yourself when you want workflow.py to run.

## Progress

#### #2023.09.23 Update:

* Enhance the robustness and readability of the algorithm, and the configuration file's choice of venue and time matches the corresponding name of the site.
* Enhanced the precision of character matching.
* Support LINUX to run without interface, but must ensure that the platform is Firefox and firefox_driver_bin_location is set to the path of geckodriver (which has been placed in the same level directory).
