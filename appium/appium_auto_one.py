import os
import subprocess
import random
import re
import time
import psutil
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from appium import webdriver
from selenium.webdriver.common.by import By

from auto_app_page import click_element, wait_element

adb_command = "adb shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey -p com.example.b12 --running-minutes 1 --throttle 1000 --act-whitelist-file /sdcard/awl.strings --uiautomatormix -v -v  --output-directory /sdcard/max-output"
adb_command2 = "adb shell am force-stop com.emanuelef.remote_capture"
adb_command3 = "adb shell am force-stop com.example.b12"
adb_kill = "adb kill-server"
adb_start = "adb start-server"
working_directory = r"D:\Software\leidian\LDPlayer9"
package_file = r"C:\Users\lenovo\Desktop\andronzy\package.yaml"
# 启动PCAPDroid会话
def start_pcapdroid_session(device_name):
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.device_name = '127.0.0.1:62025'
    options.platform_version = '12'
    options.app_activity = 'com.emanuelef.remote_capture.activities.MainActivity'
    options.app_package = 'com.emanuelef.remote_capture'
    options.no_reset = True
    options.dont_stop_app_on_reset = True  # 防止重置和关闭应用
    # 初始化 WebDriver
    return webdriver.Remote(command_executor='http://localhost:4723', options=options)
def appium_start():
    '''
    启动appium server
    :param host:
    :param port:
    :return:
    '''
    #指定bp端口号
    # bootstrap_port = str(port)
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



# 随机点击函数
def random_screen_click():
    screen_width = 1080  # 替换为设备实际屏幕宽度
    screen_height = 1920  # 替换为设备实际屏幕高度
    x = random.randint(100, screen_width - 100)
    y = random.randint(100, screen_height - 100)
    adb_command = f"adb shell input tap {x} {y}"
    os.system(adb_command)
    print(f"已点击坐标: ({x}, {y})")


# 获取设备上所有已安装的应用包名
def get_installed_apps():
    result = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages'], stdout=subprocess.PIPE)
    packages = result.stdout.decode('utf-8').splitlines()
    package_names = [pkg.split(":")[1] for pkg in packages]
    return package_names


# 获取应用的主Activity
def get_main_activity(package_name):
    result = subprocess.run(['adb', 'shell', 'cmd', 'package', 'resolve-activity', '--brief', package_name],
                            stdout=subprocess.PIPE)
    activity_info = result.stdout.decode('utf-8').strip()
    match = re.search(r'([a-zA-Z0-9\.]+)/([a-zA-Z0-9\./]+)', activity_info)
    return f"{match.group(1)}/{match.group(2)}" if match else None


# 获取PCAPDroid任务ID
def get_pcapdroid_task_id():
    result = subprocess.run(['adb', 'shell', 'dumpsys', 'activity', 'activities'], stdout=subprocess.PIPE)
    activities_info = result.stdout.decode('utf-8')
    for line in activities_info.splitlines():
        if 'com.emanuelef.remote_capture' in line and 'taskId' in line:
            match = re.search(r'taskId=(\d+)', line)
            return match.group(1) if match else None
    return None


# 切换回PCAPDroid应用，通过任务ID恢复
def switch_back_to_pcapdroid():
    task_id = get_pcapdroid_task_id()
    if task_id:
        os.system(f"adb shell am move-task-to-front {task_id}")
        print(f"已将PCAPDroid任务恢复到前台，任务ID: {task_id}")
    else:
        print("未找到PCAPDroid任务，无法恢复")


# 返回到主页
def return_to_home(driver):
    driver.press_keycode(3)  # 按下Home键
    print("返回到主页")


