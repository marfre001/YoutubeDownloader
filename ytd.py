import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import subprocess
import sys
import datetime

def check_ffmpeg():
    """Checks if FFmpeg is installed and accessible in the system's PATH."""
    try:
        # Use subprocess.run to hide output and only check if the command exists.
        subprocess.run(['ffmpeg', '-version'], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       startupinfo=subprocess.STARTUPINFO() if sys.platform == 'win32' else None)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader Pro")
        
        # Get screen height and set the window to occupy most of it
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"650x{screen_height-200}")
        self.root.resizable(True, True)

        # Interface state variables
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="video")
        self.filename_var = tk.StringVar()
        self.output_dir = tk.StringVar(value=os.getcwd())

        # MP3 audio quality map
        self.audio_quality_map = {
            "Best (VBR ~256k)": "0",
            "High (320 kbps)": "320",
            "Good (192 kbps)": "192",
            "Standard (128 kbps)": "128",
            "Low (96 kbps)": "96",
            "Very Low (64 kbps)": "64",
            "Voice Only (32 kbps)": "32",
        }
        self.audio_quality_var = tk.StringVar(value="Good (192 kbps)")

        # MP4 video quality map (compression)
        self.video_quality_map = {
            "Best available (up to 4K)": 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            "High (1080p)": 'bestvideo[height<=?1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            "Medium (720p)": 'bestvideo[height<=?720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            "Low (480p)": 'bestvideo[height<=?480][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            "Very Low (360p)": 'bestvideo[height<=?360][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        }
        self.video_quality_var = tk.StringVar(value="High (1080p)")

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Configures custom styles for a more professional look."""
        self.style = ttk.Style()
        
        # Try to use modern themes
        try:
            if sys.platform == "win32":
                self.style.theme_use('vista')
            elif sys.platform == "darwin":
                self.style.theme_use('aqua')
            else:
                self.style.theme_use('clam')
        except tk.TclError:
            pass

        # Custom styles
        self.style.configure('Title.TLabel', 
                           font=('Segoe UI', 14, 'bold'),
                           foreground='#2c3e50')
        
        self.style.configure('Heading.TLabel', 
                           font=('Segoe UI', 10, 'bold'),
                           foreground='#34495e')
        
        self.style.configure('Primary.TButton',
                           font=('Segoe UI', 11, 'bold'),
                           padding=(25, 12))
        
        self.style.configure('Secondary.TButton',
                           font=('Segoe UI', 9),
                           padding=(8, 4))

    def create_widgets(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configuration for window resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 25))
        header_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(header_frame, text="🎥 YouTube Downloader Pro", style='Title.TLabel')
        title_label.grid(row=0, column=0)
        
        subtitle_label = ttk.Label(header_frame, text="Download video and audio from YouTube", 
                                 font=('Segoe UI', 9), foreground='#7f8c8d')
        subtitle_label.grid(row=1, column=0, pady=(3, 0))

        # --- URL Input Section ---
        ttk.Label(main_frame, text="Video URL:", style='Heading.TLabel').grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, font=('Segoe UI', 10))
        url_entry.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20), ipady=6)

        # --- Format Section ---
        format_frame = ttk.LabelFrame(main_frame, text="Format", padding="15")
        format_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        format_frame.columnconfigure(0, weight=1)
        
        radio_frame = ttk.Frame(format_frame)
        radio_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Radiobutton(radio_frame, text="🎬 Video (MP4)", 
                       variable=self.format_var, value="video", 
                       command=self.toggle_quality_widgets).pack(side='left', padx=(0, 30))
        
        ttk.Radiobutton(radio_frame, text="🎵 Audio (MP3)", 
                       variable=self.format_var, value="audio", 
                       command=self.toggle_quality_widgets).pack(side='left')

        # --- Quality Section ---
        quality_frame = ttk.LabelFrame(main_frame, text="Quality", padding="15")
        quality_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        quality_frame.columnconfigure(1, weight=1)
        
        ttk.Label(quality_frame, text="Video:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.video_quality_combobox = ttk.Combobox(quality_frame, 
                                                 textvariable=self.video_quality_var, 
                                                 values=list(self.video_quality_map.keys()), 
                                                 state='readonly',
                                                 font=('Segoe UI', 9))
        self.video_quality_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 8))
        
        ttk.Label(quality_frame, text="Audio:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.audio_quality_combobox = ttk.Combobox(quality_frame, 
                                                 textvariable=self.audio_quality_var, 
                                                 values=list(self.audio_quality_map.keys()), 
                                                 state='readonly',
                                                 font=('Segoe UI', 9))
        self.audio_quality_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # --- File Section ---
        file_frame = ttk.LabelFrame(main_frame, text="Destination", padding="15")
        file_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Filename (optional):").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        filename_entry = ttk.Entry(file_frame, textvariable=self.filename_var, font=('Segoe UI', 9))
        filename_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 8), ipady=4)
        
        ttk.Label(file_frame, text="Folder:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        
        dir_frame = ttk.Frame(file_frame)
        dir_frame.grid(row=1, column=1, sticky=(tk.W, tk.E))
        dir_frame.columnconfigure(0, weight=1)
        
        self.dir_label = ttk.Label(dir_frame, text=self.output_dir.get(), 
                                 relief="sunken", anchor="w", font=('Segoe UI', 9))
        self.dir_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 8), ipady=4)
        
        ttk.Button(dir_frame, text="Browse", command=self.browse_directory,
                  style='Secondary.TButton').grid(row=0, column=1)

        # Download Button
        self.download_btn = ttk.Button(main_frame, text="⬇️ DOWNLOAD", 
                                     command=self.start_download, 
                                     style='Primary.TButton')
        self.download_btn.grid(row=6, column=0, columnspan=2, pady=(10, 20))

        # --- Progress Section ---
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="15")
        progress_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate', maximum=100)
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5), ipady=3)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to download", 
                                      font=('Segoe UI', 9))
        self.progress_label.grid(row=1, column=0)

        # --- Log Section ---
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="15")
        log_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
        
        log_container = ttk.Frame(log_frame)
        log_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_container.columnconfigure(0, weight=1)
        log_container.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_container, height=6, wrap=tk.WORD, 
                              font=('Consolas', 8),
                              relief="sunken", borderwidth=1)
        scrollbar = ttk.Scrollbar(log_container, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Initialize state
        self.toggle_quality_widgets()

    def toggle_quality_widgets(self):
        """Enables or disables the quality menus based on the format selection."""
        if self.format_var.get() == "audio":
            self.audio_quality_combobox.config(state='readonly')
            self.video_quality_combobox.config(state='disabled')
        else: # "video"
            self.audio_quality_combobox.config(state='disabled')
            self.video_quality_combobox.config(state='readonly')

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)
            self.dir_label.config(text=directory)

    def log_message(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def update_progress(self, percentage, status=""):
        self.progress['value'] = percentage
        status_text = f"{status} {int(percentage)}%" if status else f"{int(percentage)}%"
        self.progress_label.config(text=status_text)
        self.root.update_idletasks()

    def reset_progress(self):
        self.progress['value'] = 0
        self.progress_label.config(text="Ready to download")
        self.root.update_idletasks()

    def start_download(self):
        """'Gatekeeper' function: performs preliminary checks and starts the download thread."""
        if not self.url_var.get().strip():
            messagebox.showerror("Error", "Please enter a valid URL!")
            return

        if self.format_var.get() == 'audio':
            if not check_ffmpeg():
                self.log_message("✗ ERROR: FFmpeg not found or not configured in PATH.")
                messagebox.showerror(
                    "FFmpeg Not Found",
                    "FFmpeg is required to download in MP3 format. "
                    "Please ensure it is installed and configured in your system's PATH."
                )
                return

        # Disable the button during download
        self.download_btn.config(state='disabled', text='⏳ Downloading...')
        
        # Start the download in a separate thread to avoid blocking the GUI
        threading.Thread(target=self.download_video, daemon=True).start()

    def download_video(self):
        """Worker function that handles the download process."""
        try:
            self.reset_progress()
            self.update_progress(0, "Initializing...")

            url = self.url_var.get().strip()
            format_type = self.format_var.get()
            custom_filename = self.filename_var.get().strip()
            output_dir = self.output_dir.get()

            self.log_message("Starting download with yt-dlp...")
            self.download_with_ytdlp(url, format_type, custom_filename, output_dir)

        except Exception as e:
            self.log_message(f"CRITICAL ERROR: {str(e)}")
            messagebox.showerror("Critical Error", f"An unexpected error occurred:\n{str(e)}")
        finally:
            self.reset_progress()
            # Re-enable the button
            self.download_btn.config(state='normal', text='⬇️ DOWNLOAD')

    def download_with_ytdlp(self, url, format_type, filename, output_dir):
        try:
            import yt_dlp

            def progress_hook(d):
                if d['status'] == 'downloading':
                    total = d.get('total_bytes') or d.get('total_bytes_estimate')
                    if total:
                        percent = (d['downloaded_bytes'] / total) * 100
                        self.update_progress(percent * 0.9, "Downloading...") # Download is 90% of the process
                elif d.get('postprocessor'):
                    self.update_progress(95, "Converting/Merging...")

            ydl_opts = {
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'noplaylist': True,
            }

            if filename:
                ydl_opts['outtmpl'] = os.path.join(output_dir, f'{filename}.%(ext)s')

            if format_type == "audio":
                selected_quality_text = self.audio_quality_var.get()
                quality_value = self.audio_quality_map.get(selected_quality_text, '192')
                self.log_message(f"MP3 format, quality: {selected_quality_text}")

                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality_value,
                    }],
                })
            else: # Video
                selected_quality_text = self.video_quality_var.get()
                format_code = self.video_quality_map.get(selected_quality_text)
                self.log_message(f"MP4 Video format, quality: {selected_quality_text}")
                ydl_opts['format'] = format_code

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.update_progress(100, "Completed!")
            self.log_message("✓ Download completed successfully!")
            messagebox.showinfo("Success", "Download complete!")

        except ImportError:
            self.log_message("✗ ERROR: The 'yt-dlp' library is not installed.")
            messagebox.showerror("Library Error", "The yt-dlp library is not installed.\n\nTo install it, open a terminal or command prompt and type:\npip install yt-dlp")
        except Exception as e:
            self.log_message(f"✗ Error with yt-dlp: {str(e)}")
            messagebox.showerror("yt-dlp Error", f"An error occurred during the download:\n{str(e)}")


def main():
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()