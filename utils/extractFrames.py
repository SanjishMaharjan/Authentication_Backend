import cv2
import os

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def remove_similar_frames_with_faces(video_path, output_folder, threshold=200):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    # Get the frames per second (fps) of the input video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Get the width and height of frames
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))

    # Read the first frame
    _, prev_frame = cap.read()

    while True:
        # Read the next frame
        ret, frame = cap.read()

        if not ret:
            break  # Break the loop if the video ends

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # Calculate absolute difference between frames
        diff = cv2.absdiff(prev_frame, frame)

        # Convert the difference to grayscale
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Threshold the grayscale difference
        _, thresh_diff = cv2.threshold(gray_diff, threshold, 255, cv2.THRESH_BINARY)

        # Count non-zero pixels in the thresholded difference
        non_zero_pixels = cv2.countNonZero(thresh_diff)

        # If the number of non-zero pixels is above a certain threshold,
        # and faces are detected, save the frame and update the previous frame
        if non_zero_pixels > threshold and len(faces) > 0:
            output_video.write(frame)
            cv2.imwrite(f'{output_folder}/frame_{int(cap.get(cv2.CAP_PROP_POS_FRAMES))}.png', frame)

        # Update the previous frame
        prev_frame = frame

    # Release video capture and writer objects
    cap.release()
    output_video.release()

