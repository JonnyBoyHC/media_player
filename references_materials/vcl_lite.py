import pafy
import vlc
import time

# Program 1
url = 'https://www.youtube.com/watch?v=oCKrKtk-rDw'
video = pafy.new(url)
best = video.getbest()
play_url = best.url
#
Instance = vlc.Instance()
player = Instance.media_player_new()
Media = Instance.media_new(play_url)
Media.get_mrl()
player.set_media(Media)
player.play()

print(player.video_get_width(), player.video_get_height())

while True:
    time.sleep(1)    
    print("FPS: ", round(player.get_fps(), 4), ", Current Time: ", round(player.get_time()/1000), "s" )
#     print(player.get_stats())
    pass
