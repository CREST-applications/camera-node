from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from pydantic import BaseModel
import cv2


class Config(BaseModel):
    fps: int
    device: int
    scale: float


class Camera(Node):
    def __init__(self, config: Config):
        super().__init__("camera")

        self.__config = config

        self.__pub = self.create_publisher(Image, "/camera", 10)
        self.create_timer(1 / config.fps, self.__callback)

        self.__capture = cv2.VideoCapture(self.__config.device)
        self.__cv_bridge = CvBridge()

        self.get_logger().info(f"Initialized with config: {self.__config}")

    def __callback(self):
        # Read the frame
        has_frame, frame = self.__capture.read()

        # Check if the frame is valid
        if not has_frame:
            self.get_logger().error("No frame")
            return

        # Convert the frame and publish it
        frame = cv2.resize(frame, None, fx=self.__config.scale, fy=self.__config.scale)
        # _, frame = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50])

        self.get_logger().info(frame.shape)
        image = self.__cv_bridge.cv2_to_imgmsg(frame, encoding="mono8")

        self.__pub.publish(image)
        self.get_logger().debug("published to `/camera`")
