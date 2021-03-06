import click
import gi
import logging
import os
import queue
import threading

from adb_shell.auth.sign_pythonrsa import PythonRSASigner

from apksideloader.adb import CROSTINI_DEFAULT_ADB_SERVER, CROSTINI_DEFAULT_ADB_PORT
from apksideloader.adb import AdbConnection, AdbConnectionError

from apksideloader.apk import ApkStatus

from apksideloader.gui import MainWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa


def fail_apks(apks, message):
    while True:
        try:
            apk = apks.get(False)
        except queue.Empty:
            return

        apk.fail(message)
        apks.task_done()


def do_installs(conn, apks):
    # Connect to ADB Server
    try:
        conn.connect()
    except AdbConnectionError as e:
        fail_apks(apks, e)
        return

    # Install all of the requested APKs
    while not apks.empty():
        try:
            apk = apks.get(False)
        except queue.Empty:
            return

        try:
            conn.install_apk(apk)
        except Exception as e:
            fail_apks(apks, e)

        apks.task_done()


def worker(win, conn, apks):
    do_installs(conn, apks)
    win.enable_done_button()


@click.command()
@click.option('-d', '--debug/--no-debug', default=False)
@click.option('-s', '--adb-server', type=str, default=CROSTINI_DEFAULT_ADB_SERVER, show_default=True)
@click.option('-p', '--adb-port', type=int, default=CROSTINI_DEFAULT_ADB_PORT, show_default=True)
@click.option('-k', '--authkey',
              type=click.File('rb'),
              default=lambda: '{}/.android/adbkey'.format(os.environ.get('HOME', None)),
              show_default='$HOME/.android/adbkey')
@click.argument('apk', type=click.Path(exists=True), nargs=-1)
def main(debug, adb_server, adb_port, authkey, apk):

    if debug:
        logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
        logger = logging.getLogger('apksideloader')
        logger.setLevel(logging.DEBUG)
        logger.debug("Debugging mode enabled")
    else:
        logging.basicConfig()

    win = MainWindow()

    conn = AdbConnection(server=adb_server, port=adb_port, signer=PythonRSASigner('', authkey.read()))

    apks = queue.Queue()
    for counter, pkg in enumerate(apk):
        apk = ApkStatus(pkg)
        win.add_apk(apk)
        apks.put(apk)

    win.show_all()

    worker_thread = threading.Thread(target=worker, daemon=True, args=(win, conn, apks)).start()

    Gtk.main()


if __name__ == '__main__':
    main()
