#!/usr/bin/env python3

from upload_thru_iot import Upload_thru_iot
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridgeError, CvBridge
import numpy as np
import sys,datetime,os

class push_usb_iamge_to_azure:
    def __init__(self,subscriber_node,image_path,connection_string):
        self.connection_string=connection_string
        self.image_path=image_path
        self.bridge= CvBridge()
        self.image_count=1
        image_sub = rospy.Subscriber(subscriber_node,Image, self.callback)

    def callback(self,ros_image):
        this_moment=datetime.datetime.now()
        print("received image at {time}".format(time=this_moment))
        image_recieved=self.bridge.imgmsg_to_cv2(ros_image,"bgr8")
        filename=("received_image_{year:x}{month:x}{day:x}{hour:x}{minute:x}{sec:x}.jpg".format(year=this_moment.year,month=this_moment.month,day=this_moment.day,hour=this_moment.hour,minute=this_moment.minute,sec=this_moment.second))
        
        if(not os.path.exists(self.image_path)):
            os.makedirs(self.image_path)

        filepath=os.path.join(self.image_path,filename)
        cv2.imwrite(filepath,image_recieved)
        push_to_azure=Upload_thru_iot(self.connection_string)
        push_to_azure.upload_image(filepath)







def main(args):
    rospy.init_node('push_image_to_azure', anonymous=True)
    push_to_azure=push_usb_iamge_to_azure(args[1],args[2],args[3])
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__ =='__main__':
    main(sys.argv)