# Repository Description

This repository contains a user-friendly desktop application for Windows that allows users to download video and audio from YouTube.

## Key Features

*   **Graphical User Interface (GUI):** A simple and intuitive interface built with Tkinter, making it easy for users to navigate and use the application.
*   **Video and Audio Downloads:** Users can choose to download full videos in MP4 format or extract audio in MP3 format.
*   **Quality Selection:** The application allows users to select their preferred video resolution and audio bitrate from available options.
*   **Automatic yt-dlp Updates:** The core downloader component, `yt-dlp`, automatically checks for updates and installs the latest version on startup. This ensures compatibility with YouTube's ongoing changes.
*   **FFmpeg Setup:** Includes a helper script (`Install_FFmpeg.bat`) to automate the download and configuration of FFmpeg, which is necessary for audio conversion.
*   **Dynamic Format Checking:** The application dynamically fetches available video qualities for a given YouTube URL, preventing errors related to unavailable formats.
*   **Responsive and Scrollable Interface:** The GUI is designed to adapt to different screen sizes and includes a scrollable area to ensure all content is accessible.
*   **Custom Filenames and Destination:** Users can specify custom filenames and choose their desired download folder.
*   **Real-time Progress and Logging:** A progress bar and status labels provide real-time feedback during downloads. A log window displays detailed messages from `yt-dlp` for troubleshooting.
*   **Standalone and Portable:** The application is designed to run from a self-contained folder using an embedded Python interpreter, meaning users don't need to install Python separately.

## Technologies Used

*   **Python:** The primary programming language for the application.
*   **Tkinter:** Python's standard GUI library, used to create the application's user interface.
*   **yt-dlp:** A powerful command-line program to download videos from YouTube and other video sites. This project uses `yt-dlp` as its core downloading engine.

## File Structure

*   **`ytd.py`:** The main Python script containing the application's logic, including the GUI, download functions, and interaction with `yt-dlp`.
*   **`Install_FFmpeg.bat`:** A batch script for Windows users to easily download and set up FFmpeg, which is required for audio extraction and conversion.
*   **`Start_App.bat`:** A batch script for Windows users to launch the YouTube Downloader application. It also handles the automatic update of `yt-dlp`.
*   **`README.md`:** Provides a comprehensive overview of the project, including features, installation instructions, and technical details.
*   **`guide.html`:** A user guide, likely providing detailed instructions on how to use the application (noted to be in Italian in the `README.md`).
*   **`python/` (directory):** Contains the embedded Python interpreter and necessary libraries, making the application portable.
*   **`.gitignore`:** Specifies intentionally untracked files that Git should ignore.
*   **`LICENSE`:** Contains the licensing information for the project.
