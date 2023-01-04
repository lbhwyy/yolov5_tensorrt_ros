import numpy as np
import cv2
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Header


def ros_img_pub(video_path, ros_img, header):
    rospy.init_node('img_pub', anonymous=True)
    pub_ = rospy.Publisher("/usb_cam/image_raw", Image, queue_size=2)
    rate = rospy.Rate(30)

    print("/front_camera/image_raw ros image topic publish...")
    while not rospy.is_shutdown():
        cap = cv2.VideoCapture(video_path)
        ret, image = cap.read()
        while ret and not rospy.is_shutdown():
            ret, image = cap.read()
            if image is None:
                break
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)                
            header = Header(stamp=rospy.Time.now())
            header.frame_id = 'result'            
            ros_img.encoding = 'rgb8'            
            ros_img.header = header
            ros_img.height = image.shape[0]
            
            ros_img.width = image.shape[1]       
            print(ros_img.height,ros_img.width)         
            ros_img.step = image.shape[1] * image.shape[2]
            ros_img.data = np.array(image).tostring()
            pub_.publish(ros_img)
            rate.sleep()


def main():    
    video_path = '/home/tianbot/yolov5_ros_tensorrt/src/yolov5_ros/src/yolov5/data/5.mp4'
    ros_img = Image()
    header = Header
    ros_img_pub(video_path, ros_img, header)


if __name__ == '__main__':
    main()
