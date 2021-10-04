from PyQt5 import QtWidgets, QtGui, QtCore

from PIL import Image
import numpy as np
import cv2
import sys

app = QtWidgets.QApplication(sys.argv)

input_image = cv2.imread("/home/kornbotdev/Actuator_controller_bottom.png")
print(type(input_image))
#input_image = np.asarray(input_image, dtype="int32")
height, width, channels = input_image.shape
bytesPerLine = channels * width
qImg = QtGui.QImage(input_image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
pixmap01 = QtGui.QPixmap.fromImage(qImg)
pixmap_image = QtGui.QPixmap(pixmap01)
label_imageDisplay = QtWidgets.QLabel()
label_imageDisplay.setPixmap(pixmap_image)
label_imageDisplay.setAlignment(QtCore.Qt.AlignCenter)
label_imageDisplay.setScaledContents(True)
label_imageDisplay.setMinimumSize(1,1)
label_imageDisplay.show()
sys.exit(app.exec_())
