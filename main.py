import cv2
import pygame

pygame.init()
pygame.mixer.init()
cam = cv2.VideoCapture(0);

while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    difference = cv2.absdiff(frame1, frame2)

    # Convert image color space to grey
    gray = cv2.cvtColor(difference, cv2.COLOR_RGBA2GRAY)
    # Blurr the image (difference)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Create binary image
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    # Adding morphological filter to sharpen image
    dilated = cv2.dilate(thresh, None, iterations=3)
    # Shape analysis to add a triangle around movement
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c);
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        sound = pygame.mixer.Sound("alerte2.wav")
        sound.play()

    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('My Own Cam', frame1)
