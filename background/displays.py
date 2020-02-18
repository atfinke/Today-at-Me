import subprocess

from components import applescript, logging
from configuration import config

logger = logging.setup_logger(
    'displays', config.DISPLAYS_LOGGING_PATH)

__was_connected_to_external_display = None


def _is_connected_to_external_display():
    logger.info('_is_connected_to_external_display: called')
    result = subprocess.run(
        ['system_profiler', 'SPDisplaysDataType'], stdout=subprocess.PIPE)
    is_connected_to_external_display = b"Connection Type: DisplayPort" in result.stdout
    logger.info('_is_connected_to_external_display: result: {}'.format(is_connected_to_external_display))
    return is_connected_to_external_display


def configure_for_connected_display():
    logger.info('configure_for_connected_display: called')

    global __was_connected_to_external_display
    is_connected_to_external_display = _is_connected_to_external_display()
    if __was_connected_to_external_display == is_connected_to_external_display:
        logger.info('configure_for_connected_display: same state')
        return
    else:
        logger.info('configure_for_connected_display: new state')
        __was_connected_to_external_display = is_connected_to_external_display

    if is_connected_to_external_display:
        script = '''
        tell application "time.app" to quit
        {}
        {}
        tell application "System Preferences" to quit
        '''.format(__system_events_general_script(is_connected_to_external_display=True), __system_events_display_sound_output_script())
        applescript.run_sync(script)
    else:
        script = '''
        {}
        tell application "System Preferences" to quit
        delay 0.2
        set volume output volume 0
        tell application "time.app" to activate
        '''.format(__system_events_general_script(is_connected_to_external_display=False))
        applescript.run_sync(script)
    logger.info('configure_for_connected_display: updated system')


# Script Builders

def __open_pane(id, name):
    return '''
    tell application "System Preferences"
        activate
        set the current pane to pane id "{}"
        try
            repeat until window "{}" exists
                delay 0.1
            end repeat
            delay 0.25
        on error error_message
            get error_message
        end try
    end tell
    '''.format(id, name)


def __system_events_general_script(is_connected_to_external_display):
    hide_menu_bar = 'true' if is_connected_to_external_display else 'false'
    hide_dock = 'false' if is_connected_to_external_display else 'true'
    return '''
    {}
    tell application "System Events"
        set theCheckbox to checkbox "Automatically hide and show the menu bar" of window "General" of application process "System Preferences" of application "System Events"
        tell theCheckbox
            set checkboxValue to value of theCheckbox as boolean
            if checkboxValue is {} then click theCheckbox
        end tell
        set the autohide of the dock preferences to {}
    end tell
    '''.format(__open_pane('com.apple.preference.general', 'General'), hide_menu_bar, hide_dock)


def __system_events_display_sound_output_script():
    return '''
    {}
    tell application "System Events" to tell application process "System Preferences"
        set theRows to rows of table 1 of scroll area 1 of tab group 1 of window "Sound"
        set theLastRowIndex to (count of items in theRows)
        
        set theLastRow to item theLastRowIndex of theRows
        set selected of theLastRow to true
    end tell
    '''.format(__open_pane('com.apple.preference.sound', 'Sound'))
