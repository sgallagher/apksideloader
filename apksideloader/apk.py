import gi
import logging

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa


class ApkStatus:

    def __init__(self, name):
        self.src_path = name
        self.label = Gtk.Label(label=name)
        self.progress = Gtk.ProgressBar()
        self.info_label = Gtk.Label()

    def update_progress(self, filename, bytes_written, total_bytes):
        if total_bytes > 0:
            self.progress.set_fraction(float(bytes_written) / float(total_bytes))
            logging.debug("{} / {} = {}".format(bytes_written, total_bytes, self.progress.get_fraction()))
        else:
            self.progress.pulse()

    def info(self, message):
        self.info_label.set_markup(message)

    def succeed(self):
        self.info_label.set_markup('<span foreground="green">Succeeded</span>')

    def fail(self, error):
        self.info_label.set_markup('<span foreground="red">{}</span>'.format(error))
