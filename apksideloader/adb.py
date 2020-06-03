import logging
import os
import random
import string

from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.exceptions import DeviceAuthError, TcpTimeoutException

logger = logging.getLogger(__name__)

CROSTINI_DEFAULT_ADB_SERVER = '100.115.92.2'
CROSTINI_DEFAULT_ADB_PORT = 5555


class AdbConnectionError(ConnectionError):
    pass


class AdbConnection:
    device = None
    TMP_PATH = '/data/local/tmp'
    server = None
    port = 0
    signer = None
    connected = False
    apks = None

    def __init__(self, server, port, signer=None):
        self.server = server
        self.port = port
        self.signer = signer

    def connect(self):
        self.device = AdbDeviceTcp(self.server, self.port)

        try:
            if self.signer:
                self.device.connect(rsa_keys=[self.signer], timeout_s=10.0)
            else:
                self.device.connect(timeout_s=10.0)

        except OSError as e:
            logger.error("OSError: {}".format(e))
            raise AdbConnectionError(e)

        except (DeviceAuthError, TcpTimeoutException) as e:
            logger.error("Could not authenticate to the ADB server: {}".format(e))
            raise AdbConnectionError(e)

    def install_apk(self, apk):
        apk.progress.set_fraction(0.0)
        apk.info('Copying...')

        # Copy the APK to the target
        dst_filename = ''.join(random.choice(string.ascii_lowercase) for i in range(16)) + '.apk'

        dst_path = os.path.join(AdbConnection.TMP_PATH, dst_filename)
        logger.debug("dst_path: {}".format(dst_path))
        self.device.push(apk.src_path, dst_path, total_timeout_s=10.0, progress_callback=apk.update_progress)
        apk.progress.set_fraction(1.0)

        apk.info('Installing...')

        # Install the APK on the target
        try:
            output = self.device.shell('pm install -r {}'.format(dst_path))
        except Exception as e:
            logger.error("Installation failed: {}".format(e))
            raise

        if output != "Success\n":
            apk.fail(output.split('\n')[0])

        else:
            apk.succeed()