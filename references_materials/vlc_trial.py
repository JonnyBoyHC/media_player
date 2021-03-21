# import pafy
# import vlc
# import time

# # Program 1
# url = 'https://www.youtube.com/watch?v=oCKrKtk-rDw'
# video = pafy.new(url)
# best = video.getbest()
# play_url = best.url
#
# Instance = vlc.Instance()
# player = Instance.media_player_new()
# Media = Instance.media_new(play_url)
# Media.get_mrl()
# player.set_media(Media)
# player.play()
#
# time.sleep(50)

# # Program 2
# # method to play video
# def video(source):
#     # creating a vlc instance
#     vlc_instance = vlc.Instance()
#
#     # creating a media player
#     player = vlc_instance.media_player_new()
#
#     # creating a media
#     media = vlc_instance.media_new(source)
#
#     # setting media to the player
#     player.set_media(media)
#
#     # play the video
#     player.play()
#
#     # wait time
#     time.sleep(0.5)
#
#     # getting the duration of the video
#     duration = player.get_length()
#
#     # printing the duration of the video
#     print("Duration : " + str(duration))
#
#
# # call the video method
# video("Jon Schmidt  Steven Nelson - Love Story Viva la Vida Medley.mp4")

# # Program 3
# # url of the video
# url = "https://www.youtube.com/watch?v=il_t1WVLNxk&list=PLqM7alHXFySGqCvcwfqqMrteqWukz9ZoE"
#
# # creating pafy object of the video
# video = pafy.new(url)
#
# # getting stream at index 0
# best = video.streams[0]
#
# # creating vlc media player object
# media = vlc.MediaPlayer(best.url)
#
# # start playing video
# media.play()

# # Program 4
#
# # importing vlc module
# import vlc
#
# # importing time module
# import time
#
# # creating a media player object
# media_player = vlc.MediaListPlayer()
#
# # creating Instance class object
# player = vlc.Instance()
#
# # creating a new media list object
# media_list = player.media_list_new()
#
# # creating a new media
# media = player.media_new("Jon Schmidt  Steven Nelson - Love Story Viva la Vida Medley.mp4")
#
# # adding media to media list
# media_list.add_media(media)
#
# # setting media list to the media player
# media_player.set_media_list(media_list)
#
# # start playing video
# media_player.play()
#
# # wait so the video can be played for 5 seconds
# # irrespective for length of video
# time.sleep(120)
#
# # getting media player current state
# value = media_player.get_state()
#
# # printing value
# print(value)


# Program 5
# import os, time

# # Set the VLC library path, before import vlc
# os.environ['PYTHON_VLC_MODULE_PATH'] = "./vlc-3.0.6"

import vlc


class Player:
    """
                 args: set options
    """

    def __init__(self, *args):
        if args:
            instance = vlc.Instance(*args)
            self.media = instance.media_player_new()
        else:
            self.media = vlc.MediaPlayer()

    # Set the URL address or local file path to be played, and the resource will be reloaded every time it is called
    def set_uri(self, uri):
        self.media.set_mrl(uri)

    # Play success returns 0, failure returns -1
    def play(self, path=None):
        if path:
            self.set_uri(path)
            return self.media.play()
        else:
            return self.media.play()

    # time out
    def pause(self):
        self.media.pause()

    # Restore
    def resume(self):
        self.media.set_pause(0)

    # stop
    def stop(self):
        self.media.stop()

    # Release resources
    def release(self):
        return self.media.release()

    # Is it playing
    def is_playing(self):
        return self.media.is_playing()

    # Elapsed time, return millisecond value
    def get_time(self):
        return self.media.get_time()

    # Drag the specified millisecond value to play. Return 0 on success, -1 on failure (note that only the current
    # multimedia format or streaming media protocol support will take effect)
    def set_time(self, ms):
        return self.media.get_time()

    # The total length of audio and video, returns the value in milliseconds
    def get_length(self):
        return self.media.get_length()

    # Get the current volume (0~100)
    def get_volume(self):
        return self.media.audio_get_volume()

    # Set the volume (0~100)
    def set_volume(self, volume):
        return self.media.audio_set_volume(volume)

    # Return to the current state: playing; paused; other
    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    # Current playback progress. Returns a floating point number between 0.0 and 1.0
    def get_position(self):
        return self.media.get_position()

    # Drag the current progress and pass in a floating point number between 0.0 and 1.0 (note that only the current
    # multimedia format or streaming protocol support will take effect)
    def set_position(self, float_val):
        return self.media.set_position(float_val)

    # Get the current file playback rate
    def get_rate(self):
        return self.media.get_rate()

    # Set the playback rate (for example: 1.2, which means to speed up the playback by 1.2 times)
    def set_rate(self, rate):
        return self.media.set_rate(rate)

    # Set the aspect ratio (such as "16:9", "4:3")
    def set_ratio(self, ratio):
        self.media.video_set_scale(0)  # Must be set to 0, otherwise the screen width and height cannot be modified
        self.media.video_set_aspect_ratio(ratio)

    # Register listener
    def add_callback(self, event_type, callback):
        self.media.event_manager().event_attach(event_type, callback)

    # Remove listener
    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)


def my_call_back(event):
    print("call:", player.get_time())


if "__main__" == __name__:
    player = Player()
    player.add_callback(vlc.EventType.MediaPlayerTimeChanged, my_call_back)
    # Play streaming video online
    # player.play("https://www.youtube.com/watch?v=oCKrKtk-rDw")

    # Play local mp3
    player.play("Jon Schmidt  Steven Nelson - Love Story Viva la Vida Medley.mp4")

    # Prevent the current process from exiting
    while True:
        pass
