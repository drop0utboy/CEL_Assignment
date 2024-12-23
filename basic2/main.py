import cv2
import os
import json

# 저장 폴더 생성
os.makedirs("./output", exist_ok=True)

# 입력 폴더와 비디오 파일 검색
input_folder = "./input"
video_file = None
for file in os.listdir(input_folder):
    if file.endswith(".mp4"):
        video_file = os.path.join(input_folder, file)
        break

if video_file is None:
    print("Error: No .mp4 files found in ./input directory.")
    exit()

# 변수 초기화
cropping = False
ref_point = []
crop_data = []

# 마우스 콜백 함수
def click_and_crop(event, x, y, flags, param):
    global ref_point, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        ref_point.append((x, y))
        cropping = False

        # 직사각형 영역 표시
        cv2.rectangle(frame, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("Video", frame)

# JSON 저장 함수
def save_to_json(data, output_path):
    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

# 비디오 열기
cap = cv2.VideoCapture(video_file)

if not cap.isOpened():
    print(f"Error: Could not open video file {video_file}.")
    exit()

cv2.namedWindow("Video")
cv2.setMouseCallback("Video", click_and_crop)

frame_index = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video or error reading frame.")
        break

    clone = frame.copy()
    cv2.imshow("Video", frame)

    key = cv2.waitKey(30) & 0xFF

    # 'q' 입력으로 재생 중단
    if key == ord('q'):
        print("Exiting...")
        break

    # 직사각형 선택 완료 시 크롭 및 저장
    if len(ref_point) == 2:
        x1, y1 = ref_point[0]
        x2, y2 = ref_point[1]
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        cropped_frame = clone[y1:y2, x1:x2]
        crop_filename = f"./output/crop_frame_{frame_index}.png"
        cv2.imwrite(crop_filename, cropped_frame)

        # 좌표 및 파일 정보 저장
        crop_data.append({
            "frame_index": frame_index,
            "crop_coordinates": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
            "saved_file": crop_filename
        })

        ref_point = []

    frame_index += 1

# JSON 파일 저장
json_output_path = "./output/crop_data.json"
save_to_json(crop_data, json_output_path)

print(f"Cropping data saved to {json_output_path}")

cap.release()
cv2.destroyAllWindows()