# 遍历所有应用并打开每个应用，跳过PCAPDroid和io.appium.settings，处理异常
def open_apps_and_random_clicks(driver, app_list, wait_time):
    count = 0  # 计数器，用于每打开4个应用后唤醒一次PCAPDroid
    for app in app_list:
        if app in ['com.emanuelef.remote_capture', 'io.appium.settings']:
            print(f"跳过应用：{app}")
            continue

        main_activity = get_main_activity(app)
        if main_activity:
            try:
                print(f"正在打开应用：{app}，主Activity：{main_activity}")

                # 强制停止应用
                os.system(f"adb shell am force-stop {app}")
                time.sleep(wait_time)  # 确保应用停止

                # 打开应用
                result = subprocess.run(['adb', 'shell', 'am', 'start', '-n', main_activity],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(wait_time)  # 等待应用启动

                # 检查输出中的警告
                output = result.stderr.decode('utf-8')
                if "Warning: Activity not started" in output:
                    print(f"警告: 应用 {app} 已在运行，跳过该应用")
                    continue

                # 随机点击
                random_screen_click()

                # 退出应用进程
                os.system(f"adb shell am force-stop {app}")
                print(f"已强制停止应用：{app}")

                count += 1  # 计数器加1
                if count >= 4:  # 每打开4个应用唤醒一次PCAPDroid
                    switch_back_to_pcapdroid()
                    return_to_home(driver)
                    count = 0  # 重置计数器

            except Exception as e:
                print(f"无法打开应用 {app} 或在操作时出错，错误：{e}，跳过该应用")
                continue
        else:
            print(f"未找到主Activity：{app}")


# 执行步骤1和步骤2
def perform_step_1_and_2(driver, wait_time):
    time.sleep(wait_time)
    # driver.find_element(By.ID, "com.emanuelef.remote_capture:id/action_start").click()
    # click_element(driver, (AppiumBy.XPATH, '//android.widget.TextView[@content-desc="启动"]'), '启动按钮')
    # 第一个点击坐标
    x1 = (872, 56)
    y1 = (984, 984)
    # 生成并执行 adb 命令
    adb_command = f"adb shell input tap {x1[0]} {x1[1]}"
    os.system(adb_command)

    time.sleep(wait_time)

    # 设定点击范围的坐标
    x2 = (779, 189)
    y2 = (840, 227)
    # 生成并执行 adb 命令
    adb_command = f"adb shell input tap {x2[0]} {x2[1]}"
    os.system(adb_command)
    # print(f"已点击坐标: ({x}, {y})")
    # click_element(driver, (AppiumBy.XPATH, '//android.widget.TextView[@text="连接"]'), "查看连接")
    # click_element(driver, (AppiumBy.XPATH, '//android.widget.TextView[@text="连接"]'), "查看连接")
    # [779, 189][840, 227]
    time.sleep(wait_time)


def operation_steps(waite_time):
    for app in app_name:
        app_package = app['appPackage']  # 获取传入的app对象中的appPackage
        # time.sleep(5)
        # 使用appPackage替换命令中的特定包名
        adb_command = f"adb shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey -p {app_package} --running-minutes 1 --throttle 1000 --act-whitelist-file /sdcard/awl.strings --uiautomatormix -v -v --output-directory /sdcard/max-output"
        adb_command3 = f"adb shell am force-stop {app_package}"
        adb_command2 = "adb shell am force-stop com.emanuelef.remote_capture"
        # 调用执行命令的函数
        execute_maxim(adb_command, adb_command2, adb_command3)

def execute_maxim(adb_command,adb_command2, adb_command3):
    stop_appium(4723)  # 先判断端口是否被占用，如果被占用则关闭该端口号
    kill_uiautomator_process()
    process_to_kill = "Appium Server GUI.exe"
    kill_process_by_name(process_to_kill)
    task_to_close = "Appium Server GUI.exe"
    close_task_by_name(task_to_close)
    try:
        subprocess.run(adb_command, shell=True, cwd=working_directory, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    try:
        subprocess.run(adb_command3, shell=True, cwd=working_directory, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    appium_start()
    devices_name = '127.0.0.1:62025'
    driver = start_pcapdroid_session(devices_name)
    perform_step_3_and_4(driver, 2)
    time.sleep(10)

# 执行步骤3和步骤4
def perform_step_3_and_4(driver, wait_time):
    # time.sleep(wait_time)
    # click_element(driver, (AppiumBy.XPATH, '//android.widget.TextView[@content-desc="保存到文件"]'), "点击保存到文件")
    # time.sleep(wait_time)
    x1 = (984,56)
    y1 = (1080,152)
    # 生成并执行 adb 命令
    adb_command = f"adb shell input tap {x1[0]} {x1[1]}"
    os.system(adb_command)
    time.sleep(5)
    # 第七步：修改文件名称
    file_name = wait_element(driver,
                             (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="android:id/title"]')).text
    print(f'获取当前默认文件名称: {file_name}')
    click_element(driver, (AppiumBy.XPATH, '//android.widget.Button[@resource-id="android:id/button1"]'), "点击保存")
    time.sleep(5)
    os.system(f"adb pull /sdcard/{file_name} C:/Users/lenovo/Desktop/android_appium/TEST/{file_name}")
    time.sleep(wait_time)


# 主逻辑执行
if __name__ == "__main__":
    stop_appium(4723)
    appium_start()
    app_name = [
        {'appName': '知乎', 'appPackage': 'com.zhihu.android',
         'appActivity': 'com.zhihu.android.app.ui.activity.LauncherActivity'},
        {'appName': '抖音', 'appPackage': 'com.ss.android.ugc.aweme',
         'appActivity': 'com.ss.android.ugc.aweme.main.MainActivity'},
        {'appName': '微信', 'appPackage': 'com.tencent.mm', 'appActivity': 'com.tencent.mm.ui.LauncherUI'},
        {'appName': '小红书', 'appPackage': 'com.xingin.xhs', 'appActivity': 'com.xingin.xhs.activity.SplashActivity'},
        {'appName': '微信', 'appPackage': 'com.tencent.mm', 'appActivity': 'com.tencent.mm.ui.LauncherUI'},
        {'appName': '抖音', 'appPackage': 'com.ss.android.ugc.aweme',
         'appActivity': 'com.ss.android.ugc.aweme.main.MainActivity'},
        {'appName': 'QQ音乐HD', 'appPackage': 'com.tencent.qqmusicpad',
         'appActivity': 'ccom.tencent.qqmusicpad.activity.MainActivity'}]
    # 填写设备名称
    devices_name = '127.0.0.1:62025'
    driver = start_pcapdroid_session(devices_name)
    # 执行步骤1和步骤2
    perform_step_1_and_2(driver, 2)
    # 打开其他应用并执行
    operation_steps(2)
    driver = start_pcapdroid_session(devices_name)
    # 切换回PCAPDroid应用
    subprocess.run(['adb', '-s', devices_name, 'shell', 'am', 'start', '-n',
                    'com.emanuelef.remote_capture/com.emanuelef.remote_capture.activities.MainActivity'])
    # 执行步骤3和步骤4
    perform_step_3_and_4(driver, 2)


# !/user/bin/env python3
# -*- coding: utf-8 -*-
