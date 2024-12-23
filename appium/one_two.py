# !/user/bin/env python3
# -*- coding: utf-8 -*-
import time
import random
import os
import psutil

import subprocess
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from analysis_pcap import PCAPAnalyzer
from auto_app_page import send_element, click_element, wait_element

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

destination_dir = "C:/Users/lenovo/Desktop/android_appium/TEST"
# def start_pcapdroid_session(device_name):
#     options = UiAutomator2Options()
#     options.platform_name = 'Android'
#     options.device_name = '127.0.0.1:8011'
#     # options.platform_version = '12'
#     options.app_activity = 'com.emanuelef.remote_capture.activities.MainActivity'
#     options.app_package = 'com.emanuelef.remote_capture'
#     options.no_reset = True
#     options.dont_stop_app_on_reset = True  # 防止重置和关闭应用
#
#     # 初始化 WebDriver
#     return webdriver.Remote(command_executor='http://localhost:4723', options=options)
# 随机操作页面方法

def rename_file(file_name, destination_dir, new_extension=".pcap"):
    """
    只负责重命名本地文件为指定后缀。

    参数:
    - file_name (str): 文件名，可能不包含后缀。
    - destination_dir (str): 文件所在的本地路径。
    - new_extension (str): 需要添加的后缀，默认为 ".pcap"。
    """
    # 使用 os.path.join 确保路径正确
    original_path = os.path.join(destination_dir, file_name)

    # 如果文件不存在，输出错误提示
    if not os.path.exists(original_path):
        print(f"找不到文件: {original_path}，请确认文件是否已成功拉取到本地。")
        return

    # 检查文件是否已有指定后缀
    if not original_path.endswith(new_extension):
        new_path = os.path.join(destination_dir, f"{file_name}{new_extension}")
        try:
            os.rename(original_path, new_path)
            print(f"文件已成功重命名为: {new_path}")
        except Exception as e:
            print(f"文件重命名失败: {e}")
    else:
        print(f"文件已正确命名为: {original_path}")


def random_click(driver):
    # 获取屏幕的宽高
    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']
    # 生成随机的点击坐标
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    # 执行点击操作
    os.system(f"adb shell input tap {x} {y}")


# 指定一个应用并打开，然后随机操作
def open_app_and_random_clicks(app_name):
    # 强制停止应用
    os.system(f"adb shell am force-stop {app_name['appPackage']}")
    time.sleep(2)  # 等待应用停止

    print(f"正在启动应用：{app_name['appPackage']}，主活动：{app_name['appActivity']}")
    result = subprocess.run(['adb', 'shell', 'am', 'start', '-n', f"{app_name['appPackage']}/{app_name['appActivity']}"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)  # 等待应用加载

    # 检查启动结果
    if result.returncode != 0:
        print(f"启动应用失败，错误信息：{result.stderr.decode('utf-8')}")
        return
    # 随机点击
    for _ in range(10):  # 随机点击三次

        time.sleep(2)  # 等待一段时间再进行下一次点击     random_click(driver)

    # 强制停止应用
    os.system(f"adb shell am force-stop {app_name['appPackage']}")
    print(f"已强制停止应用：{app_name['appName']}")

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
def operation_steps(driver,waite_time):
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
        time.sleep(waite_time)

        # 第五步:找到应用并点击
        click_element(driver, (
        AppiumBy.XPATH, '(//android.widget.ImageView[@resource-id="com.emanuelef.remote_capture:id/app_icon"])[1]'),
                      f"{app['appName']}")
        time.sleep(waite_time)

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
        adb_command = f"adb shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey -p {app_package} --running-minutes 1 --throttle 1000 --act-whitelist-file /sdcard/awl.strings --uiautomatormix -v -v --output-directory /sdcard/max-output"
        adb_command3 = f"adb shell am force-stop {app_package}"
        adb_command2 = "adb shell am force-stop com.emanuelef.remote_capture"

        # 调用执行命令的函数
        execute_maxim(adb_command, adb_command2, adb_command3)
        # # 第九步：打开目标应用并执行随机点击
        # open_app_and_random_clicks(app)
        # time.sleep(waite_time)
        #
        # # 第十步：停止应用
        # click_element(driver, (AppiumBy.XPATH, '//android.widget.TextView[@content-desc="停止"]'), '停止')
        # time.sleep(waite_time)
        #
        # # 第十一步：停止应用后确认页面弹窗
        # click_element(driver, (AppiumBy.XPATH, '//android.widget.Button[@resource-id="android:id/button3"]'), '确认')
        # time.sleep(waite_time)
        try:
            subprocess.run(adb_command2, shell=True, cwd=working_directory, check=True)
            print("Command executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
        # 第十二步：保存PCAP到本地
        print(new_file_name)
        os.system(f"adb pull /sdcard/{new_file_name} C:/Users/lenovo/Desktop/android_appium/TEST/{new_file_name}")

        # rename_file(file_name, destination_dir)
        time.sleep(5)  # 等待应用停止
    # 连接数据库并创建表
        analyzer.connect_to_db()
        analyzer.create_table()

        # 立即分析刚刚下载的最新的 PCAP 文件
        analyzer.analyze_pcap()

        # 关闭数据库连接
        analyzer.close_db_connection()
        # driver = start_pcapdroid_session("127.0.0.1:62025")
    driver.quit()  # 关闭 WebDriver
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
    time.sleep(3)
    devices_name = '127.0.0.1:62025'
    driver = start_pcapdroid_session(devices_name)
    x2 = (779, 189)
    y2 = (840, 227)
    # 生成并执行 adb 命令
    adb_command = f"adb shell input tap {x2[0]} {x2[1]}"
    os.system(adb_command)
    time.sleep(30)
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
    time.sleep(2)


if __name__ == '__main__':
    #填写设备名称
    stop_appium(4723)
    appium_start()
    # 需要操作的应用名
    app_name = [
        {'appName': '抖音', 'appPackage': 'com.ss.android.ugc.aweme',
         'appActivity': 'com.ss.android.ugc.aweme.main.MainActivity'},
        {'appName': '小红书', 'appPackage': 'com.xingin.xhs', 'appActivity': 'com.xingin.xhs.activity.SplashActivity'},
        {'appName': '微信', 'appPackage': 'com.tencent.mm', 'appActivity': 'com.tencent.mm.ui.LauncherUI'},
        {'appName': '抖音', 'appPackage': 'com.ss.android.ugc.aweme',
         'appActivity': 'com.ss.android.ugc.aweme.main.MainActivity'},
        {'appName': 'QQ音乐HD', 'appPackage': 'com.tencent.qqmusicpad',
         'appActivity': 'ccom.tencent.qqmusicpad.activity.MainActivity'}]
    devices_name = '127.0.0.1:62025'
    driver = start_pcapdroid_session(devices_name)
    # 执行操作步骤
    operation_steps(driver,2)



