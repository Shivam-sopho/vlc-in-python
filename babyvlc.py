import sys
import gi
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('GdkX11', '3.0')
from gi.repository import GdkX11
from threading import Timer

import vlc
MRL = ""
now_time = time.localtime(time.time())


class ApplicationWindow(Gtk.Window):
    def __init__(self):

        Gtk.Window.__init__(self, title="My VLC")
        self.connect("delete-event", Gtk.main_quit)
        self.is_player_active = False
        self.is_paused = False
        # Setting the images for the buttons

    def show(self): self.show_all()

    def setup_objects_and_events(self):
        self.play_button = Gtk.Button()
        self.stop_button = Gtk.Button()
        self.play_image = Gtk.Image.new_from_icon_name(
            "media-playback-start", Gtk.IconSize.MENU
        )
        self.pause_image = Gtk.Image.new_from_icon_name(
            "media-playback-pause", Gtk.IconSize.MENU
        )
        self.stop_image = Gtk.Image.new_from_icon_name(
            "media-playback-stop",
            Gtk.IconSize.MENU
        )
        self.play_button.set_image(self.play_image)
        self.stop_button.set_image(self.stop_image)

        self.play_button.connect("clicked", self.toggle_play_pause)
        self.stop_button.connect("clicked", self.toggle_stop)

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(500, 500)

        self.drawing_area.connect("realize", self._realized)

        self.hbox = Gtk.Box(spacing=10)
        self.hbox.pack_start(self.play_button, True, True, 0)
        self.hbox.pack_start(self.stop_button, True, True, 0)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.vbox.pack_start(self.drawing_area, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)

    def toggle_stop(self, widget, data=None):
        """
        Handler for the stop Button
        """
        self.player.stop()
        self.is_player_active = False
        self.play_button.set_image(self.play_image)
   
    def toggle_play_pause(self, widget, data=None):
        """
        Handler for the play/pause button
        """
        def wait():
            self.player.pause()
            self.is_paused = True

        if self.is_player_active == False and self.is_paused == False:
            self.player.play()
            self.play_button.set_image(self.pause_image)
            self.is_player_active = True
            print("1st")

        elif self.is_player_active == True and self.is_paused == True:
#            win = Gtk.Window()
#            win.maximize()
            self.player.play()
            self.play_button.set_image(self.pause_image)
            self.is_paused = False
            t = Timer(5*60,wait)
            t.start()
            
                
        elif self.is_player_active == True and self.is_paused == False:
            self.player.pause()
            self.play_button.set_image(self.play_image)
            self.is_paused = True
            print("Hello")
        else:
            pass

    def _realized(self, widget, data=None):
        """
         Handler for the realization of the window
        """
        self.instance = vlc.Instance("--no-xlib")
        self.player = self.instance.media_player_new()
        win = widget.get_window().get_xid()
        self.player.set_xwindow(win)
        self.player.set_mrl(MRL)
        self.player.play()
        self.play_button.set_image(self.pause_image)
        self.is_player_active = True


if __name__ == '__main__':
    if not sys.argv[1:]:

        print("Please Enter the (relative)location of the Video to be played")
        sys.exit(1)
    else:
        MRL = sys.argv[1]
        window = ApplicationWindow()
        window.setup_objects_and_events()
        window.show_all()
        Gtk.main()
        window.player.stop()
        window.instance.release()

