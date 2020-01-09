import pyrealsense2 as rs
import numpy as np
import cv2
import time


def main(pipeline):
    fps_refresh_interval = 0.1
    fps_counter = 0
    fps = 0
    start_time = time.time()
    color_map = 13

    while True:
        fps_counter += 1
        frames = pipeline.wait_for_frames()

        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), color_map)

        if (time.time() - start_time) > fps_refresh_interval:
            fps = fps_counter/(time.time() - start_time)
            fps_counter = 0
            start_time = time.time()

        cv2.putText(depth_colormap, "FPS: " + "{:.2f}".format(fps) +"; Color Map: " + str(color_map), (0, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))

        cv2.imshow('RealSense', depth_colormap)
        cv2.waitKey(1)


if __name__ == '__main__':
    pipeline = None
    try:
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        #config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        pipeline.start(config)

        main(pipeline)
    except Exception as e:
        print(e)
    finally:
        if pipeline is not None:
            pipeline.stop()
