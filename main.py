import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
from yt_dlp import YoutubeDL

class GUILogger:
    def __init__(self, log_widget):
        self.log_widget = log_widget

    def debug(self, msg):
        self.log_widget.insert(tk.END, msg + "\n")
        self.log_widget.see(tk.END)

    def info(self, msg):
        self.log_widget.insert(tk.END, msg + "\n")
        self.log_widget.see(tk.END)

    def warning(self, msg):
        self.log_widget.insert(tk.END, "WARNING: " + msg + "\n")
        self.log_widget.see(tk.END)

    def error(self, msg):
        self.log_widget.insert(tk.END, "ERROR: " + msg + "\n")
        self.log_widget.see(tk.END)

def progress_hook(d, log_widget):
    if d['status'] == 'downloading':
        msg = f"Скачивание: {d.get('_percent_str', '').strip()} ({d.get('_speed_str', '').strip()})"
        log_widget.insert(tk.END, msg + "\n")
        log_widget.see(tk.END)
    elif d['status'] == 'finished':
        log_widget.insert(tk.END, "Скачивание завершено, объединение файлов...\n")
        log_widget.see(tk.END)

def download_videos(file_path, output_dir='downloads', log_widget=None):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    logger = GUILogger(log_widget) if log_widget else None

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'logger': logger,
        'progress_hooks': [lambda d: progress_hook(d, log_widget)],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(file_path)
        if logger:
            logger.info("Скачивание завершено!")
        messagebox.showinfo("Успех", "Скачивание завершено!")
    except Exception as e:
        if logger:
            logger.error(str(e))
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

def select_file():
    file_path = filedialog.askopenfilename(title="Выберите файл со ссылками", filetypes=(("Text Files", "*.txt"),))
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def select_output_dir():
    directory = filedialog.askdirectory(title="Выберите папку для сохранения")
    if directory:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, directory)

def start_download():
    file_path = entry_file.get()
    output_dir = entry_output.get() or 'downloads'

    if not file_path:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите файл со ссылками.")
        return

    btn_download.config(state=tk.DISABLED)

    log_text.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)
    log_text.config(state=tk.DISABLED)

    threading.Thread(target=run_download, args=(file_path, output_dir)).start()

def run_download(file_path, output_dir):
    log_text.config(state=tk.NORMAL)
    download_videos(file_path, output_dir, log_widget=log_text)
    log_text.config(state=tk.DISABLED)
    btn_download.config(state=tk.NORMAL)

def create_gui():
    global entry_file, entry_output, btn_download, log_text

    root = tk.Tk()
    root.title("Массовый YT и TikTok Downloader")
    root.geometry("700x500")


    frame_file = tk.Frame(root)
    frame_file.pack(padx=10, pady=10, fill=tk.X)

    lbl_file = tk.Label(frame_file, text="Файл со ссылками:")
    lbl_file.pack(side=tk.LEFT)

    entry_file = tk.Entry(frame_file, width=50)
    entry_file.pack(side=tk.LEFT, padx=5)

    btn_browse = tk.Button(frame_file, text="Обзор", command=select_file)
    btn_browse.pack(side=tk.LEFT)

   
    frame_output = tk.Frame(root)
    frame_output.pack(padx=10, pady=10, fill=tk.X)

    lbl_output = tk.Label(frame_output, text="Папка для сохранения:")
    lbl_output.pack(side=tk.LEFT)

    entry_output = tk.Entry(frame_output, width=50)
    entry_output.pack(side=tk.LEFT, padx=5)

    btn_browse_output = tk.Button(frame_output, text="Обзор", command=select_output_dir)
    btn_browse_output.pack(side=tk.LEFT)

   
    btn_download = tk.Button(root, text="Начать скачивание", command=start_download, bg='green', fg='blue')
    btn_download.pack(pady=10)

    
    log_text = scrolledtext.ScrolledText(root, width=80, height=20, state=tk.DISABLED)
    log_text.pack(padx=10, pady=10)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
