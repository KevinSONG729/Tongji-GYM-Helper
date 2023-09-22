# Badminton Reservation Script for Tongji University Gymnasium

Scripted login using selenium to emulate a browser, implementing a crack for raw character authentication at login.

## Project documents

* config.json

    Parameter settings, including login platform, student number and password, time selection, peer student number, etc.

* STZHONGS.TTF

    Generate the font files needed to match the image, which can be changed according to subsequent changes in requirements.

* decorators.py

    Function decorators for enhanced code robustness and error debugging.

* word_detection_and_match.py

    Login validation core module for secluded character localization and matching.

    Algorithm flow: image hsv->threshold constraints->kmeans clustering->outlier detection->fine kmeans clustering->target box creation->labeled image generation->SIFT feature point extraction and matching->post-processing.

* workflow.py

    A workflow for the badminton reservation process, where the login module can remain unchanged and the workflow functions and destination ip can be adapted to your needs.

## Libraries to install

opencv-python、selenium、sklearn

## Running Instructions

Run workflow.py.If you need a timed task, choose for yourself when you want workflow.py to run.
