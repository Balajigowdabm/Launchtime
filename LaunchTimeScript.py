import subprocess
import time
import os

launch_time_list = []
wb_greps = "Game Load Time Log:"
current_time = int(time.time())

def install_app(package_name, apk_file_path):
    subprocess.run("adb logcat -c", shell=True)
    subprocess.run(['adb', 'install', '-r', apk_file_path])#installs an APK file on a connected Android device, and the -r option ensures that the app is reinstalled if it already exists without losing the existing data.

def launch_app(package_name):
    subprocess.run(["adb", "shell", "am", "start", "-n", package_name + "/in.playsimple.AppActivity"])
    global current_time
    current_time = int(time.time())
    print("current time:")
    print(current_time)

def grant_notification_permission(package_name):
    subprocess.run(["adb", "shell", "pm", "grant", package_name, "android.permission.POST_NOTIFICATIONS"])

def check_log_for_game_load_time():
    while True:
        # Check if the log message is available
        log_output = subprocess.check_output("adb logcat -d", shell=True)
        if wb_greps.encode() in log_output:
            break
        time.sleep(1)  # Adjust the delay as per your requirement
    
    time.sleep(1)  # Adjust the delay as per your requirement
    subprocess.call("adb logcat -d | grep '" + wb_greps + "'", shell=True)
    displayed_log = subprocess.check_output("adb logcat -d | grep -m1 '" + wb_greps + "'", shell=True)
    displayed_log = str(displayed_log).split('Game Load Time Log:')[1].split(',')[0]
    displayed_log = displayed_log.replace("\\n'", "")
    displayed_log_seconds = int(displayed_log) / 1000  # Convert milliseconds to seconds
    wb_launchtime = (displayed_log_seconds - current_time)
    print("launch time:", wb_launchtime)
    launch_time_list.append(wb_launchtime)
    print("Launch time list:", launch_time_list)

    # Calculate the average launch time
    average_launch_time = sum(launch_time_list) / len(launch_time_list)
    print("Average Launch Time:", average_launch_time)

def uninstall_app(package_name):
    subprocess.run(['adb', 'uninstall', package_name])

def get_apk_file_path():
    return input("Enter the APK file path: ")

def get_num_loops():
    try:
        return int(input("Enter the number of loops: "))
    except ValueError:
        print("Invalid input. Using default value (5 loops).")
        return 5

def main():
    app_package_name = 'in.playsimple.wordbingo'  # Replace with the package name of the app you want to install/reinstall

    num_loops = get_num_loops()
    apk_file_path = get_apk_file_path()

    for i in range(num_loops):
        print(f"Loop {i + 1}")

        print("Installing the app...")
        install_app(app_package_name, apk_file_path)
        time.sleep(1)

        print("Launching the app...")
        launch_app(app_package_name)
        time.sleep(1)

        print("Granting notification permission...")
        grant_notification_permission(app_package_name)
        time.sleep(1)

        print("Checking log for game load time...")
        check_log_for_game_load_time()

        print("Uninstalling the app...")
        uninstall_app(app_package_name)

        print()

if __name__ == "__main__":
    main()
