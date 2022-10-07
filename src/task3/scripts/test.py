#!/usr/bin/python3

import rospy
import torch
from torchvision import datasets, models, transforms
import os
import numpy
from PIL import Image
from sensor_msgs.msg import Image as RosImage
import matplotlib.pyplot as plt
import time
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import cv2
from std_msgs.msg import String
from pathlib import Path

class Test:

    def __init__(self):

        rospy.init_node('test', anonymous=True)

        self.food_image_sub = rospy.Subscriber(
            "/food_image", RosImage, self.food_image
        )

        self.food_message_sub = rospy.Subscriber(
            "/food_msg_command", String, self.new_food
        )

        self.food_message_pub = rospy.Publisher(
            "/food_msg", String, queue_size=10
        )

        self.bridge = CvBridge()
        self.got_image = False
        self.image = None
        self.got_command = False


    def new_food(self, data):

        self.got_command = True


    def food_image(self, data):

        try:
            self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        self.got_image = True

        cv2.imshow("FOOD", self.image)
        cv2.waitKey()

    def test_food(self):

        input_size = 224

        data_transforms = {
            'train': transforms.Compose([
                transforms.RandomResizedCrop(input_size),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
            'val': transforms.Compose([
                transforms.Resize(input_size),
                transforms.CenterCrop(input_size),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
        }

        class_dict = {0:'baklava',
                      1:'pica',
                      2:'pomfri',
                      3:'solata',
                      4:'torta'}

        cwd = Path.cwd()
        mod_path = Path(__file__).parent
        relative_path = '../scripts/cake'
        images_path = (mod_path / relative_path).resolve()
        # img_path = str(src_path_1) + "/good_map_fixed.pgm"
        # images_path = '/home/mateja/Rins2/src/task3/scripts/cake'
        os.chdir(images_path)
        #images_path = '/home/mateja/Rins2/src/task3/scripts/cake'
        #images_path = '/home/Rins/src/task3/scripts/images'
        mod_path = Path(__file__).parent
        relative_path = '../scripts/Foodero/best_foodero_model.pt'
        model_path = (mod_path / relative_path).resolve()
        #model_path = '/home/mateja/Rins2/src/task3/scripts/Foodero/best_foodero_model.pt'

        if self.got_command == True:

            model = torch.load(model_path)
            model.eval()

            for image_name in os.listdir(images_path):
                image_file = os.path.join(images_path, image_name)

                opencv_image = cv2.imread(image_file)
                color_converted = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
                img_p = Image.fromarray(color_converted)
                #img_p = Image.open(image_file)
                #img_p = cv2.cvtColor(img_p, cv2.COLOR_BGR2RGB)
                #img_p = Image.fromarray(img_p)
                #print(img_p.format)
                #img_p.show()
                # time.sleep(10)

                img = data_transforms['train'](img_p).unsqueeze(0)
                pred = model(img)

                pred_np = pred.cpu().detach().numpy().squeeze()
                class_ind = np.argmax(pred_np)

                os.remove(image_file)
                #print(class_dict[class_ind])
                self.food_message_pub.publish(class_dict[class_ind])

                #plt.imshow(img_p)
                #plt.text(20,50,class_dict[class_ind], c='g')
                #plt.show()


def main():

    test = Test()
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        test.test_food()
        rate.sleep()


if __name__ == '__main__':
    main()