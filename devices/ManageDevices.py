"""
@Author  : nzy

"""
import yaml
class ManageDevices:
    """
       1、重启adb服务。
       2、通过adb devices命令获取当前平台中,已连接的设备个数，和设备uuid.
       3、通过adb -P 5037 -s 设备uuid shell getprop ro.build.version.release获取每一个设备的版本号。
       4、将所有已连接设备的设备名称、设备版本号存储在一个列表当中。
       5、通过调用get_devices_info函数，即可获得4中的列表。
    """

    def __init__(self):
        self.__devices_info = []
        # 重启adb服务
        self.__run_command_and_get_stout("adb kill-server")
        self.__run_command_and_get_stout("adb start-server")

    def get_devices_info(self):
        """
        获取已连接设备的uuid,和版本号。
        :return: 所有已连接设备的uuid,和版本号。
        """
        self.__get_devices_uuid()
        print(self.__devices_info)
        self.__get_device_platform_vesion()
        return self.__devices_info

    def devices_pool(port=4723, system_port=8200):
        """
        设备启动参数管理池。含启动参数和对应的端口号
        :param port: appium服务的端口号。每一个设备对应一个。
        :param system_port: appium服务指定的本地端口，用来转发数据给安卓设备。每一个设备对应一个。
        :return: 所有已连接设备的启动参数和appium端口号。
        """
        desired_template = __get_yaml_data()
        devs_pool = []
        # 获取当前连接的所有设备信息
        m = ManageDevices()
        all_devices_info = m.get_devices_info()
        # 补充每一个设备的启动信息，以及配置对应的appium server端口号
        if all_devices_info:
            for dev_info in all_devices_info:
                dev_info.update(desired_template)
                dev_info["systemPort"] = system_port
                new_dict = {
                    "caps": dev_info,
                    "port": port
                }
                devs_pool.append(new_dict)
                port += 4
                system_port += 4
        return devs_pool

        def devices_pool(port=4723, system_port=8200):
            """
            设备启动参数管理池。含启动参数和对应的端口号
            :param port: appium服务的端口号。每一个设备对应一个。
            :param system_port: appium服务指定的本地端口，用来转发数据给安卓设备。每一个设备对应一个。
            :return: 所有已连接设备的启动参数和appium端口号。
            """
            desired_template = __get_yaml_data()
            devs_pool = []
            # 获取当前连接的所有设备信息
            m = ManageDevices()
            all_devices_info = m.get_devices_info()
            # 补充每一个设备的启动信息，以及配置对应的appium server端口号
            if all_devices_info:
                for dev_info in all_devices_info:
                    dev_info.update(desired_template)
                    dev_info["systemPort"] = system_port
                    new_dict = {
                        "caps": dev_info,
                        "port": port
                    }
                    devs_pool.append(new_dict)
                    port += 4
                    system_port += 4
            return devs_pool
