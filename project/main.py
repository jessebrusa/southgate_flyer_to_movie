import os
import tkinter as tk 
from tkinter import filedialog 
import cv2
import time


class FlyerToMovie():

    def __init__(self):
        self.custom_font = ("Helvetica", 20)
        self.gui()
        self.browse_for_folder()
        self.create_movie()


    def gui(self):
        self.gui_root = tk.Tk()
        self.gui_root.geometry("600x150")
        self.gui_root.title("Flyer Range")

        label = tk.Label(self.gui_root, text="What is the date range of flyers?:",
                         font=self.custom_font)
        label.pack(padx=5, pady=5)

        self.gui_entry = tk.Entry(self.gui_root, font=self.custom_font, width=30)
        self.gui_entry.pack(padx=5, pady=5)

        button = tk.Button(self.gui_root, text="Submit", command=self.get_input,
                           width=20, height=5)
        button.pack(padx=5, pady=5)

        self.gui_root.bind("<Return>", self.get_input)

        self.gui_root.mainloop()


    def get_input(self, event=None):
        self.user_input_date = self.gui_entry.get()
        self.gui_root.destroy()


    def browse_for_folder(self):
        root = tk.Tk()
        root.withdraw()

        self.folder_path = filedialog.askdirectory()

        root.destroy()


    def create_movie(self):
        self.loading_root = tk.Tk()
        self.loading_root = tk.Toplevel(self.loading_root)
        self.loading_root.wm_attributes('-topmost', 1)
        self.loading_label = tk.Label(self.loading_root, text="Loading....",
                         font=self.custom_font)
        self.loading_label.pack(padx=10, pady=10)
        self.loading_root.update()
        

        output_file = f'{self.folder_path}/{self.user_input_date}.mp4'
        frame_size = (1920, 1080)
        fps = .5
        image_duration = 8
        frames_per_image = int(fps * image_duration)

        image_files = sorted([f for f in os.listdir(self.folder_path) if f.endswith('.jpg')])
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        video_writer = cv2.VideoWriter(output_file, fourcc, fps, frame_size)

        for file_name in image_files:
            file_path = os.path.join(self.folder_path, file_name)
            img = cv2.imread(file_path)
            img = cv2.resize(img, frame_size)
            video_writer.write(img)

            for _ in range(frames_per_image):
                video_writer.write(img)

        video_writer.release()

        self.loading_label.config(text='Complete!')
        self.loading_root.update()
        
        
        time.sleep(5)
        self.loading_root.destroy()


flyer_to_movie = FlyerToMovie()