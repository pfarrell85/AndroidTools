# AndroidTools

## Advanced Adb

This tool allows you to easily manage multiple Android devices connected to your
computer over adb.

### Commands

Show all adb devices:
aadb devices

Access the first Android device in the list:
aadb 0 shell

Access the second Android device in the list:
aadb 1 shell

Reboot all Android devices:
aadb shell reboot

Run a command over all Android devices in the list:
aadb shell "ls"
