import subprocess

def isConnectedToExternalDisplay():
    result = subprocess.run(['system_profiler', 'SPDisplaysDataType'], stdout=subprocess.PIPE)
    return b"Connection Type: DisplayPort" in result.stdout