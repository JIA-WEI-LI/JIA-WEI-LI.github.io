import tkinter as tk
import webbrowser
import threading

from tkinter import ttk, filedialog, messagebox
from YoutubeDownload import VideoDownloader
# from Util import ToolTip

def search_video_info():
    progress_bar["value"] = 0
    
    video_url = url_var.get()
    if video_url:
        downloader = VideoDownloader(video_url)
        video_info = downloader.get_video_info()
        search_var.set(video_info['title'])
        vedio_url_var.set(video_url)

        length_seconds = video_info['length_seconds']
        hours = length_seconds // 3600
        minutes = (length_seconds % 3600) // 60
        seconds = length_seconds % 60
        duration_var.set(f"{hours} 小時 {minutes} 分 {seconds} 秒")

        author_var.set(video_info['author'])
        channel_url_var.set(video_info['channel_url'])
        total_views_var.set(video_info['views'])
        
def download_highest_resolution_video():
    progress_bar["value"] = 0
    
    video_url = url_var.get()
    if video_url:
        downloader = VideoDownloader(video_url, on_progress_callback=update_progress)
        download_thread = threading.Thread(target=downloader.download_highest_resolution_video)
        download_thread.start()
        
def update_progress(percent):
    progress_bar["value"] = percent

def open_vedio_url(event):
    webbrowser.open(vedio_url_var.get())        

def open_channel_url(event):
    webbrowser.open(channel_url_var.get())

root = tk.Tk(screenName="YT影片下載")
root.title("YT影片下載")

style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

frame = ttk.Frame(root)
frame.pack(fill="x", expand=True)

file_frame = ttk.Frame(frame)
file_frame.grid(row=0, column=0, padx=5, pady=0, sticky="nsew")

file_frame.columnconfigure(1, weight=1)

url_label = ttk.Label(file_frame, text="輸入網址")
url_label.grid(row=0, column=0, padx=5, pady=(10,5), sticky="e")
url_var = tk.StringVar()  # 創建StringVar
url_entry = ttk.Entry(file_frame, textvariable=url_var)
url_entry.grid(row=0, column=1, padx=5, pady=(10,5), sticky="ew")
url_entry.config(width=100)
url_select = ttk.Button(file_frame, text="確定", style="Accent.TButton", command=search_video_info)
url_select.grid(row=0, column=2, padx=5, pady=(10,5), sticky="w")

# info 視窗
widgets_frame = ttk.Frame(frame)
widgets_frame.grid(row=1, column=0, padx=10, pady=10,  sticky="nsew")
widgets_frame.columnconfigure(0, weight=1)

name_label = ttk.Label(widgets_frame, text="搜尋結果： ")
name_label.grid(row=0, column=0, padx=5, pady=(10,5), sticky="w")

search_var = tk.StringVar()
search_var.set("(影片標題)")
name_entry = ttk.Entry(widgets_frame, textvariable=search_var, state="readonly", cursor="hand2")
name_entry.grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky="ew")
name_entry.bind("<Button-1>", open_vedio_url)
# ToolTip(name_entry, "點擊進入網站影片")

duration_var = tk.StringVar()
author_var = tk.StringVar()
channel_url_var = tk.StringVar()
total_views_var = tk.StringVar()
vedio_url_var = tk.StringVar()

info_frame = ttk.Labelframe(widgets_frame, text="影片資訊")
info_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
length_sec_label = ttk.Label(info_frame, text="影片時長：")
length_sec_label.grid(row=0, column=0, padx=(20,5), pady=(10,5), sticky="ew")
duration_label = ttk.Label(info_frame, textvariable=duration_var)
duration_label.grid(row=0, column=1, padx=5, pady=(10,5), sticky="w")
author_label = ttk.Label(info_frame, text="頻道名稱：")
author_label.grid(row=1, column=0, padx=(20,5), pady=5, sticky="ew")
author_info_label = ttk.Label(info_frame, textvariable=author_var)
author_info_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
channel_url_label = ttk.Label(info_frame, text="頻道連結：")
channel_url_label.grid(row=2, column=0, padx=(20,5), pady=5, sticky="ew")
channel_url_info_label = ttk.Label(info_frame, textvariable=channel_url_var, cursor="hand2", foreground="#da00bb")
channel_url_info_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
channel_url_info_label.bind("<Button-1>", open_channel_url)
views_label = ttk.Label(info_frame, text="總觀看數：")
views_label.grid(row=3, column=0, padx=(20,5), pady=(5,10), sticky="ew")
total_views_info_label = ttk.Label(info_frame, textvariable=total_views_var)
total_views_info_label.grid(row=3, column=1, padx=5, pady=(5,10), sticky="w")

# advanced_frame = ttk.Labelframe(widgets_frame, text="進階下載")
# advanced_frame.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

# 影片預覽區
# vedio_labelframe = ttk.Labelframe(widgets_frame, text="影片預覽")
# vedio_labelframe.grid(row=2, column=1, rowspan=2, padx=5, pady=0, sticky="nsew")
# preview_frame = ttk.Frame(vedio_labelframe, width=400, height=300)
# preview_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

search_button = ttk.Button(widgets_frame, text="開始下載並預覽", style="Accent.TButton", command=download_highest_resolution_video)
search_button.grid(row=4, column=0, padx=5, pady=5, columnspan=2, sticky="ew")

progress_frame = ttk.Frame(widgets_frame)
progress_frame.grid(row=5, column=0, padx=5, pady=5, columnspan=2, sticky="ew")
progress_bar = ttk.Progressbar(progress_frame, mode="determinate")
progress_bar.pack(fill="x", padx=5, pady=5)

# 啟動主迴圈
root.mainloop()
