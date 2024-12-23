from appium.options.android import UiAutomator2Options
from appium import webdriver
import threading
import queue
import time
import random
import os
import psutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from analysis_pcap import PCAPAnalyzerdef android_driver(device: dict, info: dict):
    desired_caps = {
        "appium:appWaitDuration": 60000,
        "skipServerInstallation": True,
        "skipDeviceInitialization": True,
        "appium:skipLogcatCapture": True,
        "appium:disableSuppressAccessibilityService": True,
        "platformName": "Android",
        "appium:automationName": "uiautomator2",
        "appium:newCommandTimeout": 0,
        "autoGrantPermissions": True,
        "appium:adbExecTimeout": 120000,
        "appium:noReset": True,
        "appium:uiautomator2ServerLaunchTimeout": 120000,
        "appium:udid": device.get("appium:udid"),
        "appium:systemPort": device.get("appium:systemPort"),
        "deviceName": device.get("device_name"),
        "appium:appPackage": info['appium:appPackage'],
        "appium:appActivity": info["appium:appActivity"]
    }
from auto_app_page import send_element, click_element, wait_element

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=UiAutomator2Options().load_capabilities(desired_caps),
    )
    driver.update_settings({'waitForIdleTimeout': 0})
    driver.update_settings({'allowInvisibleElements': True})
    driver.update_settings({'ignoreUnimportantViews': True})
    driver.update_settings({'enableMultiWindows': True})
    return driver
def android_driver2(device: dict, info: dict):
    desired_caps = {
        "appium:appWaitDuration": 60000,
        "skipServerInstallation": True,
        "skipDeviceInitialization": True,
        "appium:skipLogcatCapture": True,
        "appium:disableSuppressAccessibilityService": True,
        "platformName": "Android",
        "appium:automationName": "uiautomator2",
        "appium:newCommandTimeout": 0,
        "autoGrantPermissions": True,
        "appium:adbExecTimeout": 120000,
        "appium:noReset": True,
        "appium:uiautomator2ServerLaunchTimeout": 120000,
        "appium:udid": device.get("appium:udid"),
        "appium:systemPort": device.get("appium:systemPort"),
        "deviceName": device.get("device_name"),
        "appium:appPackage": info['appium:appPackage'],
        "appium:appActivity": info["appium:appActivity"]
    }
    driver = webdriver.Remote(
        "http://127.0.0.1:4725",
        options=UiAutomator2Options().load_capabilities(desired_caps),
    )
    driver.update_settings({'waitForIdleTimeout': 0})
    driver.update_settings({'allowInvisibleElements': True})
    driver.update_settings({'ignoreUnimportantViews': True})
    driver.update_settings({'enableMultiWindows': True})
    return driver
new_file_name={}


adb_command = "adb shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey -p com.example.b12 --running-minutes 1 --throttle 1000 --act-whitelist-file /sdcard/awl.strings --uiautomatormix -v -v  --output-directory /sdcard/max-output"
adb_command2 = "adb shell am force-stop com.emanuelef.remote_capture"
adb_command3 = "adb shell am force-stop com.example.b12"
adb_kill = "adb kill-server"
adb_start = "adb start-server"
working_directory = r"D:\Software\leidian\LDPlayer9"
package_file = r"C:\Users\lenovo\Desktop\andronzy\package.yaml"

# 数据库配置
db_config = {
    'host': "150.109.100.62",
    'user': "root",
    'password': "Zm.1575098153",
    'database': "mobile",
    'port': "3306"
}
def appium_start():
    '''
    启动appium server
    :param host:
    :param port:
    :return:
    '''
    #指定bp端口号
    #把在cmd弹窗输入的命令，直接写到这里
    # cmd = 'start /b appium -a ' + host+' -p '+str(port) +' -bp '+ str(bootstrap_port)
    #去掉 “/b”，即可以打开cmd弹窗运行
    # subprocess.Popen(f'appium', shell=True)
    # cmd = 'start  appium -a ' + host+' -p '+str(port) +' -bp '+ str(bootstrap_port)
    # 在命令行中启动Appium服务
    subprocess.Popen("appium", shell=True)
    print("Appium服务已启动。")
    # 打印输入的cmd命令，及时间
    # print("%s at %s " %(cmd,time.ctime()))

