# APK Sideloader for ChromeOS Devices

## Prerequisites
* [A device running ChromeOS 81 or later that supports Linux](https://www.chromium.org/chromium-os/chrome-os-systems-supporting-linux) (Developer Mode is *not* required)


### Tested Devices:
* Pixel Slate

## First-time Installation
* [Enable Linux support](https://support.google.com/chromebook/answer/9145439)
* Launch the Linux terminal and run `sudo apt update && sudo apt install adb`.
* Run the command `adb connect 100.115.92.2:5555`. You will be prompted to "Allow USB Debugging?". Check the box marked "Always allow from this computer". This will generate and save the encryption keys you will need to communicate with the Android environment. These keys can be found in `~/.android`.
* Optional: run `adb disconnect 100.115.92.2:5555` since you will not need it any longer.
* In the Linux settings in the ChromeOS settings app, go to "Develop Android app" and "enable ADB debugging" . (Note: after doing this, your system will report at the lock screen that it may contain software not verified by Google.)

## Installing from PyPI:
* Simply run `pip3 install apksideloader` in the Linux terminal

## Installing from source:
* Clone this git repository
* `python3 setup.py install --user`