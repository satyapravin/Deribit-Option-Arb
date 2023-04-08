from PyQt6.QtWidgets import QDialog, QLabel
from PyQt6.QtGui import QPixmap                                                                                                            
                                                                                                                                

class ImageViewer(QDialog): 
    def __init__(self):  
        super().__init__()                                                                                                                  
        self.lbl = None
        self.initUI()                                                                                                                 

    def initUI(self):    
        self.lbl = QLabel(self)                                                                                               
        self.setWindowTitle('PayOff')  

    def update(self):
        pixmap = QPixmap("file.png")                                                                                                        
        self.lbl.setPixmap(pixmap)                                                                                                          
