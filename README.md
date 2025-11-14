# Face Authentication & Liveness Demo

Simple desktop app demonstrating face enrollment, face verification and a two-step liveness check (eye closure + peace-sign hand gesture). Built with OpenCV, dlib / face_recognition, MediaPipe and PyQt5.

## Features
- Step 1: Upload & save a reference face (saves encoding + preview)
- Step 2: Authenticate — verifies face then runs liveness:
  - Eye-closure (close eyes for 2s)
  - Peace sign gesture (hold index + middle fingers for 2s)
- Per-step 15s timer and prominent on-screen instructions
- UI with progress, logs and Reset button to clear state

## Files of interest
- `faceauth_app.py` — PyQt5 GUI and app flow
- `save_face.py` — face enrollment / save reference encoding
- `verify_face.py` — face verification UI & logic
- `liveness_check.py` — liveness detector (eyes + hand)
- `requirements.txt` — Python deps

Generated at runtime (do not commit):
- `saved_face.npy` — stored face encoding
- `saved_face_preview.jpg` — preview image

## Requirements
- macOS (instructions use zsh)
- Python 3.8+
- Recommended: virtual environment

Dependencies (see `requirements.txt`):
- face_recognition, dlib, opencv-python, numpy, PyQt5, imutils, mediapipe, scipy

## Install & run (recommended)
Open a terminal in the project folder:

1. Create and activate venv
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Upgrade pip and install requirements
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. If dlib or PyQt5 fail to install, install prerequisites:
```bash
# common macOS build deps
brew install cmake boost

# optional: if PyQt5 wheel fails
brew install qt
python -m pip install PyQt5
```

4. Run the app
```bash
python faceauth_app.py
```

## Usage
1. Click "Step 1: Upload and Save Face" — choose an image with a clear face. On success the button turns green and is disabled.
2. Click "Step 2: Authenticate" — this runs face verification then the liveness checks. Each step has a 15s window. Buttons turn green and disable on success.
3. Click "Reset" to clear saved files and return to start state.

Notes:
- On-screen instructions are always visible, timers appear top-right for each phase.
- If no face/hands are detected the instructions remain visible (so users know what to do).

## Troubleshooting
- ModuleNotFoundError: No module named 'PyQt5' — activate venv and run `python -m pip install PyQt5` (or use conda).
- dlib / face_recognition installation errors — ensure `cmake` and `boost` are installed via Homebrew before `pip install dlib`.
- Large model files (e.g. `shape_predictor_68_face_landmarks.dat`) should NOT be committed to git. Keep them external and reference their paths in code or add to `.gitignore`.

## Git / Repo tips
- Do not commit generated files (`saved_face.npy`, preview image) or large model binaries. Use `.gitignore` or Git LFS for required large assets.
- If a push fails due to a large pack, find large blobs and move them to LFS or strip them from history (tools: BFG, git-filter-repo).

## License
MIT

## Contact / Next steps
- To improve reliability, consider:
  - adding retries / better error handling around camera access
  - making model paths configurable via environment variables
  - moving large pre-trained models to an external download step
