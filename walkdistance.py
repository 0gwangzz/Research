import cv2
import math

# 선분의 두 점 사이의 거리를 계산하는 함수
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# 이미지 경로 입력
image_path = input("이미지 파일 경로를 입력하세요: ")

# 이미지 불러오기
image = cv2.imread(image_path)
image_copy = image.copy()

# 점 클릭 이벤트 핸들러 함수
def draw_point(event, x, y, flags, param):
    global click_count, start_x, start_y, end_x, end_y, baseline_length, baseline_drawn, num_segments, drawing_mode, total_length, lengths
    if event == cv2.EVENT_LBUTTONDOWN:
        if not baseline_drawn:
            baseline_drawn = True
            baseline_length = 0
            start_x, start_y = x, y
        else:
            if drawing_mode == "baseline":
                baseline_length = calculate_distance(start_x, start_y, x, y)
                print(f"기준선의 길이: {baseline_length:.2f} 픽셀")
                drawing_mode = "segments"
                total_length = 0
                lengths = []
            elif drawing_mode == "segments":
                if num_segments == 0:
                    print("모든 선분을 그리셨습니다.")
                    return
                if click_count % 2 == 0:
                    start_x, start_y = x, y
                else:
                    end_x, end_y = x, y
                    pixel_length = calculate_distance(start_x, start_y, end_x, end_y)
                    length_in_cm = (pixel_length / baseline_length) * baseline_length_in_cm
                    total_length += length_in_cm
                    lengths.append(length_in_cm)
                    print(f"{num_segments_original - num_segments + 1}번째 선분의 길이: {length_in_cm:.2f} cm")
                    num_segments -= 1
                    if num_segments == 0:
                        average_length = total_length / len(lengths)
                        print(f"각 선분의 길이: {', '.join([f'{length:.2f} cm' for length in lengths])}")
                        print(f"선분들의 평균 길이: {average_length:.2f} cm")
                        drawing_mode = None
                    cv2.line(image_copy, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)  # 선분 그리기
                click_count += 1
            
    cv2.imshow("Image with Segments", image_copy)

num_segments_original = int(input("선분의 개수를 입력하세요: "))
baseline_length_in_cm = float(input("사진상의 기준선 길이를 센티미터로 입력하세요: "))
total_length = 0
lengths = []
click_count = 0
baseline_drawn = False
baseline_length = 0
num_segments = num_segments_original
drawing_mode = "baseline"

cv2.namedWindow("Image with Segments")
cv2.setMouseCallback("Image with Segments", draw_point)

while True:
    cv2.imshow("Image with Segments", image_copy)
    key = cv2.waitKey(1)
    if key == 27:  # ESC 키를 누르면 종료
        break
    elif key == ord("q"):
        if drawing_mode == "baseline":
            drawing_mode = "segments"

cv2.destroyAllWindows()
