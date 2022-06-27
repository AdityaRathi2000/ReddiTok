import pandas as pd
import praw
from pytube import YouTube
from gtts import gTTS
import os
import IPython
from pydub import AudioSegment
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops, ImageFilter
import textwrap
import random
from random import randint, randrange
import wave
import contextlib
from moviepy.editor import VideoFileClip
from moviepy.editor import *
import moviepy.editor as mp
from mutagen.mp3 import MP3
from moviepy.video.fx.all import crop

def setingUp():
    personal_use_script = '75FzK6A6WfwBjw'
    secret_use_script = 'pcExPZaMj3HDuy31A_TTmZdw7EB_KA'
    app_name = 'threatwatch_v1'
    reddit_username = 'Aditya_Rathi_4'
    login_password = '!1Threatwatch'

    reddit = praw.Reddit(client_id=personal_use_script, \
                         client_secret=secret_use_script, \
                         user_agent=app_name, \
                         username=reddit_username, \
                         password=login_password, check_for_async=False)

    return reddit

def setup_df(subreddit_name, filter):
    reddit = setingUp()

    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.top(filter)
    posts_dict = {"Title": [], "Post Text": [], "ID": [], "Author": []}

    for post in posts:
        # Title of each post
        posts_dict["Title"].append(post.title.replace("\n", ""))

        # Text inside a post
        posts_dict["Post Text"].append(post.selftext.replace("\n", ""))

        # Unique ID of each post
        posts_dict["ID"].append(post.id)

        # Author
        posts_dict["Author"].append(post.author)

        # Saving the data in a pandas dataframe
        top_posts = pd.DataFrame(posts_dict)

        # Set ID as index

    top_posts = top_posts.set_index('ID')
    return top_posts

#################################### Download subway surver video ####################################################

# link of the video to be downloaded
#path = '/content/drive/MyDrive/UPenn/Projects/RedditTok/Video Storage'
#link = "https://www.youtube.com/watch?v=hs7Z0JUgDeA&t=1105s"

#yt = YouTube(link)
#mp4_files = yt.streams.filter(file_extension="mp4")
#mp4_369p_files = yt.streams.get_highest_resolution()
#mp4_369p_files.download(path)
######################################################################################################################

def text_to_vid(testing_id, testing_text, testing_title):
    path = "/Users/adityarathi/PycharmProjects/RedditTok/Audio Storage/{}".format(testing_id)
    if not os.path.exists(path):
        os.mkdir(path)

    language = 'en'
    myobj = gTTS(text=testing_text, lang=language, slow=False)

    sound_path_in_mp3 = "/Users/adityarathi/PycharmProjects/RedditTok/Audio Storage/{}/{}.mp3".format(testing_id,
                                                                                                         testing_title)
    sound_path_in_wav = "/Users/adityarathi/PycharmProjects/RedditTok/Audio Storage/{}/{}.wav".format(testing_id,
                                                                                                         testing_title)

    myobj.save(sound_path_in_mp3)
    #sound = AudioSegment.from_mp3(sound_path_in_mp3)
    #sound.export(sound_path_in_wav, format="wav")

    return sound_path_in_mp3, sound_path_in_wav

def audio_len(path_to_audio):
    audio = MP3(path_to_audio)
    return audio.info.length

def screenshot_creating(testing_id, testing_text):
    NUM_ROWS = 9
    novo = textwrap.wrap(testing_text, width=53)
    big_screen = [novo[x:x + NUM_ROWS] for x in range(0, len(novo), NUM_ROWS)]
    total_audio_len = 0

    screenshot_counter = 1
    for screenshot in big_screen:
        img = Image.open('/Users/adityarathi/PycharmProjects/RedditTok/Screenshot Storage/black_back_copy.jpg')
        d1 = ImageDraw.Draw(img)
        myFont = ImageFont.truetype('/Users/adityarathi/PycharmProjects/RedditTok/Screenshot Storage/verdana.ttf',
                                    24)

        for i in range(len(screenshot)):
            from_left = 25

            if i == 0:
                from_top = 25
            else:
                from_top = 50 * (i) + 25

            d1.text((from_left, from_top), screenshot[i], fill=(255, 255, 255), font=myFont)

        full_string = ''.join(screenshot)
        sound_path_in_mp3, sound_path_in_wav = text_to_vid(testing_id, full_string.replace('AITA', 'Am I the Asshole'),
                                                           screenshot_counter)
        total_audio_len += audio_len(sound_path_in_mp3)
        img.save("/Users/adityarathi/PycharmProjects/RedditTok/Screenshot Storage/{}/{}.jpeg".format(testing_id,
                                                                                                        screenshot_counter))
        screenshot_counter += 1

    return total_audio_len, screenshot_counter


def mask_circle_solid(pil_img, background_color, offset=0):
    background = Image.new(pil_img.mode, pil_img.size, background_color)
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset + 1, offset + 1, pil_img.size[0] - offset - 1, pil_img.size[1] - offset - 1.05), fill=255)
    return Image.composite(pil_img, background, mask)