def close_task_by_name(task_name):
    try:
        # 使用taskkill命令关闭指定名称的任务
        os.system(f'taskkill /F /IM {task_name}')
        print(f"Successfully closed task: {task_name}")
    except Exception as e:
        print(f"Error closing task: {e}")


def kill_processes_on_ports(ports):
    """
    终止正在使用指定端口的进程。

    :param ports: 要终止进程的端口列表
    """
    for port in ports:
        try:
            # 使用 netstat 找到占用该端口的 PID
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True
            )

            # 查找输出中包含该端口的行
            for line in result.stdout.splitlines():
                if f":{port}" in line:
                    # 获取 PID
                    pid = line.split()[-1]
                    print(f"Killing process on port {port} with PID {pid}")
                    # 终止该进程
                    os.system(f"taskkill /PID {pid} /F")
                    break
        except Exception as e:
            print(f"Error while killing process on port {port}: {e}")
def kill_process_by_name(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            pid = process.info['pid']
            try:
                # 强制终止进程
                psutil.Process(pid).kill()
                print(f"Successfully killed process: {process_name} (PID: {pid})")
            except psutil.NoSuchProcess as e:
                print(f"Error killing process: {e}")

def kill_uiautomator_process():
    find_process_cmd = "adb shell ps | findstr uiautomator"
    process = subprocess.Popen(find_process_cmd, shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()

    if output:
        lines = output.decode().splitlines()
        for line in lines:
            if 'uiautomator' in line:
                pid = line.split()[1]  #
                # Command to kill the uiautomator process
                kill_process_cmd = f"adb shell kill {pid}"
                subprocess.run(kill_process_cmd, shell=True)
                print(f"Killed uiautomator process with PID: {pid}")
                print("5555555555555")
    else:
        print("No uiautomator process found.")
def stop_appium(post_num=4723):
    '''关闭appium服务'''
    subprocess.Popen("appium --kill", shell=True)
    pc = 'WIN'
    if pc.upper() =='WIN':
        p = os.popen(f'netstat  -aon|findstr {post_num}')
        p0 = p.read().strip()
        if p0 != '' and 'LISTENING' in p0:
            p1 = int(p0.split('LISTENING')[1].strip()[0:4])  # 获取进程号
            os.popen(f'taskkill /F /PID {p1}')  # 结束进程
            print('appium server已结束')
    elif pc.upper() == 'MAC':
        p = os.popen(f'lsof -i tcp:{post_num}')
        p0 = p.read()
        if p0.strip() != '':
            p1 = int(p0.split('\n')[1].split()[1])  # 获取进程号
            os.popen(f'kill {p1}')  # 结束进程
            print('appium server已结束')

# 目标目录和 DoH 解析器文件
pcap_directory = 'C:/Users/lenovo/Desktop/android_appium/TEST'
doh_resolver_file = 'C:/Users/lenovo/Desktop/android_appium/config/doh_resolver_ip_full.csv'

# 生成 PCAPAnalyzer 实例
analyzer = PCAPAnalyzer(db_config, pcap_directory, doh_resolver_file)

# 检查开关状态
def check_and_toggle_switch(driver):
    switch_state = driver.find_element(AppiumBy.XPATH, '//android.widget.Switch[@resource-id="com.emanuelef.remote_capture:id/app_filter_switch"]')
    if switch_state.get_attribute('checked') == 'false':  # 开关是关闭的
        print("开关已关闭，正在开启开关")
        click_element(driver, (AppiumBy.XPATH, '//android.widget.Switch[@resource-id="com.emanuelef.remote_capture:id/app_filter_switch"]'), '开启目标应用Switch')
        time.sleep(2)
    else:
        print("开关已开启，正在关闭开关")
        click_element(driver, (AppiumBy.XPATH, '//android.widget.Switch[@resource-id="com.emanuelef.remote_capture:id/app_filter_switch"]'), '关闭目标应用Switch')
        time.sleep(2)
        # 再次开启开关
        click_element(driver, (AppiumBy.XPATH, '//android.widget.Switch[@resource-id="com.emanuelef.remote_capture:id/app_filter_switch"]'), '开启目标应用Switch')
        time.sleep(2)

# 执行操作步骤
def operation_steps(device,app_name,driver,waite_time):
    for app in app_name:
        time.sleep(2)
        # 第一步:点击PCAP文件选项
        click_element(driver, (AppiumBy.XPATH,
                               '//android.widget.Spinner[@resource-id="com.emanuelef.remote_capture:id/dump_mode_spinner"]/android.widget.LinearLayout'),
                      'PCAP文件选项')
        time.sleep(waite_time)

        # 第二步:选择PCAP菜单选项
        click_element(driver, (AppiumBy.XPATH,
                               '//android.widget.ListView[@resource-id="com.emanuelef.remote_capture:id/select_dialog_listview"]/android.widget.LinearLayout[3]'),
                      'PCAP文件选项')
        time.sleep(waite_time)

        # 第三步:检查并切换目标应用Switch状态
        check_and_toggle_switch(driver)

        # 第四步输入需要搜索的应用
        send_element(driver, (AppiumBy.XPATH,
                              '//android.widget.AutoCompleteTextView[@resource-id="com.emanuelef.remote_capture:id/search_src_text"]'),
                     app['appName'], '搜索应用')
        time.sleep(5)

        # 第五步:找到应用并点击
        # click_element(driver, (
        # AppiumBy.XPATH, '(//android.widget.ImageView[@resource-id="com.emanuelef.remote_capture:id/app_icon"])[1]'),
        #               f"{app['appName']}")
        # time.sleep(5)
        x2 = (240, 292)
        y2 = (932, 330)
        # 生成并执行 adb 命令
        if device == device1:
            adb_command = f"adb -s 127.0.0.1:62025 shell input tap {x2[0]} {x2[1]}"
        if device == device2:
            adb_command = f"adb -s 127.0.0.1:62026 shell input tap {x2[0]} {x2[1]}"
        os.system(adb_command)
        # 第六步:点击启动按钮
        click_element(driver, (AppiumBy.XPATH, '//android.widget.TextView[@content-desc="启动"]'), '启动按钮')
        time.sleep(waite_time)

        # 第七步：修改文件名称
        file_name = wait_element(driver,
                                 (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="android:id/title"]')).text
        print(f'获取当前默认文件名称: {file_name}')
        new_file_name = file_name.replace("PCAPdroid", app['appName'])
        print(f'替换后的文件名称: {new_file_name}')
        click_element(driver, (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="android:id/title"]'))
        time.sleep(waite_time)
        wait_element(driver, (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="android:id/title"]')).clear()
        time.sleep(waite_time)
        send_element(driver, (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="android:id/title"]'),
                     new_file_name)
        time.sleep(waite_time)

        # 第八步点击保存
        click_element(driver, (AppiumBy.XPATH, '//android.widget.Button[@resource-id="android:id/button1"]'), '保存')
        time.sleep(waite_time)
        app_package = app['appPackage']  # 获取传入的app对象中的appPackage
        # time.sleep(5)
        # 使用appPackage替换命令中的特定包名

        if device == device1:
            adb_command = f"adb -s 127.0.0.1:62025 shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey -p {app_package} --running-minutes 1 --throttle 1000 --act-whitelist-file /sdcard/awl.strings --uiautomatormix -v -v --output-directory /sdcard/max-output"
            adb_command3 = f"adb -s 127.0.0.1:62025 shell am force-stop {app_package}"
            adb_command2 = f"adb -s 127.0.0.1:62025 shell am force-stop com.emanuelef.remote_capture"
        if device == device2:
            adb_command = f"adb -s 127.0.0.1:62026 shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey -p {app_package} --running-minutes 1 --throttle 1000 --act-whitelist-file /sdcard/awl.strings --uiautomatormix -v -v --output-directory /sdcard/max-output"
            adb_command3 = f"adb -s 127.0.0.1:62026 shell am force-stop {app_package}"
            adb_command2 = f"adb -s 127.0.0.1:62026 shell am force-stop com.emanuelef.remote_capture"
        # 调用执行命令的函数
        # execute_maxim(device,adb_command, adb_command2, adb_command3)

        # 第十二步：保存PCAP到本地
        print(new_file_name)


def run_adb_command(command):
    try:
        subprocess.run(command, shell=True, cwd=working_directory, check=True)
        print(f"Command '{command}' executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e}")


def execute_maxim(device, adb_command, adb_command2, adb_command3):
    stop_appium(4723)  # 先判断端口是否被占用，如果被占用则关闭该端口号
    kill_uiautomator_process()
    process_to_kill = "Appium Server GUI.exe"
    kill_process_by_name(process_to_kill)
    task_to_close = "Appium Server GUI.exe"
    close_task_by_name(task_to_close)

    adb_command1 = f"adb -s 127.0.0.1:62025 shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey -p com.ss.android.ugc.aweme --running-minutes 1 --throttle 1000 --act-whitelist-file /sdcard/awl.strings --uiautomatormix -v -v --output-directory /sdcard/max-output"
    adb_command3 = f"adb -s 127.0.0.1:62025 shell am force-stop com.ss.android.ugc.aweme"
    adb_command2 = f"adb -s 127.0.0.1:62025 shell am force-stop com.emanuelef.remote_capture"

    adb_command11 = f"adb -s 127.0.0.1:62026 shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey -p com.example.b12 --running-minutes 1 --throttle 1000 --act-whitelist-file /sdcard/awl.strings --uiautomatormix -v -v --output-directory /sdcard/max-output"
    adb_command33 = f"adb -s 127.0.0.1:62026 shell am force-stop com.example.b12"
    adb_command22 = f"adb -s 127.0.0.1:62026 shell am force-stop com.emanuelef.remote_capture"

    with ThreadPoolExecutor() as executor:
        futures = []

        # 提交第一个组的命令
        futures.append(executor.submit(run_adb_command, adb_command1))
        futures.append(executor.submit(run_adb_command, adb_command11))

        # 提交第二个组的命令
        futures.append(executor.submit(run_adb_command, adb_command3))
        futures.append(executor.submit(run_adb_command, adb_command33))

        # 等待所有命令执行完成
        for future in as_completed(futures):
            future.result()  # 这里调用 result() 会引发异常（如果有的话）


def re_start_appium():
    driver = android_driver2(device, info)
    x2 = (779, 189)
    y2 = (840, 227)
    # 生成并执行 adb 命令
    if device == device1:
        adb_command = f"adb -s 127.0.0.1:62025 shell input tap {x2[0]} {x2[1]}"
    if device == device2:
        adb_command = f"adb -s 127.0.0.1:62026 shell input tap {x2[0]} {x2[1]}"
    os.system(adb_command)
    time.sleep(10)
    x1 = (984, 56)
    y1 = (1080, 152)
    # 生成并执行 adb 命令
    if device == device1:
        adb_command = f"adb -s 127.0.0.1:62025 shell input tap {x1[0]} {x1[1]}"
    if device == device2:
        adb_command = f"adb -s 127.0.0.1:62026 shell input tap {x1[0]} {x1[1]}"
    os.system(adb_command)
    time.sleep(5)
    # 第七步：修改文件名称
    file_name = wait_element(driver,
                             (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="android:id/title"]')).text
    print(f'获取当前默认文件名称: {file_name}')
    click_element(driver, (AppiumBy.XPATH, '//android.widget.Button[@resource-id="android:id/button1"]'), "点击保存")
    time.sleep(5)
    if device == device1:
        adb_command = f"adb -s 127.0.0.1:62025 pull /sdcard/{file_name} C:/Users/lenovo/Desktop/android_appium/TEST/{file_name}"
    if device == device2:
        adb_command = f"adb -s 127.0.0.1:62026 pull /sdcard/{file_name} C:/Users/lenovo/Desktop/android_appium/TEST/{file_name}"
    os.system(adb_command)
    time.sleep(5)
    if device == device1:
        adb_command2 = f"adb -s 127.0.0.1:62025 shell am force-stop com.emanuelef.remote_capture"
    if device == device2:
        adb_command2 = f"adb -s 127.0.0.1:62026 shell am force-stop com.emanuelef.remote_capture"
    try:
        subprocess.run(adb_command2, shell=True, cwd=working_directory, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

    if device == device1:
        adb_command = f"adb -s 127.0.0.1:62025 pull /sdcard/{new_file_name} C:/Users/lenovo/Desktop/android_appium/TEST/{new_file_name}"
    if device == device2:
        adb_command = f"adb -s 127.0.0.1:62026 pull /sdcard/{new_file_name} C:/Users/lenovo/Desktop/android_appium/TEST/{new_file_name}"
    os.system(adb_command)
    # rename_file(file_name, destination_dir)
    time.sleep(5)  # 等待应用停止
    # 连接数据库并创建表
    analyzer.connect_to_db()
    analyzer.create_table()

    # 立即分析刚刚下载的最新的 PCAP 文件
    analyzer.analyze_pcap()

    # 关闭数据库连接
    analyzer.close_db_connection()


def run_test_on_device(device, info):
    driver = android_driver(device, info)
    if device == device1:
        operation_steps(device,app_name,driver, 2)
    if device == device2:
        operation_steps(device,app_name2, driver, 2)
    # 在这里写需要driver做的一些操作
    driver.quit()

if __name__ == "__main__":
    device1 = {
        "appium:udid": '127.0.0.1:62025',
        "device_name": '127.0.0.1:62025',
        "appium:systemPort": 8201,
    }
    device2 = {
        "appium:udid": '127.0.0.1:62026',
        "device_name": '127.0.0.1:62026',
        "appium:systemPort": 8202,
    }
    app_name = [
        {'appName': '抖音', 'appPackage': 'com.ss.android.ugc.aweme',
         'appActivity': 'com.ss.android.ugc.aweme.main.MainActivity'}]

    app_name2 = [
        {'appName': '王者体育', 'appPackage': 'com.example.b12',
         'appActivity': 'com.example.b12.MainActivity'}, ]

    appinfo = [{"appium:appPackage": "com.emanuelef.remote_capture", "appium:appActivity": "com.emanuelef.remote_capture.activities.MainActivity"}]
    devices = [device1, device2]
    ports_to_kill = [8201, 8202, 8203, 8204]
    kill_processes_on_ports(ports_to_kill)
    stop_appium(4723)  # 先判断端口是否被占用，如果被占用则关闭该端口号
    kill_uiautomator_process()
    process_to_kill = "Appium Server GUI.exe"
    kill_process_by_name(process_to_kill)
    task_to_close = "Appium Server GUI.exe"
    close_task_by_name(task_to_close)
    appium_start()
    threads = []
    for app in appinfo:
        for device in devices:
            t = threading.Thread(target=run_test_on_device, args=(device, app))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()
    execute_maxim(device, adb_command, adb_command2, adb_command3)
    device1 = {
        "appium:udid": '127.0.0.1:62025',
        "device_name": '127.0.0.1:62025',
        "appium:systemPort": 8203,
    }
    device2 = {
        "appium:udid": '127.0.0.1:62026',
        "device_name": '127.0.0.1:62026',
        "appium:systemPort": 8204,
    }

    appinfo = [{"appium:appPackage": "com.emanuelef.remote_capture",
                "appium:appActivity": "com.emanuelef.remote_capture.activities.MainActivity"}]
    devices = [device1, device2]
    ports_to_kill = [8201, 8202, 8203, 8204]
    kill_processes_on_ports(ports_to_kill)
    stop_appium(4723)  # 先判断端口是否被占用，如果被占用则关闭该端口号
    kill_uiautomator_process()
    process_to_kill = "Appium Server GUI.exe"
    kill_process_by_name(process_to_kill)
    task_to_close = "Appium Server GUI.exe"
    close_task_by_name(task_to_close)

    appium_start()
    time.sleep(2)
    threads = []
    info = {"appium:appPackage": "com.emanuelef.remote_capture",
            "appium:appActivity": "com.emanuelef.remote_capture.activities.MainActivity"}
    for app in appinfo:
        for device in devices:
            t = threading.Thread(target=re_start_appium(), args=(device, app))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

