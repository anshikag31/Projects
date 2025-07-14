# 🎯 Player Re-Identification in a Single Feed

## Objective

This project simulates **real-time re-identification and tracking** of players in a 15-second video. The task involves detecting players, assigning unique track IDs, and ensuring **consistency of player identity even after occlusion or reappearance**.


## Input

- **Video**: `input.mp4`
- **Model**: Fine-tuned YOLOv11 trained on players and ball.

## Download Model - https://drive.google.com/file/d/1-5fOSHOSB9UXYPenOoZNAMScrePVcMD/view


## Features

- Real-time player detection and tracking using YOLOv11.
- Player re-identification after temporary absence.
- CSV export of tracking results (`frame_number`, `track_id`, `x1`, `y1`, `x2`, `y2`).

## Directory Structure

Player Reidentification/
│
├── videos/ # Helper scripts for matching, drawing, etc.
   ├── input
   ├── output
   ├── tracking_log.csv
├── track_players.py
├── README.md # Setup & run instructions
├── Report.pdf # Brief project report
├── requirements.txt

## Dependencies

opencv-python
ultralytics
deep-sort-realtime
Python 3.8+
Pandas
NumPy

## Output video link: https://drive.google.com/file/d/1UyCZyp8kb1qQq9sQ1PutHQUW-E-yu5vq/view?usp=sharing

