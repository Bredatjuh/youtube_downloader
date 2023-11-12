from pytube import YouTube
import ffmpeg
import os

file_name = 'youtube_list.txt'
with open(file_name) as file:
    myList = [i for i in file.read().strip().split("\n")]

def Video_info(link):
    """returns video info, this is helpfull if the current itags aren't working"""
    count = []
    for i in str(YouTube(link).streams.last).strip().split("<Stream:")[1:]:
        print(i)
        count.append(i)
    print(f"\nThere are {len(count)} ITAGS")

def Download_song(link):
    """Downloads audio of youtube link"""
    mov_title = YouTube(link).title.replace('/','').replace('"','').replace("'","").replace("|","").replace("(","").replace(")","")[0:35]
    filename_audio = f"{mov_title}_audio.mp4"
    hd_aud = {258:"384kbps",141:"256kbps",251:"160kbps",140:"128kbps"}
    for key,value in hd_aud.items():
        try:
            YouTube(link).streams.get_by_itag(key).download(filename=filename_audio)
            print(f"Song {filename_audio}\n(itag {key} - {value}) download is completed successfully")
            break
        except:
            print(f"An error has occurred with {filename_audio},\nitag {value} is not available")

def Download_video(link):
    """Downloads video of youtube link"""
    mov_title = YouTube(link).title.replace('/','').replace('"','').replace("'","").replace("|","").replace("(","").replace(")","")[0:35]
    filename_video = f"{mov_title}_video.mp4"
    hd_vid = {401:"4k",313:"4k",271:"2k",399:"1080p",248:"1080p",137:"1080p"}
    for key,value in hd_vid.items():
        try:
            YouTube(link).streams.get_by_itag(key).download(filename=filename_video)
            print(f"Movie {filename_video},\n(itag {key} - {value}) download is completed successfully")
            break
        except:
            print(f"An error has occurred with {filename_video},\nitag {key} ({value}) is not available")

def Merge(link):
    """Merges video and audio of youtube link"""
    mov_title = YouTube(str(link)).title
    mov_title = mov_title.replace('/','').replace('"','').replace("'","").replace("|","").replace("(","").replace(")","")[0:35]
    video = ffmpeg.input(f"{mov_title}_video.mp4")
    audio = ffmpeg.input(f"{mov_title}_audio.mp4")
    
    # combines video and audio together
    try:
        ffmpeg.concat(video, audio, v=1, a=1).output(f'{mov_title}.mp4').run(overwrite_output=True)
        print("Merge is completed successfully")
    
        # removes old video file
        os.remove(f"{mov_title}_video.mp4") 
        print(f"{mov_title}_video.mp4 is removed")

    except:
        print(f"""\nThere was an issue with combining the files.\ncheck if {mov_title}_video.mp4 and {mov_title}_audio.mp4 are available\nIf not try using info to find the right ITAGS!""")
        # quit

link = input(f"""\n\n\n\n\n
Hi there!
Welcome to this cute youtube downloader.

Would you like to download a song?                  --> type in "song" 
Would you like to download multiple songs?          --> type in "songs"
Make sure you have your links append to
{os.getcwd()}/youtube_list.txt

Would you like to download a video?                 --> type in "video" 
Would you like to download multiple videos?         --> type in "videos"
Make sure you have your links append to
{os.getcwd()}/youtube_list.txt

Are you having issues with ITAGS?                   --> type in "info"
Do you wanna leave?                                 --> type in "quit"
""")

if      link == "song":
        link_1 = input("What is the youtube link?:\n")
        print("\nDownloading audio....")
        Download_song(link_1)

elif    link == "songs":
        print("\nDownloading audio....")
        for i in myList:
            Download_song(i)

elif    link == "video":
        link_1 = input("What is the youtube link?:\n")
        print("\nDownloading audio....")
        Download_song(link_1)
        print("\nDownloading video....")
        Download_video(link_1)
        print("\nCombining files....")
        Merge(link_1)

elif    link == "videos":
        for i in myList:
            try:
                print("\nDownloading audio....")
                Download_song(i)
                print("\nDownloading video....")
                Download_video(i)
                print("\nCombining files....")
                Merge(i)
            except:
                print(f"merge failed {i}")
elif    link == "info":
        info = input("What is the youtube link?:\n")
        Video_info(info)

elif    link == "quit":
        quit

else:
    print("""wrong input.\nplease try again.""")
    quit