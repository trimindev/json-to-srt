import tkinter as tk
import json
import os
import re
from gui_utils import create_entry, create_button, create_status_label


class SRTConverter:
    def __init__(self, root):
        self.root = root
        root.title("Capcut JSON to SRT Converter")

        self.input_entry = create_entry(
            self, "Capcut Drafts Folder:", 0, isFolder=True, isBrowse=True
        )

        self.folder_name_entry = create_entry(self, "Folder Name:", 1)

        self.output_entry = create_entry(self, "Output Folder:", 2, isBrowse=True)

        # Convert Button
        self.convert_button = create_button(
            self, "Convert", command=self.convert_to_srt, row=3
        )

        # Status Label
        self.status_label = create_status_label(self, "", row=4)

        self.load_path_from_json()

    def extract_data(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def ms_to_srt(self, time_in_ms):
        convert_ms = int(time_in_ms / 1000)
        ms = int(convert_ms % 1000)
        total_seconds = int((convert_ms - ms) / 1000)
        seconds = total_seconds % 60
        total_minutes = int((total_seconds - seconds) / 60)
        minutes = total_minutes % 60
        hour = int((total_minutes - minutes) / 60)
        return f"{hour:02d}:{minutes:02d}:{seconds:02d},{ms:03d}"

    def clean_captions(self, srt_content):
        # Remove '?' and lines starting with '- '
        cleaned_content = re.sub(r"\?|- ", "", srt_content)

        # Merge caption lines into one line
        merged_content = re.sub(
            r"(?<=\d{2}:\d{2}:\d{2},\d{3}\n)([^\n]+)\n([^\n]+)\n",
            r"\1 \2\n",
            cleaned_content,
        )

        return merged_content

    def convert_to_srt(self):
        input_folder = self.input_entry.get()
        output_folder = self.output_entry.get()
        folder_name = self.folder_name_entry.get()
        input_filename = os.path.join(input_folder, folder_name, "draft_content.json")
        output_filename = os.path.join(output_folder, folder_name, "converted.srt")

        # Lưu đường dẫn vào file json
        self.save_path_to_json(input_folder, folder_name)

        data = self.extract_data(input_filename)
        materials = data["materials"]
        tracks = data["tracks"]

        subtitles_info = [
            {
                "content": json.loads(i["content"])["text"],
                "id": i["id"],
            }
            for i in materials["texts"]
        ]

        sub_track_number = 1
        sub_timing = tracks[sub_track_number]["segments"]

        for s in subtitles_info:
            segment = next((i for i in sub_timing if i["material_id"] == s["id"]), None)
            while not segment:
                sub_track_number += 1
                sub_timing = tracks[sub_track_number]["segments"]
                segment = next(
                    (i for i in sub_timing if i["material_id"] == s["id"]), None
                )
            s["start"] = segment["target_timerange"]["start"]
            s["end"] = s["start"] + segment["target_timerange"]["duration"]
            s["srt_start"] = self.ms_to_srt(s["start"])
            s["srt_end"] = self.ms_to_srt(s["end"])

        with open(output_filename, "w", encoding="utf-8") as output_file:
            for i, s in enumerate(subtitles_info):
                output_file.write(
                    f"{i+1}\n{s['srt_start']} --> {s['srt_end']}\n{s['content']}\n\n"
                )

        self.status_label.config(text="Conversion completed!")

    def save_path_to_json(self, input_folder, folder_name):
        path_data = {"input_folder": input_folder, "folder_name": folder_name}
        json_file_path = "saved_path.json"
        with open(json_file_path, "w") as json_file:
            json.dump(path_data, json_file)

    def load_path_from_json(self):
        json_file_path = "saved_path.json"
        if os.path.exists(json_file_path):
            with open(json_file_path, "r") as json_file:
                path_data = json.load(json_file)
                input_folder = path_data.get("input_folder", "")
                folder_name = path_data.get("folder_name", "")
                self.input_entry.insert(0, input_folder)
                self.folder_name_entry.insert(0, folder_name)


if __name__ == "__main__":
    root = tk.Tk()
    srt_converter = SRTConverter(root)
    root.mainloop()
