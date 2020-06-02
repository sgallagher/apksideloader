import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="APK Sideloader")
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(10)
        self.grid.set_margin_start(10)
        self.grid.set_margin_end(10)
        self.grid.set_margin_top(10)
        self.grid.set_margin_bottom(10)
        self.add(self.grid)

        # Add header for the APKs
        self.header_file = Gtk.Label()
        self.header_file.set_markup('<span weight="bold">APK File</span>')
        self.grid.attach(child=self.header_file,
                         left=0,
                         top=0,
                         width=1,
                         height=1)

        self.header_progress = Gtk.Label()
        self.header_progress.set_markup('<span weight="bold">Progress</span>')
        self.grid.attach_next_to(child=self.header_progress,
                                 sibling=self.header_file,
                                 side=Gtk.PositionType.RIGHT,
                                 width=1,
                                 height=1)

        self.header_info = Gtk.Label()
        self.header_info.set_markup('<span weight="bold">Info</span>')
        self.grid.attach_next_to(child=self.header_info,
                                 sibling=self.header_progress,
                                 side=Gtk.PositionType.RIGHT,
                                 width=1,
                                 height=1)

        self.connect("destroy", Gtk.main_quit)

        # Start the APK index count at 1 so we don't overwrite the header
        self.apk_index = 1

    def add_apk(self, apk):
        # Create the label
        self.grid.attach(child=apk.label,
                         left=0,
                         top=self.apk_index,
                         width=1,
                         height=1)

        # Add the spinner
        self.grid.attach_next_to(child=apk.progress,
                                 sibling=apk.label,
                                 side=Gtk.PositionType.RIGHT,
                                 width=1,
                                 height=1)

        # Add the stderr output for later use
        self.grid.attach_next_to(child=apk.info_label,
                                 sibling=apk.progress,
                                 side=Gtk.PositionType.RIGHT,
                                 width=1,
                                 height=1)
