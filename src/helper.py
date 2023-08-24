from youtube_transcript_api import YouTubeTranscriptApi
import pafy

def extract_title(url):
    video = pafy.new(url)
    print('Title and duration extraction completed')
    return video.title

def url_parser(url):
    return url.split('?v=')[1]

def transcript_process(url_transcript):
    texts=[]
    try:
        for text in YouTubeTranscriptApi.get_transcript(url_transcript):
            texts.append(text['text'].strip('\n').replace('\n',' '))
        return (' ').join(texts)
    except:
        return "Transcript not found"