# 🎬 YouTube Downloader Pro

A user-friendly, standalone desktop application for Windows to download video and audio from YouTube. Built with Python, Tkinter, and `yt-dlp`.


![image](https://github.com/user-attachments/assets/88d5597c-ad07-438d-acbc-2d56517e4255)


---

## ✨ Features

- **Simple & Intuitive GUI**: A clean and modern interface that is easy for anyone to use.
- **Video & Audio Downloads**: Choose between downloading a full video (`MP4`) or extracting just the audio (`MP3`).
- **Quality Selection**:
    - **Video**: Select from various resolutions, from 360p up to 4K.
    - **Audio**: Choose your desired MP3 bitrate, from 32kbps to 320kbps.
- **Custom Filenames**: Optionally set a custom name for your downloaded files.
- **Destination Picker**: Easily browse and select the folder where you want to save your files.
- **Real-time Progress**: Monitor download progress with a visual progress bar and a detailed status label.
- **Activity Log**: A log window shows detailed messages from `yt-dlp`, useful for status updates and troubleshooting.
- **Standalone & Portable**: The application runs from a self-contained folder using an embedded Python interpreter, requiring no prior Python installation on the user's system.
- **Automatic FFmpeg Setup**: Includes a simple script to automatically download and configure FFmpeg, which is required for audio conversion.

---

## 🚀 Getting Started

Follow these simple steps to get the application running on your Windows machine.

### Prerequisites

- A **Windows** operating system (7, 8, 10, 11).
- An active **internet connection** for downloading videos and FFmpeg.

### Installation & Usage

1.  **Download the Application**
    - Go to the [**Releases**](https://github.com/your-username/your-repo-name/releases) page of this repository.
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
    - A terminal window will open first, followed by the application's main window.
    - **Important**: Do not close the black terminal window while the app is running!

---

## 🔧 How It Works (Technical Details)

This project is designed to be as user-friendly as possible by bundling its dependencies.

-   **Embedded Python**: The application uses a portable, embedded version of **Python 3.10.11**. This means users don't need to have Python installed on their system. The `Start_App.bat` script ensures that this specific interpreter is used to run the application.
-   **Core Downloader**: The heavy lifting of downloading and processing is done by the excellent [**`yt-dlp`**](https://github.com/yt-dlp/yt-dlp) library, a powerful and actively maintained fork of `youtube-dl`.
-   **Graphical User Interface (GUI)**: The interface is built using **Tkinter**, Python's standard GUI toolkit, with `ttk` for a more modern look and feel.
-   **Batch Scripts**:
    -   `Install_FFmpeg.bat`: A helper script that downloads the latest "essentials" build of FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extracts it to `%LOCALAPPDATA%\FFmpeg`, and permanently adds its `bin` directory to the user's `PATH`. This makes FFmpeg accessible to `yt-dlp` for audio conversion.
    -   `Start_App.bat`: This script sets the `PYTHONHOME` environment variable to point to the embedded Python folder and then executes the `ytd.py` script, ensuring all dependencies are found correctly.

---

## 📂 File Structure

```
.
├── python/                   # Embedded Python 3.10.11 interpreter and libraries
├── ytd.py                    # The main application source code
├── guide.html                # A detailed user guide (in English)
├── Install_FFmpeg.bat        # Script to automatically install FFmpeg
├── Start_App.bat             # Script to launch the application
└── README.md                 # This file
```

---

## ⚠️ Disclaimer

This tool is for personal and educational use only. Downloading copyrighted content without permission may be illegal in your country. The developers of this application are not responsible for its misuse. Please respect copyright laws and YouTube's terms of service.
