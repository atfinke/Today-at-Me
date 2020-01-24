import subprocess
from components import applescript, launch_app

__was_connected_to_external_display = None

def _is_connected_to_external_display():
    result = subprocess.run(['system_profiler', 'SPDisplaysDataType'], stdout=subprocess.PIPE)
    return b"Connection Type: DisplayPort" in result.stdout

def configure_for_connected_display():
    global __was_connected_to_external_display
    is_connected_to_external_display = _is_connected_to_external_display()
    if __was_connected_to_external_display == is_connected_to_external_display:
        return
    else:
        __was_connected_to_external_display = is_connected_to_external_display

    if is_connected_to_external_display:
        script = '''
        tell application "time.app" to quit
        {}
        {}
        tell application "System Preferences" to quit
        '''.format(__open_system_preferences_script(), __system_events_script(is_connected_to_external_display=True))
        applescript.run_sync(script)
    else:
        script = '''
        {}
        {}
        tell application "System Preferences" to quit
        delay 0.2
        tell application "time.app" to activate
        '''.format(__open_system_preferences_script(), __system_events_script(is_connected_to_external_display=False))
        applescript.run_sync(script)


# Script Builders

def __open_system_preferences_script():
    return '''
    tell application "System Preferences"
        activate
        set the current pane to pane id "com.apple.preference.general"
        try
            repeat until window "General" exists
                delay 0.1
            end repeat
            delay 0.25
        on error error_message
            get error_message
        end try
    end tell
    '''

def __system_events_script(is_connected_to_external_display):
    opposite_of_hide_menu_bar = 'true' if is_connected_to_external_display else 'false'
    hide_dock = 'false' if is_connected_to_external_display else 'true'
    return '''
    tell application "System Events"
        set theCheckbox to checkbox "Automatically hide and show the menu bar" of window "General" of application process "System Preferences" of application "System Events"
        tell theCheckbox
            set checkboxValue to value of theCheckbox as boolean
            if checkboxValue is {} then click theCheckbox
        end tell
        set the autohide of the dock preferences to {}
    end tell
    '''.format(opposite_of_hide_menu_bar, hide_dock)