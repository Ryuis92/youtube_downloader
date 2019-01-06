import subprocess
from PyQt5 import QtCore
from pytube import YouTube

class Yt(QtCore.QThread):
    detail = QtCore.pyqtSignal("PyQt_PyObject")
    
    def __init__(self):
        super().__init__()
        self.yt = None
        self.url = None
        self.fail = False
    
    def run(self):
        try:
            self.fail = False
            self.yt = YouTube(self.url)
            self.detail.emit(self.yt)
        except:
            self.fail = True
            print("invalid url")
            return

class download(QtCore.QThread):
    down = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.yt = None
        self.path = None
        self.filename = None
        self.video_list = None
        self.audio_list = None
        self.video_combo_index = 0
        self.audio_combo_index = -1
        self.video_complete = False
        self.audio_complete = False
        self.label = None

    def run(self):
        self.video_complete = False
        self.audio_complete = False
        
        print(self.path)
        print(self.filename)

        #start video download
        self.video_list[self.video_combo_index].download(output_path=self.path, filename = (self.filename + 'v'))
        
        if self.audio_list:
            #audio download if exist
            self.audio_list[self.audio_combo_index].download(output_path=self.path, filename = (self.filename + 'a'))
            
            #merge video and audio using FFMEPG
            subprocess.call(self.get_cmd_list())
            

    def progress(self, stream, chunk, file_handle, bytes_remaining):
        if self.audio_list:
            if self.video_complete:
                per = int((file_handle.tell() + self.video_list[self.video_combo_index].filesize) / (self.video_list[self.video_combo_index].filesize + self.audio_list[self.audio_combo_index].filesize) * 100)
            else:
                per = int(file_handle.tell() / (self.video_list[self.video_combo_index].filesize + self.audio_list[self.audio_combo_index].filesize) * 100)
        else:
            per = int(file_handle.tell() / (self.video_list[self.video_combo_index].filesize) * 100)
        self.down.emit(per)

    def get_cmd_list(self):
        video_filename = self.path + self.filename + 'v.' + self.video_list[self.video_combo_index].subtype
        audio_filename = self.path + self.filename + 'a.' + self.audio_list[self.audio_combo_index].subtype
            
        if self.video_list[self.video_combo_index].subtype == 'webm' and self.audio_list[self.audio_combo_index].subtype == 'mp4':
            print("hi")
            audio_codec = 'libopus'
        else:
            audio_codec = 'copy'
        output_filename = self.path + self.filename + '.' + self.video_list[self.video_combo_index].subtype

        cmd_list = ['ffmpeg', '-y','-i', video_filename, '-i', audio_filename, '-c:v', 'copy', '-c:a', audio_codec, output_filename]

        return cmd_list
