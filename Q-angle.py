import cv2
import math

def calculate_angle(p1, p2, p3):
    vector1 = [p1[0] - p2[0], p1[1] - p2[1]]
    vector2 = [p3[0] - p2[0], p3[1] - p2[1]]

    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

    magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
    magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

    angle_radians = math.acos(dot_product / (magnitude1 * magnitude2))
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def main():
    # Load the image
    image = cv2.imread('/Users/seeunyoon/Desktop/ICPA/ICPA 2023/과학과제연구/Q-angle 사진/image.png')

    if image is None:
        print("Error loading image.")
        return

    points = []
    drawing = False
    selected_point = None

    def click_event(event, x, y, flags, param):
        nonlocal drawing, selected_point

        if event == cv2.EVENT_LBUTTONDOWN:
            for point in points:
                if abs(point[0] - x) < 10 and abs(point[1] - y) < 10:
                    drawing = True
                    selected_point = point
                    break
            else:
                drawing = True
                selected_point = None

        if event == cv2.EVENT_LBUTTONUP:
            if drawing:
                drawing = False
                if selected_point is None:
                    points.append((x, y))
                    cv2.circle(image, (x, y), 10, (0, 0, 255), -1)

        if drawing and event == cv2.EVENT_MOUSEMOVE:
            temp_image = image.copy()
            if selected_point:
                for i, point in enumerate(points):
                    if point == selected_point:
                        points[i] = (x, y)
                        break
            cv2.imshow('Image', temp_image)

    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', click_event)

    while True:
        temp_image = image.copy()
        if drawing and selected_point is not None:
            cv2.circle(temp_image, selected_point, 10, (0, 0, 255), -1)
        cv2.imshow('Image', temp_image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            if len(points) == 3:
                angle = calculate_angle(points[0], points[1], points[2])
                print(f"Angle between the three points: {angle} degrees")
                if angle > 90:
                    opposite_angle = 180 - angle
                    print(f"Opposite angle: {opposite_angle} degrees")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
