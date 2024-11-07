# Development Set-up

## Prerequisites

Before starting, make sure you have the following installed:

1. **Python** (version 3.x)
   - [Download Python](https://www.python.org/downloads/) if it is not already installed.

2. **Chrome or Chromium Browser**
   - This extension requires Chrome to run.
   - [Download Chrome](https://www.google.com/chrome/) if needed.

3. **Python Packages**
   - Install required Python packages by running:
     ```bash
     pip install requests flask flask-cors pandas scikit-learn stop-words joblib
     ```

## Instructions

1. **Load the Chrome Extension**:
   - Open Chrome and navigate to `chrome://extensions/`.
   - Enable "Developer Mode" (usually found in the upper right corner).
   - Select "Load unpacked" and choose the `extension` folder in the `code` folder.

2. **Run the Local Server**:
   - Run the server by executing the `server.bat` file in the `code` folder. This will start the local server that the extension communicates with.

3. **Using the Extension**:
   - Paste a valid Shopee link into the extension's text box.
   - Click "Analyze" and wait for the extension to process the link and display results.

