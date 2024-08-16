# from flask import Flask, request
# from youtube_transcript_api import YouTubeTranscriptApi
# from transformers import pipeline

# app = Flask(__name__)

# @app.get('/summary')
# def summary_api():
#     url = request.args.get('url', '')
#     video_id = url.split('=')[1]
#     summary = get_summary(get_transcript(video_id))
#     return summary, 200

# def get_transcript(video_id):
#     transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
#     transcript = ' '.join([d['text'] for d in transcript_list])
#     return transcript

# def get_summary(transcript):
#     summariser = pipeline('summarization')
#     summary = ''
#     for i in range(0, (len(transcript)//1000)+1):
#         summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
#         summary = summary + summary_text + ' '
#     return summary
    

# if __name__ == '__main__':
#     app.run()
# from flask import Flask, request
# from youtube_transcript_api import YouTubeTranscriptApi
# from transformers import pipeline
# from flask_cors import CORS
# import re

# app = Flask(__name__)
# CORS(app)

# def get_video_id(url):
#     # Handle various YouTube URL formats
#     video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
#     if video_id_match:
#         return video_id_match.group(1)
#     return None

# @app.get('/summary')
# def summary_api():
#     url = request.args.get('url', '')
#     video_id = get_video_id(url)
#     if not video_id:
#         return "Invalid YouTube URL", 400
#     transcript = get_transcript(video_id)
#     if not transcript:
#         return "Failed to retrieve transcript", 500
#     summary = get_summary(transcript)
#     return summary, 200

# def get_transcript(video_id):
#     try:
#         transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
#         transcript = ' '.join([d['text'] for d in transcript_list])
#         return transcript
#     except Exception as e:
#         print(f"Error retrieving transcript: {e}")
#         return None

# def get_summary(transcript):
#     if not transcript:
#         return "Transcript could not be retrieved"
#     try:
#         summariser = pipeline('summarization')
#         summary = ''
#         for i in range(0, (len(transcript)//1000)+1):
#             summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
#             summary = summary + summary_text + ' '
#         return summary
#     except Exception as e:
#         print(f"Error during summarization: {e}")
#         return "Error during summarization"

# if __name__ == '__main__':
#     app.run()
from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

def get_video_id(url):
    # Handle various YouTube URL formats
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    if video_id_match:
        return video_id_match.group(1)
    return None

@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    print(f"Received URL: {url}")
    video_id = get_video_id(url)
    if not video_id:
        return "Invalid YouTube URL", 400
    print(f"Video ID: {video_id}")
    transcript = get_transcript(video_id)
    if 'Error' in transcript:
        print(f"Error: {transcript}")
        return transcript, 500
    summary = get_summary(transcript)
    print(f"Summary: {summary}")
    return summary, 200

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([d['text'] for d in transcript_list])
        return transcript
    except Exception as e:
        return f"Error retrieving transcript: {str(e)}"

def get_summary(transcript):
    if 'Error retrieving transcript' in transcript:
        return transcript
    try:
        summariser = pipeline('summarization')
        summary = ''
        for i in range(0, (len(transcript)//1000)+1):
            summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
            summary = summary + summary_text + ' '
        return summary
    except Exception as e:
        return f"Error during summarization: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
