#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import sys


# 
# # 画面宽度设定为 1920
# 
# # 画面高度度设定为 1080
# 

## 创建一个名字叫做 “image_win” 的窗口
# 窗口属性 flags
#   * WINDOW_NORMAL：窗口可以放缩
#   * WINDOW_KEEPRATIO：窗口缩放的过程中保持比率
#   * WINDOW_GUI_EXPANDED： 使用新版本功能增强的GUI窗口
# cv2.namedWindow('image_win',flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)

cap = cv2.VideoCapture("/dev/video0")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cv2.namedWindow('image_kinova',flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
cv2.namedWindow('image_usb',flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)


class image_converter:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/color/image_raw",Image,self.callback)
        
    def callback(self,data):
        try:
            kinova_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        kinova_image = cv2.resize(kinova_image, (640,480), cv2.INTER_AREA)
        cv2.imshow("image_kinova", kinova_image) 
        ret, frame = cap.read()
        cv2.imshow('image_usb',frame)
        key = cv2.waitKey(3)
            

def main(args):
    ic = image_converter()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows() # 销毁所有的窗口
    # cap.release() # 释放VideoCapture

if __name__ == '__main__':
    main(sys.argv)
