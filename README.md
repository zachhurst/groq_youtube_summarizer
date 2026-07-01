# Groq YouTube Summarizer

A simple Python script that fetches a YouTube video's transcript and uses the Groq API to generate summaries, answer questions, and save the conversation as markdown.

## How It Works

1. Paste a YouTube URL
2. The script fetches the transcript via `youtube-transcript-api`
3. Ask questions or request summaries — the Groq LLM responds in real time
4. Transcripts and conversation history are saved to a folder named after the video ID

## Requirements

- Python 3.8+
- A Groq API key (free tier available at [console.groq.com](https://console.groq.com))

## Installation

```bash
pip install requests "youtube-transcript-api>=1.0.0"
```

## Setup

Set your Groq API key as an environment variable:

```bash
# Temporary (current session)
export GROQ_API_KEY="your_groq_api_key"

# Permanent (add to ~/.zshrc or ~/.bash_profile)
export GROQ_API_KEY="your_groq_api_key"
```

## Usage

```bash
python yt_summarizer-GROQ-llama-3.1-8b-instant.py
```

You'll be prompted for a YouTube URL, then can interactively ask questions about the video. Type `exit` or `quit` to end the session.

## Project History

This project was originally created in 2024 using Groq's `llama-3.1-8b-instant` model. It sat untouched for over two years until a July 2026 audit uncovered two breaking deprecations:

- **Groq model**: `llama-3.1-8b-instant` was deprecated on June 17, 2026 and decommissioned on August 16, 2026. Replaced with `openai/gpt-oss-20b`.
- **youtube-transcript-api**: The static `get_transcript()` method was deprecated in v1.0.0 (March 2025) and removed entirely in v1.2.0 (July 2025). Replaced with the instance-based `fetch()` API.

Both issues would have caused the script to crash on any fresh install with current dependencies.

## License

MIT
