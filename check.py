import cv2

index = 0
while True:
    cap = cv2.VideoCapture(index)
    if not cap.read()[0]:
        break
    else:
        print(f"Camera {index} is available.")
    cap.release()
    index += 1

print("Finished checking cameras.")