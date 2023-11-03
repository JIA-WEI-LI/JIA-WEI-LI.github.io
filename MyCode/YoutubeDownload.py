import os
from pytube import YouTube

class VideoDownloader:
    def __init__(self, video_url, on_progress_callback=None):
        self.video_url = video_url
        self.yt = YouTube(video_url)
        self.on_progress_callback = on_progress_callback

    def get_video_info(self):
        title = self.yt.title
        length = self.yt.length
        author = self.yt.author
        channel_url = self.yt.channel_url
        thumbnail_url = self.yt.thumbnail_url
        views = self.yt.views

        return {
            'title': title,
            'length_seconds': length,
            'author': author,
            'channel_url': channel_url,
            'thumbnail_url': thumbnail_url,
            'views': views
        }

    def download_highest_resolution_video(self):
        print('Downloading highest resolution video...')
        title = self.yt.title
        filename = f"{os.path.basename(title)}.mp4"  # 使用合法的文件名
        self.yt.register_on_progress_callback(self.on_progress)
        self.yt.streams.get_highest_resolution().download(filename=filename)
        print('Download completed.')

    def download_video_by_resolution(self, resolution, filename=None):
        print(f'Downloading {resolution} video...')
        if filename is None:
            filename = f'{self.yt.title}_{resolution}.mp4'
        self.yt.register_on_progress_callback(self.on_progress)
        self.yt.streams.filter(res=resolution).first().download(filename=filename)
        print('Download completed.')

    def on_progress(self, stream, chunk, remains):
        total = stream.filesize
        percent = (total - remains) / total * 100
        if self.on_progress_callback:
            self.on_progress_callback(percent)

    def get_all_streams(self):
        return self.yt.streams.all()
    
# video_url = 'https://www.youtube.com/watch?v=K57XcDsUl6A&list=RDK57XcDsUl6A&start_radio=1'
# downloader = VideoDownloader(video_url)

# video_info = downloader.get_video_info()
# print('Video Info:')
# print(video_info)

# all_streams = downloader.get_all_streams()
# print('Available Streams:')
# for stream in all_streams:
#     print(stream)

# downloader.download_highest_resolution_video()

# https://www.youtube.com/watch?v=0BUDGBnN8JU
