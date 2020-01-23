from subprocess import Popen

def run_sync(script):
    Popen(['osascript', '-e', script])