import rclpy

from .camera import Camera, Config


def main():
    config = Config(
        camera_topic="/image_raw/compressed",
        fps=30,
        device=-1,
        scale=1.0,
    )

    rclpy.init()
    camera = Camera(config)
    rclpy.spin(camera)
    rclpy.shutdown()
