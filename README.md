# Face Authentication & Liveness — Personal Project

A small, fun desktop app for experimenting with face verification and a simple liveness routine (eye closure + peace-sign). Built from OpenCV, dlib/face_recognition, MediaPipe and PyQt5.

## What it does
- Step 1: Upload and save a reference face (encoding + preview).
- Step 2: Authenticate — verifies the face, then runs two liveness checks:
  - Close your eyes for 2 seconds.
  - Show a peace sign (index + middle fingers) and hold for 2 seconds.
- Each step has a 15-second window with an on-screen timer and clear instructions.

## Quick starter
Clone this repo, then from the project folder run (macOS / zsh):

```bash
# create + activate a virtualenv
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# run the app
python faceauth_app.py
```

If `PyQt5` or `dlib` fail to install on macOS, you may need Homebrew build deps:

```bash
brew install cmake boost
# optional: help with PyQt5 wheels
brew install qt
python -m pip install PyQt5
```

## Files you’ll care about
- `faceauth_app.py` — GUI front-end (PyQt5).
- `save_face.py` — helper to save a reference face.
- `verify_face.py` — face verification view.
- `liveness_check.py` — eye + hand liveness logic.
- `requirements.txt` — Python packages used.

Runtime artifacts (don’t commit these):
- `saved_face.npy` — saved face encoding created by the app.
- `saved_face_preview.jpg` — saved preview image.

## Tips & notes
- Keep large model files (e.g. `shape_predictor_68_face_landmarks.dat`) out of git — add them to `.gitignore` and load them at runtime instead.
- If you get `ModuleNotFoundError: No module named 'PyQt5'`, activate the venv and run `python -m pip install PyQt5`.
- If a `git push` fails because of large objects, use Git LFS for binaries or remove large blobs from history with `git-filter-repo` or BFG.

## Make it yours
- Tweak the UI text, change the timers, or swap liveness checks for something else (smile detection, head nod).
- Add a tiny web UI or an API to integrate with other tools.

## License
This repo uses the MIT license
