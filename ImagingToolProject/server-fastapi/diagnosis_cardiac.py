import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv
import os
from pathlib import Path
from typing import List
from multiprocessing import cpu_count
import pandas as pd
from ABI_subpixel import register_images

# AGG backend is for writing to file, not for rendering in a window
matplotlib.use('Agg')

class VideoProcess:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = None
        self.frames = []
        self.frame_count = 0
        self.registration_results = []
        self.registration_locations = []
        self.roi = None
    
    def load_video(self) -> bool:
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Error: Could not open video file {self.video_path}")
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return True
    
    def set_roi(self, x: int, y: int, width: int, height: int):
        self.roi = (x, y, width, height)
    
    def extract_frames(self, output_folder: str) -> List[np.ndarray]:
        frame_count = 0
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            if self.roi:
                x, y, w, h = self.roi
                frame = frame[y:y+h, x:x+w]

            frame_filename = os.path.join(output_folder, f"frame_{frame_count:03d}.png")
            cv2.imwrite(frame_filename, frame)
            self.frames.append(frame)
            frame_count += 1
        self.cap.release()
        return self.frames


class ImageRegistration:
    def __init__(self, frames: List[np.ndarray]):
        self.frames = frames
        self.intensities = []
        self.registration_results = []
        self.registration_locations = []

    def register_frames(self, frames_dir: str, results_dir: str) -> bool:
        frame_files = sorted([f for f in os.listdir(frames_dir) 
                            if f.startswith("frame_") and f.endswith(".png")])
        print(f"(∆π∆) Total number of frames decomposed: {len(frame_files)}")

        if len(frame_files) < 2:
            print("Not enough frames to perform registration. Exiting...")
            return False

        results_csv_path = os.path.join(results_dir, "registration_results.csv")
        with open(results_csv_path, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Frame", "Loc_Y", "Loc_X", "Disp_Y", "Disp_X"])

            reference_path = os.path.join(frames_dir, frame_files[1])
            reference_frame = cv2.imread(reference_path)

            if reference_frame is None:
                print(f"Failed to load reference frame: {reference_path}")
                return False

            for i, frame in enumerate(frame_files[1:]):
                current_frame = cv2.imread(os.path.join(frames_dir, frame))

                if current_frame is None:
                    print(f"Failed to load frame: {frame}")
                    continue

                try:
                    results, locs = register_images(
                        im1=reference_frame,
                        im2=current_frame,
                        plot=False,
                        threads=cpu_count() - 2,
                        stride=100,
                        windowsize=100,
                        thresh=10
                    )

                    for j in range(len(results)):
                        csv_writer.writerow([
                            i,
                            locs[j][1],
                            locs[j][0],
                            results[j][0][0],
                            results[j][0][1]
                        ])

                    self.registration_results.append(results)
                    self.registration_locations.append(locs)

                except Exception as e:
                    print(f"Error during registration of frame {i}: {e}")
                    continue

        return True
    

class DataVisualization:
    def __init__(self, results_dir: str):
        self.results_dir = results_dir
        self.csv_path = os.path.join(results_dir, "registration_results.csv")
        self.data = None

    def load_data(self) -> bool:
        try:
            self.data = pd.read_csv(self.csv_path)
            self.data["Total_Displacement"] = np.sqrt(
                self.data["Disp_X"] ** 2 + self.data["Disp_Y"] ** 2
            )
            print(f"(∆π∆) Data loaded, shape: {self.data.shape}")
            return True
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            return False
    
    def plot_displacements(self) -> bool:
        if self.data is None:
            print("No data loaded. Please load data first.")
            return False

        try:
            unique_points = self.data.groupby(["Loc_Y", "Loc_X"])
            num_points = len(unique_points)
            print(f"(∆π∆) Number of grid points: {num_points}")

            plt.figure(figsize=(12, 6))
            for (loc_y, loc_x), group in unique_points:
                plt.plot(group["Frame"], group["Total_Displacement"], "-", alpha=0.5,
                        label=f"Point ({loc_y}, {loc_x})")

            plt.xlabel('Frame Number')
            plt.ylabel('Total Displacement (pixels)')
            plt.title(f'Total Displacement over Frames for {num_points} Grid Points')
            plt.grid(True)
            plt.tight_layout()

            plot_path = os.path.join(self.results_dir, "total_displacement_plot.png")
            plt.savefig(plot_path)
            plt.close()
            return True
        except Exception as e:
            print(f"Error creating displacement plot: {e}")
            return False

async def process_video_sync(input_folder_path: str, frames_storage_path: str, results_storage_path: str, roi: dict=None) -> bool:
    print(f"(∆π∆)Input folder: {input_folder_path}")
    print(f"(∆π∆)Frames storage: {frames_storage_path}")
    print(f"(∆π∆)Results storage: {results_storage_path}")

    try:
        video_files = [f for f in os.listdir(input_folder_path) 
                      if f.lower().endswith(('.mp4', '.avi', '.mov'))]
        if not video_files:
            raise ValueError(f"No video files found in {input_folder_path}")

        video_path = os.path.join(input_folder_path, video_files[0])
        video_name = Path(video_files[0]).stem

        # Decompose video into frames
        processor = VideoProcess(video_path)
        processor.load_video()
        if roi:
            processor.set_roi(roi['x'], roi['y'], roi['width'], roi['height'])
        frames = processor.extract_frames(frames_storage_path)

        # Image registration
        analyzer = ImageRegistration(frames)
        analyzer.register_frames(frames_storage_path, results_storage_path)

        # Visualize results
        visualizer = DataVisualization(results_storage_path)
        
        if visualizer.load_data():
            visualizer.plot_displacements()

        return True
    except Exception as e:
        print(f"Error during video analysis: {e}")
        return False


async def video_cardiac_analyze(input_path: str, frames_path: str, results_path: str, roi: dict = None) -> bool:
    try:
        result = await process_video_sync(input_path, frames_path, results_path, roi)
        return result
    except Exception as e:
        print(f"Error in video cardiac analyze: {e}")
        return False