def make_title_ss(testing_id, testing_title, testing_author):
    path = "/Users/adityarathi/PycharmProjects/RedditTok/Screenshot Storage/{}".format(testing_id)
    if not os.path.exists(path):
        os.mkdir(path)

    img = Image.open('/Users/adityarathi/PycharmProjects/RedditTok/Screenshot Storage/title_final.png')
    im2 = Image.open('/Users/adityarathi/PycharmProjects/RedditTok/Screenshot Storage/reddit_acc_logo.png')
    d1 = ImageDraw.Draw(img)

    verdana_reg = ImageFont.truetype('/Users/adityarathi/PycharmProjects/RedditTok/Screenshot Storage/verdana.ttf',
                                     15)
    verdana_headline = ImageFont.truetype(
        '/Users/adityarathi/PycharmProjects/RedditTok/Screenshot Storage/verdana.ttf', 30)
    verdana_bold = ImageFont.truetype(
        '/Users/adityarathi/PycharmProjects/RedditTok/Screenshot Storage/verdana-bold.ttf', 15)

    d1.text((100, 15), "r/AmITheAsshole", fill=(169, 169, 169), font=verdana_bold)
    d1.text((100, 40), "u/{}".format(testing_author), fill=(30, 144, 255), font=verdana_reg)
    d1.text((245, 40), " • {}h".format(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])), fill=(169, 169, 169),
            font=verdana_reg)

    novo = textwrap.wrap(testing_title, width=53)
    for i in range(len(novo)):
        from_top = 50 * (i) + 80
        d1.text((50, from_top), novo[i], fill=(192, 192, 192), font=verdana_headline)

    im2_resize = im2.resize((50, 50))
    im2_resize = mask_circle_solid(im2_resize, (0, 0, 0))
    img.paste(im2_resize, (30, 15))

    sound_path_in_mp3, sound_path_in_wav = text_to_vid(testing_id, testing_title.replace('AITA', 'Am I the Asshole'),
                                                       "title")
    img.save("/Users/adityarathi/PycharmProjects/RedditTok/Screenshot Storage/{}/title.png".format(testing_id))

    return audio_len(sound_path_in_mp3)

# loading video dsa gfg intro video
def creating_small_vid(total_video_len, testing_id):
  clip = VideoFileClip("/Users/adityarathi/PycharmProjects/RedditTok/Video Storage/full_minecraft_video.mp4")
  start_of_vid = randint(100, int(clip.duration)-1000)

  clip = clip.subclip(start_of_vid, start_of_vid+total_video_len)  # REPLACE 5 with total_video_len
  clip_no_audio = clip.without_audio()
  (w, h) = clip_no_audio.size
  cropped_clip = crop(clip_no_audio, width=360, height=640, x_center=w/ 2, y_center=h / 2)
  #clip_no_audio_resize = clip_no_audio.resize(height=1920)
  #clip_no_audio_vertical = clip_no_audio_resize.crop(x1=1166.6, y1=0, x2=2246.6, y2=1920)

  path = "/Users/adityarathi/PycharmProjects/RedditTok/Video Storage/{}".format(testing_id)
  if not os.path.exists(path):
      os.mkdir(path)

  cropped_clip.write_videofile("/Users/adityarathi/PycharmProjects/RedditTok/Video Storage/{}/{}.mp4".format(testing_id, testing_id), verbose=False, logger=None)

def mark_as_completed(testing_id):
    with open('/Users/adityarathi/PycharmProjects/RedditTok/track.txt', 'a') as f:
        f.write('\n')
        f.write(testing_id)

def full_video_download(testing_id, screenshot_counter):
    ######### title stuff #############
    video = VideoFileClip(
        "/Users/adityarathi/PycharmProjects/RedditTok/Video Storage/{}/{}.mp4".format(testing_id, testing_id))
    title_audio = AudioFileClip(
        "/Users/adityarathi/PycharmProjects/RedditTok/Audio Storage/{}/title.mp3".format(testing_id))
    title_pic = (
        ImageClip("/Users/adityarathi/PycharmProjects/RedditTok/Screenshot Storage/{}/title.png".format(testing_id))
        .set_duration(title_audio.duration)
        .resize(height=60)  # if you need to resize...
        .margin(right=8, top=8, opacity=0)  # (optional) logo-border padding
        .set_position((50, 300)))
    video = video.set_audio(title_audio)
    ####################################

    full_composite = [title_pic]
    for i in range(1, screenshot_counter):
        ss_audio = AudioFileClip(
            "/Users/adityarathi/PycharmProjects/RedditTok/Audio Storage/{}/{}.mp3".format(testing_id, i))
        ss_image = (ImageClip(
            "/Users/adityarathi/PycharmProjects/RedditTok/Screenshot Storage/{}/{}.jpeg".format(testing_id, i))
                    .set_duration(ss_audio.duration)
                    .resize(height=205)  # if you need to resize...
                    .margin(right=8, top=8, opacity=0)  # (optional) logo-border padding
                    .set_position((40, 250)))
        ss_image = ss_image.set_audio(ss_audio)
        full_composite.append(ss_image)

    final_clip = concatenate_videoclips(full_composite).set_position((20, 220))
    final = mp.CompositeVideoClip([video, final_clip])
    final.write_videofile("/Users/adityarathi/PycharmProjects/RedditTok/Unuploaded_Complete_Videos/{}.mp4".format(testing_id),
                          audio_codec='aac', verbose=False, logger=None)

def main_func(subreddit, filter_by):
  top_posts = setup_df(subreddit, filter_by)

  num = 0
  for testing_id in top_posts.index:
    track_me = open("/Users/adityarathi/PycharmProjects/RedditTok/track.txt", "r")
    if testing_id not in track_me.read():
      print("[{}/{}] - Working on {}...".format(num, len(top_posts.index), testing_id))
      testing_title = top_posts.loc[testing_id, "Title"]
      testing_text = top_posts.loc[testing_id, "Post Text"]
      testing_author = top_posts.loc[testing_id, "Author"]

      title_audio_len = make_title_ss(testing_id, testing_title, testing_author)
      total_audio_len, screenshot_counter = screenshot_creating(testing_id, testing_text)
      total_video_len = title_audio_len+total_audio_len
      creating_small_vid(total_video_len, testing_id)
      full_video_download(testing_id, screenshot_counter)
      mark_as_completed(testing_id)
      print("Just Finished {}!".format(testing_id))
      num += 1
