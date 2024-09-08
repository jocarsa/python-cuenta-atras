import cv2
import numpy as np

# Video properties
width, height = 1920, 1080
fps = 60
duration = 3600  # 1 hour in seconds
output_file = "countdown_timer.mp4"

# Create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# Define font and color for the text
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 4
font_color = (255, 255, 255)  # White color
thickness = 8

# Create a black background image
background = np.zeros((height, width, 3), dtype=np.uint8)

for second in range(duration, -1, -1):
    # Calculate the time in HH:MM:SS format
    hours = second // 3600
    minutes = (second % 3600) // 60
    seconds = second % 60
    time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

    # Create a copy of the background
    frame = background.copy()

    # Calculate the size of the text and position it in the center
    text_size = cv2.getTextSize(time_str, font, font_scale, thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2

    # Put the text on the frame
    cv2.putText(frame, time_str, (text_x, text_y), font, font_scale, font_color, thickness)

    # Write the frame to the video
    for _ in range(fps):
        out.write(frame)

# Release the video writer
out.release()

print("Video creation complete!")
