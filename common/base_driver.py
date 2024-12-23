
from appium import webdriver
from common.all_path import configPath, appPath
import yaml
import os

from common.app_info import get_devices_version, get_app_name, get_app_launchable_activity, get_app_package_name

from common.appium_auto_server import open_appium


class BaseDriver:

    def __init__(self, device_info):
        self.device_info = device_info
        cmd = "start /b appium -a 127.0.0.1 -p {0} -bp {1}".format(self.device_info["server_port"],
                                                                   self.device_info["server_port"] + 1)
        open_appium(cmd, self.device_info["server_port"])

    def base_driver(self, automationName="appium"):
        fp = open(f"{configPath}//caps.yml", encoding='utf-8')
        # 平台名称、包名、Activity名称、超时时间、是否重置、server_ip、
        desired_caps = yaml.load(fp, Loader=yaml.FullLoader)

        # 设备名称
        desired_caps["deviceName"] = self.device_info['device']

        # 版本信息
        desired_caps["platform_version"] = get_devices_version(desired_caps["deviceName"])

        app_path = os.path.join(appPath, get_app_name(appPath))
        desired_caps['app'] = app_path

        desired_caps['appPackage'] = get_app_package_name()

        desired_caps['appActivity'] = get_app_launchable_activity()

        # udid
        desired_caps["udid"] = self.device_info['device']
        # 系统端口号
        desired_caps["systemPort"] = self.device_info["system_port"]

        if automationName != "appium":
            desired_caps["automationName"] = automationName

        driver = webdriver.Remote(f"http://127.0.0.1:{self.device_info['server_port']}/wd/hub",
                                  desired_capabilities=desired_caps)
        return driver
