from PyQt5 import QtCore, QtGui, QtWidgets
import pyperclip
import urllib
import prompt

import time
import re
from thread import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #main window setting
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800,750)
        MainWindow.setIconSize(QtCore.QSize(24, 24))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setWindowIcon(QtGui.QIcon('icon/youtube_full_color_icon/social/1024px/red/youtube_social_square_red.png'))
        
        #prompt
        self.helper = prompt.helper()
        self.analysis = prompt.analysis()

        #layout
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout.addWidget(self.groupBox)
        
        self.groupBox_layout = QtWidgets.QHBoxLayout()
        self.image_label = QtWidgets.QLabel()
        self.groupBox_layout.addWidget(self.image_label)
        self.groupBox.setLayout(self.groupBox_layout)

        #video detail goes here
        self.groupBox_layout_layout =  QtWidgets.QVBoxLayout()
        self.lb_list = [QtWidgets.QLabel() for i in range(0,4)]
        for lb in self.lb_list:
            lb.setWordWrap(True)
            self.groupBox_layout_layout.addWidget(lb)

        self.groupBox_layout.addLayout(self.groupBox_layout_layout)
        self.groupBox_layout.setSpacing(50)

        #Download option group box
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2_layout = QtWidgets.QVBoxLayout()
        
        #video options
        video_layout = QtWidgets.QHBoxLayout()
        video_layout.addWidget(QtWidgets.QLabel("Video Quality"))
        self.video_combo = QtWidgets.QComboBox()
        self.video_combo.setEnabled(False)
        self.video_combo.activated.connect(self.video_combo_active)
        video_layout.addWidget(self.video_combo)
        self.video_combo_index = 0

        #audio options
        audio_layout = QtWidgets.QHBoxLayout()
        audio_layout.addWidget(QtWidgets.QLabel("Audio Quality"))
        self.audio_combo = QtWidgets.QComboBox()
        self.audio_combo.setEnabled(False)
        self.audio_combo.activated.connect(self.audio_combo_active)
        audio_layout.addWidget(self.audio_combo)
        self.audio_combo_index = -1

        #set layout
        self.groupBox_2_layout.addLayout(video_layout)
        self.groupBox_2_layout.addLayout(audio_layout)
      
        self.groupBox_2.setLayout(self.groupBox_2_layout)

        self.verticalLayout.addWidget(self.groupBox_2)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
       
        #status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        #toolbar
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setEnabled(True)
        self.toolBar.setBaseSize(QtCore.QSize(0, 0))
        self.toolBar.setStyleSheet("spacing:12px;\n""padding:3px")
        self.toolBar.setMovable(False)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setIconSize(QtCore.QSize(60, 60))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        
        #toolbar save
        self.save = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/save"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save.setIcon(icon)
        self.save.setObjectName("save")
        self.save.setEnabled(False)
        self.percent = prompt.percent()
        #TODO
        self.save.triggered.connect(self.save_file)         
        self.percent.closeEvent = self.quitThread
        self.percent.btn.clicked.connect(self.close_download)

        #toolbar copy_from_url
        self.copy_from_url = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/youtube_full_color_icon/social/1024px/red/youtube_social_circle_red"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copy_from_url.setIcon(icon1)
        self.copy_from_url.setObjectName("copy_from_url")
        
        #TODO        
        self.copy_from_url.triggered.connect(self.copy_from_cb)         
        
        #QThread
        self.yt = None
        self.qthread = Yt()
        self.qthread.detail.connect(self.get_yt)
        self.download = download()
        self.download.down.connect(self.on_progress)
        
        #toolbar help
        self.help = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help.setIcon(icon2)
        self.help.setObjectName("help")
        
        #TODO
        self.help.triggered.connect(self.show_help)         

        #attach to toolbar
        self.toolBar.addAction(self.copy_from_url)
        self.toolBar.addAction(self.save)
        self.toolBar.addAction(self.help)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Youtube Downloader"))
        self.groupBox.setTitle(_translate("MainWindow", "Video Info"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Download option"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.save.setText(_translate("MainWindow", "save"))
        self.copy_from_url.setText(_translate("MainWindow", "copy_from_url"))
        self.help.setText(_translate("MainWindow", "help"))
    
    def close_download(self):
        self.download.terminate()
        self.percent.close()

    def quitThread(self, event):
        self.download.terminate()
        event.accept()

    def on_progress(self, per):
        self.percent.pb.setValue(per)
    
    def on_complete(self, stream , file_handle):
        file_handle.close()
        
        if not self.download.video_complete:
            self.download.video_complete = True
            print("Video download complete")
            if self.download.audio_combo_index is -1:
                self.percent.label.setText("Complete!")
            else:
                self.percent.label.setText("Downloading audio...")
        else:
            self.percent.label.setText("Complete!")
            print("Audio download complete")
        
    def get_yt(self, yt):
        self.yt = yt
        print('reading done')
        #set thumbnail image
        self.image_label.setPixmap(self.get_thumbnail(self.yt))
        
        #set video info
        self.set_video_info(self.yt)

        #set download options
        self.set_download_options(self.yt)
        
        self.save.setEnabled(True)
        self.video_combo.setEnabled(True)
        self.analysis.close()

    def copy_from_cb(self):
        url = pyperclip.paste()
        if not pyperclip.is_available():
            print("clip board not available")
            return
        
        self.qthread.url = url
        self.qthread.start()
        time.sleep(0.01)

        if self.qthread.fail:
            return
        
        self.analysis.show()
        
    def get_thumbnail(self, yt):
        thumb = urllib.request.urlopen(yt.thumbnail_url_hq).read()
        pixmap = QtGui.QPixmap()
        print(yt.thumbnail_url_hq)
        pixmap.loadFromData(thumb)
        print('reading thumbnail done')
        
        return pixmap
    
    def set_video_info(self, yt):
        """
        Channel
        Title
        Description
        Length

        """
        len = int(yt.length)
        s = len % 60
        m = int((len - s) / 60) % 60
        h = int(((len - s) / 60 - m) / 60)

        self.lb_list[0].setText('Channel : {}'.format(yt.author))
        self.lb_list[1].setText('Title : {}'.format(yt.title))
        self.lb_list[2].setText('Description : {}'.format(yt.description))
        self.lb_list[3].setText('Length : {0:02}:{1:02}:{2:02}'.format(h,m,s))

    def set_download_options(self, yt):
  
        self.video_list = yt.streams.filter(type='video').all()
        self.audio_list = yt.streams.filter(only_audio=True).all()

        self.video_combo.clear()
        self.audio_combo.clear()
        #with open("url.txt", "w") as file:
        #    for video in self.video_list:
        #        file.write('res:{} fps:{} {}\n'.format(video.resolution,video.fps,video.url))
        for video in self.video_list:
            if video.filesize_mb > 1024:
                self.video_combo.addItem('Resolution: {0:>5}  Fps: {1:>}  Type: {2:>4}  size: {3:>4.1f}GB'.format(video.resolution, video.fps, video.subtype, video.filesize_mb/1024))
            else:
                self.video_combo.addItem('Resolution: {0:>5}  Fps: {1:>}  Type: {2:>4}  size: {3:>4.1f}MB'.format(video.resolution, video.fps, video.subtype, video.filesize_mb))
        
        for audio in self.audio_list:
            self.audio_combo.addItem('Bit rate: {}  Type: {}'.format(audio.abr, audio.subtype))
    
    def video_combo_active(self, index):
        self.video_combo_index = index

        if self.video_list[index].includes_audio_track:
            self.audio_combo.setEnabled(False)
            self.audio_combo_index = -1
        else:
            if not self.audio_combo.isEnabled():
                self.audio_combo.setEnabled(True)
                self.audio_combo_index = self.audio_combo.currentIndex()

        print('video combo: ', index)
        print('audio combo: ', self.audio_combo_index)

    def audio_combo_active(self, index):
        print('audio combo: ', index)
        print(self.audio_list[index].audio_codec)
        self.audio_combo_index = index

    def show_help(self):
        self.helper.show()
  
    def save_file(self):
        safe = re.sub('[\'\"?/*<>|\\:]', '', self.yt.title)
        name = QtWidgets.QFileDialog.getSaveFileName(directory = '{}'.format(safe))

        if name[1] == '':
            return

        file_name = name[0].split('/')[-1]
        path = name[0].rstrip(file_name)
        #print(name)
        #print(file_name)
        #print(path)
        #print(self.video_list[self.video_combo_index])
        #print('{}{}.{}'.format(path, file_name + 'a', self.audio_list[self.audio_combo_index].subtype))
        self.download.yt = self.yt
        self.download.yt.register_on_progress_callback(self.download.progress)
        self.download.yt.register_on_complete_callback(self.on_complete)
        self.download.path = path
        self.download.filename = file_name
        self.download.video_list = self.video_list
        self.download.video_combo_index = self.video_combo_index
        self.download.label = self.percent.label

        if self.audio_combo_index is not -1:
            self.download.audio_list = self.audio_list
            self.download.audio_combo_index = self.audio_combo_index
        
        print("start downloading")
        self.download.start()
        self.percent.label.setText("Downloading...")
       
        self.percent.show()
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
   
    sys.exit(app.exec_())

