import subprocess


def is_screen_locked():
    process_name = 'LogonUI.exe'
    call_all = 'TASKLIST'
    output_all = subprocess.check_output(call_all)
    output_string_all = str(output_all)
    return process_name in output_string_all