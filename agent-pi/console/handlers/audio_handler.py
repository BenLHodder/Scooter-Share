from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # Hide pygame support prompt
import pygame
import datetime
import os

class audio_handler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(audio_handler, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialised'):
            script_dir = os.path.dirname(os.path.realpath(__file__))
            self.audio_file = os.path.join(script_dir, "bicycle-bell.mp3")
            self.initialised = True
        
    def play_bell(self, time: int):
        """
        Play the bell sound for a given amount of time.

        :param time: The time in seconds to play the sound for
        """
        pygame.mixer.init()
        pygame.mixer.music.load(self.audio_file)
        
        # Start time of the sound
        start_time = datetime.datetime.now()
        
        # Loop until the total time is met
        while (datetime.datetime.now() - start_time).seconds < time:
            pygame.mixer.music.play()  # Play the sound
            while pygame.mixer.music.get_busy():
                # Wait for the sound to finish
                pass
            
        # Stop the music after the time has passed
        pygame.mixer.music.stop()
        
# handler = AudioHandler()
# handler.play_bell(5)