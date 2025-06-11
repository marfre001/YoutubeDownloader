# --- START OF FILE ytd.py ---

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import subprocess
import sys
import datetime
import re

# ... (Le funzioni check_ffmpeg, run_main_app, update_yt_dlp, e main rimangono invariate) ...
# ... (Assicurati di avere la versione precedente completa) ...

def check_ffmpeg():
    """Checks if FFmpeg is installed and accessible in the system's PATH."""
    try:
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
        
        # --- MODIFICA: Rimuoviamo l'altezza fissa e impostiamo una dimensione minima ---
        # Questo permette alla finestra di essere più piccola su schermi con bassa risoluzione.
        self.root.minsize(600, 550) 
        
        # Interface state variables
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="video")
        self.filename_var = tk.StringVar()
        self.output_dir = tk.StringVar(value=os.getcwd())

        # MP3 audio quality map (static)
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

        self.video_quality_map = {}
        self.video_quality_var = tk.StringVar()

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        try:
            if sys.platform == "win32":
                self.style.theme_use('vista')
            elif sys.platform == "darwin":
                self.style.theme_use('aqua')
            else:
                self.style.theme_use('clam')
        except tk.TclError:
            pass

        self.style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#2c3e50')
        self.style.configure('Heading.TLabel', font=('Segoe UI', 10, 'bold'), foreground='#34495e')
        self.style.configure('Primary.TButton', font=('Segoe UI', 11, 'bold'), padding=(25, 12))
        self.style.configure('Secondary.TButton', font=('Segoe UI', 9), padding=(8, 4))

    def create_widgets(self):
        # --- MODIFICA PRINCIPALE: Creazione di un'area scorrevole ---

        # 1. Frame principale che conterrà il Canvas e la Scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # 2. Creazione del Canvas e della Scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.grid(row=0, column=1, sticky='ns')
        canvas.grid(row=0, column=0, sticky='nsew')

        # 3. Creazione del frame interno che conterrà tutti i widget
        self.scrollable_frame = ttk.Frame(canvas, padding="25")
        self.scrollable_frame_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # 4. Funzioni per far funzionare lo scrolling e il ridimensionamento
        def on_frame_configure(event):
            # Aggiorna la scrollregion del canvas per includere tutto il contenuto
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            # Ridimensiona il frame interno per riempire la larghezza del canvas
            canvas.itemconfig(self.scrollable_frame_window, width=event.width)

        self.scrollable_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        
        # Configurazione del layout per il frame scorrevole
        self.scrollable_frame.columnconfigure(1, weight=1)

        # --- Da qui in poi, tutti i widget vengono aggiunti a 'self.scrollable_frame' ---

        # Header
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 25))
        header_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(header_frame, text="🎥 YouTube Downloader Pro", style='Title.TLabel')
        title_label.grid(row=0, column=0)
        
        subtitle_label = ttk.Label(header_frame, text="Download video and audio from YouTube", 
                                 font=('Segoe UI', 9), foreground='#7f8c8d')
        subtitle_label.grid(row=1, column=0, pady=(3, 0))

        # --- URL Input Section ---
        ttk.Label(self.scrollable_frame, text="Video URL:", style='Heading.TLabel').grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        url_entry_frame = ttk.Frame(self.scrollable_frame)
        url_entry_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        url_entry_frame.columnconfigure(0, weight=1)

        url_entry = ttk.Entry(url_entry_frame, textvariable=self.url_var, font=('Segoe UI', 10))
        url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), ipady=6, padx=(0, 10))

        self.fetch_btn = ttk.Button(url_entry_frame, text="Verifica Formati", 
                                    command=self.fetch_formats_thread, style='Secondary.TButton')
        self.fetch_btn.grid(row=0, column=1, sticky=tk.E)

        # --- Format Section ---
        format_frame = ttk.LabelFrame(self.scrollable_frame, text="Format", padding="15")
        format_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
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
        quality_frame = ttk.LabelFrame(self.scrollable_frame, text="Quality", padding="15")
        quality_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        quality_frame.columnconfigure(1, weight=1)
        
        ttk.Label(quality_frame, text="Video:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.video_quality_combobox = ttk.Combobox(quality_frame, 
                                                 textvariable=self.video_quality_var, 
                                                 state='disabled',
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
        file_frame = ttk.LabelFrame(self.scrollable_frame, text="Destination", padding="15")
        file_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
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
        self.download_btn = ttk.Button(self.scrollable_frame, text="⬇️ DOWNLOAD", 
                                     command=self.start_download, 
                                     style='Primary.TButton',
                                     state='disabled')
        self.download_btn.grid(row=6, column=0, columnspan=3, pady=(10, 20))

        # --- Progress Section ---
        progress_frame = ttk.LabelFrame(self.scrollable_frame, text="Progress", padding="15")
        progress_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate', maximum=100)
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5), ipady=3)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready. Inserisci un URL e verifica i formati.", 
                                      font=('Segoe UI', 9))
        self.progress_label.grid(row=1, column=0)

        # --- Log Section ---
        log_frame = ttk.LabelFrame(self.scrollable_frame, text="Log", padding="15")
        log_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        # La riga del log non deve più espandersi verticalmente, ci pensa lo scroll
        # self.scrollable_frame.rowconfigure(8, weight=1) 
        
        log_container = ttk.Frame(log_frame)
        log_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_container.columnconfigure(0, weight=1)
        log_container.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_container, height=8, wrap=tk.WORD, # Aumentiamo un po' l'altezza di default
                              font=('Consolas', 8),
                              relief="sunken", borderwidth=1)
        log_scrollbar = ttk.Scrollbar(log_container, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Initialize state
        self.toggle_quality_widgets()

    # ... (Tutti gli altri metodi della classe rimangono invariati) ...
    def toggle_quality_widgets(self):
        if self.format_var.get() == "audio":
            self.audio_quality_combobox.config(state='readonly')
            self.video_quality_combobox.config(state='disabled')
            self.download_btn.config(state='normal')
        else: # "video"
            self.audio_quality_combobox.config(state='disabled')
            if self.video_quality_map:
                self.video_quality_combobox.config(state='readonly')
                self.download_btn.config(state='normal')
            else:
                self.video_quality_combobox.config(state='disabled')
                self.download_btn.config(state='disabled')

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
        self.progress_label.config(text="Pronto per un nuovo download.")
        self.root.update_idletasks()

    def fetch_formats_thread(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL!")
            return

        self.fetch_btn.config(state='disabled', text='Verifica...')
        self.download_btn.config(state='disabled')
        self.log_message(f"Verifica formati per: {url}")
        self.progress_label.config(text="Verifica formati disponibili...")
        
        self.video_quality_map.clear()
        self.video_quality_combobox.set('')
        self.video_quality_combobox['values'] = []

        threading.Thread(target=self.fetch_formats, args=(url,), daemon=True).start()

    def fetch_formats(self, url):
        try:
            import yt_dlp
            ydl_opts = {'quiet': True, 'noplaylist': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
            
            available_heights = set()
            for f in info_dict.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('ext') == 'mp4' and f.get('height'):
                    available_heights.add(f['height'])

            if not available_heights:
                self.log_message("✗ Nessun formato video MP4 trovato per questo URL.")
                messagebox.showerror("Errore", "Nessun formato video MP4 compatibile trovato.")
                return

            self.video_quality_map.clear()
            self.video_quality_map["Best Available (fino a 4K)"] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            
            for height in sorted(list(available_heights), reverse=True):
                label = f"{height}p"
                selector = f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                if label not in self.video_quality_map:
                    self.video_quality_map[label] = selector
            
            self.log_message(f"✓ Trovati {len(self.video_quality_map)} opzioni di qualità video.")
            self.root.after(0, self.update_video_quality_list)

        except ImportError:
            self.log_message("✗ ERRORE: La libreria 'yt-dlp' non è installata.")
            messagebox.showerror("Errore Libreria", "La libreria yt-dlp non è installata.\n\nPer installarla, apri un terminale e digita:\npip install yt-dlp")
        except Exception as e:
            self.log_message(f"✗ Errore durante la verifica dei formati: {str(e)}")
            messagebox.showerror("Errore", f"Impossibile verificare i formati.\nL'URL è valido? C'è connessione a internet?\n\nDettagli: {str(e)}")
        finally:
            self.fetch_btn.config(state='normal', text='Verifica Formati')
            self.progress_label.config(text="Pronto. Seleziona un formato e scarica.")

    def update_video_quality_list(self):
        def sort_key(x):
            if "Best" in x: return 0
            return -int(x.split('p')[0])

        formats = sorted(self.video_quality_map.keys(), key=sort_key)
        
        self.video_quality_combobox['values'] = formats
        if formats:
            self.video_quality_combobox.set(formats[0])
            self.video_quality_combobox.config(state='readonly')
            if self.format_var.get() == 'video':
                self.download_btn.config(state='normal')

    def start_download(self):
        if not self.url_var.get().strip():
            messagebox.showerror("Error", "Please enter a valid URL!")
            return

        if self.format_var.get() == 'video' and not self.video_quality_var.get():
            messagebox.showerror("Error", "Per favore, verifica i formati video disponibili prima di scaricare.")
            return

        if self.format_var.get() == 'audio':
            if not check_ffmpeg():
                self.log_message("✗ ERRORE: FFmpeg non trovato o non configurato nel PATH.")
                messagebox.showerror(
                    "FFmpeg Not Found",
                    "FFmpeg è richiesto per scaricare in formato MP3. "
                    "Assicurati che sia installato e configurato nel PATH di sistema."
                )
                return

        self.download_btn.config(state='disabled', text='⏳ Downloading...')
        self.fetch_btn.config(state='disabled')
        
        threading.Thread(target=self.download_video, daemon=True).start()

    def download_video(self):
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
            self.download_btn.config(state='normal', text='⬇️ DOWNLOAD')
            self.fetch_btn.config(state='normal')
            self.toggle_quality_widgets()

    def download_with_ytdlp(self, url, format_type, filename, output_dir):
        try:
            import yt_dlp

            def progress_hook(d):
                if d['status'] == 'downloading':
                    total = d.get('total_bytes') or d.get('total_bytes_estimate')
                    if total:
                        percent = (d['downloaded_bytes'] / total) * 100
                        self.update_progress(percent * 0.9, "Downloading...")
                elif d.get('postprocessor'):
                    self.update_progress(95, "Converting/Merging...")

            ydl_opts = {
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'noplaylist': True,
                'socket_timeout': 20,
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
                
                if not format_code:
                    self.log_message(f"✗ ERRORE: Opzione di qualità '{selected_quality_text}' non valida.")
                    messagebox.showerror("Errore", f"L'opzione di qualità selezionata '{selected_quality_text}' non è valida. Riprova a verificare i formati.")
                    return

                self.log_message(f"MP4 Video format, quality: {selected_quality_text}")
                ydl_opts['format'] = format_code

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.update_progress(100, "Completed!")
            self.log_message("✓ Download completed successfully!")
            messagebox.showinfo("Success", "Download complete!")

        except ImportError:
            self.log_message("✗ ERRORE: La libreria 'yt-dlp' non è installata.")
            messagebox.showerror("Errore Libreria", "La libreria yt-dlp non è installata.\n\nPer installarla, apri un terminale o command prompt e digita:\npip install yt-dlp")
        except Exception as e:
            error_message = str(e)
            clean_error = re.sub(r'\x1b\[[0-9;]*m', '', error_message)
            self.log_message(f"✗ Errore con yt-dlp: {clean_error}")
            messagebox.showerror("yt-dlp Error", f"An error occurred during the download:\n{clean_error}")

def run_main_app():
    """Crea e avvia la finestra principale dell'applicazione."""
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

def update_yt_dlp(loading_window, status_label, on_complete_callback):
    """
    Trova l'interprete Python portatile e aggiorna yt-dlp.
    Questa funzione è progettata per essere eseguita in un thread separato.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        python_exe = os.path.join(script_dir, 'python', 'python.exe')

        if not os.path.exists(python_exe):
            status_label.config(text="Errore: python.exe non trovato!")
            messagebox.showerror("Errore Critico", f"L'interprete Python non è stato trovato nel percorso atteso:\n{python_exe}")
            loading_window.destroy()
            return

        status_label.config(text="Aggiornamento di yt-dlp in corso...")
        loading_window.update_idletasks()

        command = [python_exe, "-m", "pip", "install", "--upgrade", "yt-dlp"]
        
        startupinfo = None
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        result = subprocess.run(command, capture_output=True, text=True, check=False, startupinfo=startupinfo)

        if result.returncode != 0:
            print(f"ATTENZIONE: Impossibile aggiornare yt-dlp. Errore:\n{result.stderr}")
            status_label.config(text="Avvio dell'applicazione...")
        else:
            print("yt-dlp è aggiornato.")
            status_label.config(text="Avvio dell'applicazione...")

    except Exception as e:
        print(f"Errore imprevisto durante l'aggiornamento: {e}")
        messagebox.showwarning("Avviso Aggiornamento", f"Non è stato possibile verificare gli aggiornamenti per yt-dlp.\nL'app potrebbe non funzionare correttamente.\n\nDettagli: {e}")
    finally:
        loading_window.after(500, on_complete_callback)

def main():
    """Funzione principale che gestisce la finestra di caricamento e l'aggiornamento."""
    loading_root = tk.Tk()
    loading_root.title("Avvio in corso")
    loading_root.geometry("350x100")
    loading_root.resizable(False, False)
    
    screen_width = loading_root.winfo_screenwidth()
    screen_height = loading_root.winfo_screenheight()
    x = (screen_width / 2) - (350 / 2)
    y = (screen_height / 2) - (100 / 2)
    loading_root.geometry(f'+{int(x)}+{int(y)}')

    status_label = ttk.Label(loading_root, text="Verifica aggiornamenti per yt-dlp...", font=('Segoe UI', 10))
    status_label.pack(pady=20)
    
    progress = ttk.Progressbar(loading_root, mode='indeterminate')
    progress.pack(padx=20, fill=tk.X)
    progress.start(10)

    def start_app_and_close_loading():
        """Distrugge la finestra di caricamento e avvia l'app principale."""
        loading_root.destroy()
        run_main_app()

    update_thread = threading.Thread(
        target=update_yt_dlp,
        args=(loading_root, status_label, start_app_and_close_loading),
        daemon=True
    )
    update_thread.start()

    loading_root.mainloop()


if __name__ == "__main__":
    main()