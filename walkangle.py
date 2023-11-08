#C:/Users/jinye/Pictures/footprint.jpg
import cv2
import numpy as np
import math

# 이미지 파일 경로
image_path = 'C:/Users/jinye/Pictures/footprint.jpg'

# 이미지 불러오기
image = cv2.imread(image_path)

# 색상 정의
color_a = (0, 0, 255)  # 빨간색 (BGR 형식)
color_b = (0, 255, 0)  # 초록색 (BGR 형식)

# 함수 to handle mouse click events
def get_point(event, x, y, flags, param):
    global point_a, point_b, point_c, click_counter

    if event == cv2.EVENT_LBUTTONDOWN:
        if click_counter == 0:
            point_a = (x, y)
            click_counter += 1
            cv2.circle(image, point_a, 5, color_a, -1)  # 점 A를 바로 표시
        elif click_counter == 1:
            point_b = (x, y)
            click_counter += 1
            cv2.circle(image, point_b, 5, color_b, -1)  # 점 B를 바로 표시
        elif click_counter == 2:
            point_c = (x, y)
            click_counter += 1

            # Draw circles for points A, B, C
            radius = 5
            color = (0, 0, 255)  # Red in BGR
            thickness = -1  # Fill the circle

            cv2.circle(image, point_c, radius, color, thickness)

            # Calculate and display the acute angle between A, B, and C
            vector_ab = np.array(point_b) - np.array(point_a)
            vector_ac = np.array(point_c) - np.array(point_a)

            dot_product = np.dot(vector_ab, vector_ac)
            magnitude_ab = np.linalg.norm(vector_ab)
            magnitude_ac = np.linalg.norm(vector_ac)

            cosine_theta = dot_product / (magnitude_ab * magnitude_ac)
            angle_rad = math.acos(cosine_theta)

            angle_deg = math.degrees(angle_rad)

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_color = (255, 255, 255)  # White in BGR
            font_thickness = 1

            cv2.putText(image, f'Acute Angle ABC: {angle_deg:.2f} degrees', (10, 30), font, font_scale, font_color, font_thickness)

            cv2.imshow('Image with Points', image)

# Create an empty window
cv2.namedWindow('Image with Points')

point_a, point_b, point_c = None, None, None
click_counter = 0

cv2.imshow('Image with Points', image)
cv2.setMouseCallback('Image with Points', get_point)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Press 'Esc' to exit
        break

cv2.destroyAllWindows()

