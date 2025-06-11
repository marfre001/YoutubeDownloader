# 🎬 YouTube Downloader Pro

A user-friendly, standalone desktop application for Windows to download video and audio from YouTube. Built with Python, Tkinter, and `yt-dlp`.

---

## ✨ Features

- **Simple & Intuitive GUI**: A clean and modern interface that is easy for anyone to use.
- **Video & Audio Downloads**: Choose between downloading a full video (`MP4`) or extracting just the audio (`MP3`).
- **🚀 Automatic Updates**: Automatically checks for and installs the latest version of the core `yt-dlp` downloader on startup to keep up with YouTube's changes.
- **🔎 Dynamic Format Checking**: Fetches the actual available video qualities for a specific URL, preventing "format not available" errors.
- **📱 Responsive & Scrollable Interface**: The GUI adapts to different screen sizes and becomes scrollable if the content doesn't fit, ensuring usability on laptops and smaller displays.
- **Quality Selection**:
    - **Video**: Select from a dynamically generated list of available resolutions for that specific video.
    - **Audio**: Choose your desired MP3 bitrate, from 32kbps to 320kbps.
- **Custom Filenames & Destination**: Optionally set a custom name and choose the folder where you want to save your files.
- **Real-time Progress**: Monitor download progress with a visual progress bar and a detailed status label.
- **Activity Log**: A log window shows detailed messages from `yt-dlp`, useful for status updates and troubleshooting.
- **Standalone & Portable**: The application runs from a self-contained folder using an embedded Python interpreter, requiring no prior Python installation on the user's system.
- **Automatic FFmpeg Setup**: Includes a simple script to automatically download and configure FFmpeg, which is required for audio conversion.

---

## 🚀 Getting Started

Follow these simple steps to get the application running on your Windows machine.

### Prerequisites

- A **Windows** operating system (7, 8, 10, 11).
- An active **internet connection** for downloading videos, FFmpeg, and application updates.

### Installation & Usage

1.  **Download the Application**
    - Go to the [**Releases**]((https://github.com/marfre001/YoutubeDownloader/releases/tag/v1.0)) page of this repository.
    - Download the latest `YouTube-Downloader-Pro.zip` file.
    - Extract the contents of the ZIP file to a folder on your computer (e.g., on your Desktop).

2.  **Install FFmpeg (One-Time Setup)**
    - Before downloading audio, you need FFmpeg. We've made this easy!
    - Open the extracted folder and double-click on `Install_FFmpeg.bat`.
    - A command prompt window will appear and guide you through the automatic download and setup.
    - **⚠️ Windows SmartScreen Warning:** Windows might show a security warning. This is normal for batch scripts. Click **"More info"** and then **"Run anyway"** to proceed.
    - This step only needs to be done once.

3.  **Run the Application**
    - To start the downloader, double-click the `Start_App.bat` file.
    - A small **"Loading" window** will appear first. It's checking for updates for the downloader component. This might take a few seconds. The main application will launch automatically afterward.
    - **Important**: Do not close the black terminal window that opens in the background while the app is running!

---

## 🔧 How It Works (Technical Details)

This project is designed to be as user-friendly as possible by bundling its dependencies.

-   **Embedded Python**: The application uses a portable, embedded version of **Python**. This means users don't need to have Python installed on their system.
-   **Core Downloader**: The heavy lifting of downloading and processing is done by the excellent [**`yt-dlp`**](https://github.com/yt-dlp/yt-dlp) library.
-   **Graphical User Interface (GUI)**: The interface is built using **Tkinter**, Python's standard GUI toolkit, with `ttk` for a more modern look and feel. The main window features a scrollable canvas to ensure usability on all screen resolutions.
-   **Batch Scripts**:
    -   `Install_FFmpeg.bat`: A helper script that downloads the latest "essentials" build of FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extracts it to `%LOCALAPPDATA%\FFmpeg`, and permanently adds its `bin` directory to the user's `PATH`.
    -   `Start_App.bat`: This script launches `ytd.py`. The Python script first displays a loading screen while a background thread runs `python -m pip install --upgrade yt-dlp` to ensure the core downloader is always up-to-date. Once complete, it launches the main Tkinter application.

---

## 📂 File Structure
Use code with caution.
Markdown
.
├── python/ # Embedded Python interpreter and libraries
├── ytd.py # The main application source code
├── guide.html # A detailed user guide (in Italian)
├── Install_FFmpeg.bat # Script to automatically install FFmpeg
├── Start_App.bat # Script to launch the application
└── README.md # This file
---

## ⚠️ Disclaimer

This tool is for personal and educational use only. Downloading copyrighted content without permission may be illegal in your country. The developers of this application are not responsible for its misuse. Please respect copyright laws and YouTube's terms of service.
