import cv2
import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

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

# JSON 저장 함수
def save_to_json(data, output_path):
    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

class VideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Cropping Tool")

        # 모니터 크기를 가져와 창 크기를 설정
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.window_width = int(screen_width * 0.8)
        self.window_height = int(screen_height * 0.8)
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        self.cropping = False
        self.ref_point = []
        self.current_point = ()
        self.paused = True

        self.cap = cv2.VideoCapture(video_file)
        if not self.cap.isOpened():
            messagebox.showerror("Error", f"Could not open video file {video_file}.")
            self.root.destroy()

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_index = 0
        self.current_frame = None

        # UI 요소 추가
        self.video_frame = ttk.Frame(self.root)
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.video_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(fill=tk.X)

        self.play_button = ttk.Button(self.control_frame, text="Play", command=self.toggle_play)
        self.play_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.root.bind("<Button-1>", self.mouse_callback)
        self.root.bind("<Motion>", self.mouse_motion)
        self.root.bind("<ButtonRelease-1>", self.mouse_release)

        self.update_video()

    def toggle_play(self):
        self.paused = not self.paused
        self.play_button.config(text="Pause" if not self.paused else "Play")

    def mouse_callback(self, event):
        if self.current_frame is not None:
            x, y = self.translate_coordinates(event.x, event.y)
            self.ref_point = [(x, y)]
            self.cropping = True

    def mouse_motion(self, event):
        if self.cropping and self.current_frame is not None:
            x, y = self.translate_coordinates(event.x, event.y)
            self.current_point = (x, y)

    def mouse_release(self, event):
        if self.cropping and self.current_frame is not None:
            x, y = self.translate_coordinates(event.x, event.y)
            self.ref_point.append((x, y))
            self.cropping = False

            # 크롭 및 저장
            x1, y1 = self.ref_point[0]
            x2, y2 = self.ref_point[1]
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            cropped_frame = self.current_frame[y1:y2, x1:x2]
            crop_filename = f"./output/crop_frame_{self.frame_index}.png"
            json_filename = f"./output/crop_frame_{self.frame_index}.json"

            cv2.imwrite(crop_filename, cropped_frame)

            crop_data = {
                "frame_index": self.frame_index,
                "crop_coordinates": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                "saved_file": crop_filename
            }

            save_to_json(crop_data, json_filename)
            messagebox.showinfo("Saved", f"Saved: {crop_filename}\n{json_filename}")

    def translate_coordinates(self, canvas_x, canvas_y):
        video_width = self.current_frame.shape[1]
        video_height = self.current_frame.shape[0]
        scale_x = video_width / self.canvas.winfo_width()
        scale_y = video_height / self.canvas.winfo_height()
        return int(canvas_x * scale_x), int(canvas_y * scale_y)

    def update_video(self):
        if not self.paused and not self.cropping:  # 드래그 중에는 프레임 갱신 중지
            ret, frame = self.cap.read()
            if not ret:
                self.paused = True
                self.play_button.config(text="Play")
                return

            self.frame_index += 1
            self.current_frame = frame.copy()

        if self.current_frame is not None:
            display_frame = self.current_frame.copy()
            if self.cropping and len(self.ref_point) == 1:
                cv2.rectangle(display_frame, self.ref_point[0], self.current_point, (255, 0, 0), 2)

            display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            display_frame = cv2.resize(display_frame, (self.window_width, self.window_height))
            img = ImageTk.PhotoImage(Image.fromarray(display_frame))

            self.canvas.img = img
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)

        self.root.after(int(1000 / self.fps), self.update_video)

    def on_close(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
