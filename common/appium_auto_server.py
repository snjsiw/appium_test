import subprocess
import socket
from common.all_path import logPath
from common.app_info import exec_cmd


def open_appium(cmd, port):
    """
    function ： 命令启动appium server
    :param cmd: appium server 启动命令
    :param port: appium server 启动端口
    :return: None
    """
    release_port(port)
    subprocess.Popen(cmd, shell=True, stdout=open(logPath+"/"+str(port)+'.log', "a"), stderr=subprocess.STDOUT)


def close_appium():
    """
    function: 关闭appium 服务器
    :return: None
    """
    cmd = "taskkill /f /im node.exe"
    subprocess.Popen(cmd, shell=True)


def check_port(host: str, port: int):
    """
    function: 检测端口是否被占用，如果sk.connect连接成功, 表示端口已经被占用，如果连接失败，则表示端口未被占用
    :param host: 主机地址：'127.0.0.1'
    :param port: 端口： 4723
    :return:
    """
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sk.connect((host, port))
        sk.shutdown(2)
    except OSError:
        return True
    else:
        return False


def release_port(port):
    """
    :param port: 需要释放的端口
    :return: 返回True
    """
    cmd = "netstat -ano| findstr {}".format(port)
    result = exec_cmd(cmd)
    if "LISTENING" and str(port) in result:
        pid = result.strip().split(" ")[-1]
        cmd = "taskkill -f -pid {}".format(int(pid))
        exec_cmd(cmd)
        return True
    else:
        return True
