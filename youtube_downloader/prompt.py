from PyQt5 import QtCore, QtGui, QtWidgets

class helper(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        text = """
        01. 원하는 유튜브 주소를 복사하세요
        02. 툴바에 있는 빨간 유튜브 아이콘을 클릭하세요.
        03. 아래에서 원하는 화질과 오디오를 선택하세요
        04. 다운로드 버튼을 누르세요
        05. 유튜브는 adaptive 방식과 progress 방식으로 영상을 전달합니다. 
            adaptive는 오디오와 영상 파일을 따로 전송하고 progress는 하나로 전송합니다.
            그래서 adaptive 방식으로 받을 경우 오디오와 영상 파일을 따로 합쳐야 합니다.
        06. progress방식은 720P 까지만 지원하고 그 이상은 adaptive 방식으로 지원됩니다.
        07. 오디오와 영상 결합은 FFMPEG을 통해 자동으로 이루어집니다.
        08. 이런 것들을 알 필요는 없습니다. 프로그램이 다 알아서 해줍니다.
        09. 간혹 안되는 영상이 있을 수 있습니다. 그건 pytube의 문제입니다.
        10. 다운로드 속도가 느릴 수 있습니다.

        Dependency
        pytube
        piperclip
        pyqt5
        FFMPEG
        """
        self.resize(500, 300)
        self.setWindowTitle("How To Use")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        label = QtWidgets.QLabel(text, self)

class analysis(QtWidgets.QWidget):   
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        pb = QtWidgets.QProgressBar()
        pb.setRange(0,0)
        #pb.setValue(100)
        pb.setTextVisible(False)
        label = QtWidgets.QLabel("URL Analyising")
        label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(pb)
        layout.addWidget(label)
        self.setLayout(layout)
        self.resize(200,50)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowStaysOnTopHint)

class percent(QtWidgets.QWidget):   
    def __init__(self):
        super().__init__()
        self.initUI()
        

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        in_layout = QtWidgets.QHBoxLayout()
        self.pb = QtWidgets.QProgressBar()
        self.pb.setRange(0,100)
        self.pb.setValue(0)
        self.pb.setTextVisible(True)
        
        self.btn = QtWidgets.QPushButton("Cancel")
        self.btn.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed)
        )

        self.label = QtWidgets.QLabel("Downloading video...")
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        
        layout.addWidget(self.pb)
        layout.addWidget(self.label)
        in_layout.addWidget(self.btn)
        layout.addLayout(in_layout)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(" ")
        self.setLayout(layout)
        self.resize(300,50)
        
  