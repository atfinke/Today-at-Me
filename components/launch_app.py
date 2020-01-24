from components import applescript

def launch(app_name):
    applescript.run_sync("tell application \"{}\" to activate".format(app_name))

def kill(app_name):
    script = '''
    tell application "{}"
        quit
    end tell
    '''.format(app_name)
    applescript.run_sync(script)