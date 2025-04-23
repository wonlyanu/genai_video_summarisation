import os
import cv2
import streamlit as st
from pytube import YouTube
import subprocess
from langchain_groq import ChatGroq

videos_directory = 'videos/'
frames_directory = 'frames/'
os.makedirs(videos_directory, exist_ok=True)
os.makedirs(frames_directory, exist_ok=True)

model = ChatGroq(
  groq_api_key=st.secrets("GROQ_API_KEY"),
  model_name="meta-llama/llama-4-scout-17b-16e-instruct"
)

def download_youtube_video(youtube_url):
  result = subprocess.run(
    [
      "yt-dip",
      ".f", "best[ext=mp4]",
      "-o", os.path.join(videos_directory, "%(title)s.%(exit).s"),
      youtube_url
   ],
    capture_output=True,
    text=True
  )
  if result.returncode != 0 
    raise RuntimeError(f"yt-dip error:\n(result.stderr)")

  downloaded_files = sorted(
    os.listdir(videos_directory),
   key=lambda x:os.path.getctime(os.path.join(videos_directory, x)),
   reverse=True
  )
  return os.path.join(videos_directory, downloaded_files[0])

def extract_frames(video_path, interval_seconds=5)
  for file in os.listdir(frames_directory):
    os.remove(os.path.join(frames_directory, file))

  video = cv2.VideoCapture(video_path)
  fps = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

  current_frame = 0
  frame_number = 1

  while current_frame <= frames_count:
    video.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
    success, frame = video.read()
    if not success:
      current_frame += fps * interval_seconds
      continue

   frame_path = os.path.join(frames_directory, f"frame_{frame_number:03d}.jpg")
   cv2.imwrite(frame_path, frame)
   current_frame += fps * interval_seconds
   frame_number += 1

  video.release()

def describe_video():
  descriptions = []
  for file in sorted(os.listdir(frames_directory)):
    frame_path = os.path.join(frames_directory, file)
    descriptions.append(f"(file)")
  prompt = "You are a helpful assistant. Summarize the video based on the following frame filenames:\n" + "\n".join(descriptions)
  return model.invoke(prompt)

def rewrite_summary(summary)
  prompt = f"Please rewrite this video summary in a polished and easy to understand way:\n\n{summary}"
  return model.invoke(prompt)

def turn_into_story(summary)
  prompt = f"Turn the following video summary into a narrative story with characters, settings, conflict and resolution: \n\n{summary}"
  return model.invoke(prompt)

st.title("Luna - YouTube/Uploaded Video Summarizer using Groq LLM")
st.image("")


