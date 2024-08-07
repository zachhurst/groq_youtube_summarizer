# YouTube Video Chat and Summary Helper
# This script allows you to interactively chat with an AI to generate a summary of any YouTube video using its transcript via the Groq API.
# Here's a step-by-step guide on what this script does and how to get started:

## Description:
# 1. Provide a YouTube URL when prompted.
# 2. Chat with the AI by optionally providing custom prompts. Ask questions or specify how you want the summary!
# 3. The script fetches the transcript of the video, uses the Groq API to generate a summary, answers your questions, and saves the conversation as a markdown file.
# 4. Both the transcript and the markdown file are saved in a folder named after the video ID from the YouTube URL, ensuring each folder is unique to its corresponding video.
# 5. Markdown files are updated in real-time with the chat conversation history.
# 6. The user can continue to interact with the AI until they type "exit" or "quit" to end the session.

## Features:
# - Interactive Chat: Engage in a conversation with the AI for personalized summarization.
# - Custom Prompts: Tailor the summary or ask specific questions about the video content.
# - Automatic Saving: The entire chat conversation and generated summary are saved in a markdown file.
# - Organized Storage: The transcript and summary are stored in a dedicated folder for each video.
# - Continuous Interaction: Keep the interaction going with multiple prompts until you decide to exit.

## Installation Instructions:
# Before running the script, you need to install the necessary Python libraries. You can do this by running:
# pip install requests youtube-transcript-api

## Environment Variable Setup:
# The script requires the Groq API key to be set as an environment variable.
# To set the environment variable, you can use the following instructions:

### Temporary Setting (current terminal session only):
# export GROQ_API_KEY="your_groq_api_key"

### Permanent Setting (for future terminal sessions):
# Add the following line to your shell's configuration file (e.g., ~/.zshrc or ~/.bash_profile):
# export GROQ_API_KEY="your_groq_api_key"
# Then reload your shell configuration:
# source ~/.zshrc  # Or source ~/.bash_profile if using bash

# Once the environment variable is set, you can run the script as usual:
# python your_script.py

import requests
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi

# Fetch the Groq API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set.")

# Set the default prompt for summaries
DEFAULT_PROMPT = "Provide a 3 paragraph summary of the following video transcript with styled markdown:"

# Set the model to use for chat completions
MODEL = "llama-3.1-8b-instant"

# Create a dictionary to store session information
session = {}

# Define a function to extract the video ID from a YouTube URL
def extract_video_id(youtube_url):
    video_id = re.search(r'v=([^&]+)', youtube_url)
    return video_id.group(1) if video_id else None

# Define a function to get the transcript of a video using its video ID
def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = ' '.join([t['text'] for t in transcript])
    return transcript_text

# Define a function to create a directory named after the video ID
def create_directory(video_id):
    if not os.path.exists(video_id):
        os.makedirs(video_id)

# Define a function to save the transcript to a text file using the video ID
def save_transcript_as_text(transcript_text, video_id):
    create_directory(video_id)
    filename = os.path.join(video_id, f"{video_id}_transcript.txt")
    with open(filename, "w") as txt_file:
        txt_file.write(transcript_text)

# Define a function to get a summary from Groq using the provided transcript and prompt
def get_summary(transcript_text, user_prompt=None):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {
                "role": "user",
                "content": f"{user_prompt if user_prompt else DEFAULT_PROMPT}\n\n{transcript_text}"
            }
        ],
        "model": MODEL
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()  # Raise an error for bad responses
    summary = response.json()["choices"][0]["message"]["content"].strip()
    return summary

# Define a function to save or update the summary as a markdown file with the video ID
def save_summary_as_markdown(user_input, summary, video_id):
    create_directory(video_id)
    filename = os.path.join(video_id, f"{video_id}.md")
    with open(filename, "a") as md_file:
        md_file.write(f"**User:** {user_input}\n\n**Assistant:** {summary}\n\n")

# Main function to run the script
def main():
    # Check if the user has a previous session
    if "youtube_url" not in session:
        youtube_url = input("Enter YouTube URL: ")
        session["youtube_url"] = youtube_url
    else:
        youtube_url = session["youtube_url"]
        print(f"Resuming session for YouTube URL: {youtube_url}")

    # Extract the video ID from the URL
    video_id = extract_video_id(youtube_url)
    if not video_id:
        print("Invalid YouTube URL")
        return

    # Fetch the transcript of the video
    try:
        transcript_text = get_transcript(video_id)
        save_transcript_as_text(transcript_text, video_id)  # Save the fetched transcript to a text file
        print(f"Transcript saved to {video_id}/{video_id}_transcript.txt")
    except Exception as e:
        print(f"Error fetching the transcript: {e}")
        return

    while True:
        # Prompt the user for a custom prompt or exit command
        user_input = input("> ").strip()
        # Exit loop if the user types "exit" or "quit"
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Generate the summary with Groq
        try:
            summary = get_summary(transcript_text, user_input)
            print(f"**User:** {user_input}")
            print(f"**Assistant:** {summary}")
            # Save or update the summary to a markdown file
            save_summary_as_markdown(user_input, summary, video_id)
            print(f"Summary saved to {video_id}/{video_id}.md")
        except Exception as e:
            print(f"Error generating summary: {e}")
            return

if __name__ == "__main__":
    main()  # Start the script