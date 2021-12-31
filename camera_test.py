import time
import cv2

def main():
    cam = cv2.VideoCapture(0)

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break

        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        time.sleep(0.5)
        if img_counter >= 5:
            break


    cam.release()

if __name__ == "__main__":
    main()