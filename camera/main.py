import rclpy

from .camera import Camera, Config


def main():
    config = Config(
        fps=30,
        device=-1,
        scale=0.1,
    )

    rclpy.init()
    camera = Camera(config)
    rclpy.spin(camera)
    rclpy.shutdown()
