import rclpy
from rclpy.node import Node
from rclpy import qos
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class MockCamera(Node):
    IMAGE_PATH_LIST = [
        "./src/camera/images/cat_meme_1.jpg",
        "./src/camera/images/cat_meme_2.jpg",
    ]

    def __init__(self):
        super().__init__("mock_camera")

        self.__pub = self.create_publisher(
            Image,
            "/camera",
            qos.qos_profile_sensor_data,
        )
        self.create_timer(0.5, self.__callback)

        self.__image_list = self.__open_images()
        self.__image_index = 0

    def __open_images(self) -> list[Image]:
        cv_bridge = CvBridge()
        image_list = []

        for image_path in self.IMAGE_PATH_LIST:
            image = cv2.imread(image_path)
            if image is None:
                raise FileNotFoundError(f"Image not found: {image_path}")

            image = cv_bridge.cv2_to_imgmsg(image)
            image_list.append(image)

        return image_list

    def __callback(self):
        image = self.__image_list[self.__image_index]
        self.__pub.publish(image)
        self.get_logger().info(
            f"Publishing image {self.__image_index + 1}/{len(self.__image_list)}"
        )

        self.__image_index += 1
        if len(self.__image_list) <= self.__image_index:
            self.__image_index = 0


def main():
    rclpy.init()
    mock_camera = MockCamera()
    rclpy.spin(mock_camera)
    rclpy.shutdown()
