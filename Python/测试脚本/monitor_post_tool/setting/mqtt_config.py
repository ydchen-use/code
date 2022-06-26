# MQTT 配置信息

remote_device_path = "/home/kbdev/ids-diag/remote_program/monitor_post_tool/setting/cert/"
test_config_path = "/usr/lib/kbids/common/monitor_post_tool/setting/cert/"

# platform_type_list = ["Official", "Nantong"]

# 测试使用
platform_type_list = ["Test_50", "Test"]

num_to_platform_type = {
    "0": "Nantong",
    "1": "Official",
    "2": "Test",
    "3": "Test_50"
}

#
# mqtt_test_config = {
#     "SERVER_URL": "in.aiot.swiftsec.com.cn",
#     "SERVER_PORT": 8883,
#     "ACCOUNT": "kibo-swift-term",
#     "PASSWORD": "kiboterm@2020",
#     "MQTT_CA": test_config_path + "test/my_root_ca.pem",
#     "MQTT_CERT": test_config_path + "test/client.pem",
#     "MQTT_KEY": test_config_path + "test/client.key",
# }
#
# mqtt_test_50_config = {
#     "SERVER_URL": "192.168.20.50",
#     "SERVER_PORT": 8883,
#     "ACCOUNT": "kibo-swift-term",
#     "PASSWORD": "kiboterm@2020",
#     "MQTT_CA": test_config_path + "test/my_root_ca.pem",
#     "MQTT_CERT": test_config_path + "test/client.pem",
#     "MQTT_KEY": test_config_path + "test/client.key",
# }

mqtt_nantong_config = {
    "SERVER_URL": "platform.istt.org.cn",
    "SERVER_PORT": 8883,
    "ACCOUNT": "kibo-swift-term",
    "PASSWORD": "kiboterm@2020",
    "MQTT_CA": remote_device_path + "test/my_root_ca.pem",
    "MQTT_CERT": remote_device_path + "test/client.pem",
    "MQTT_KEY": remote_device_path + "test/client.key",
}

mqtt_official_config = {
    "SERVER_URL": "aiot.swiftsec.com.cn",
    "SERVER_PORT": 18883,
    "ACCOUNT": "kbids",
    "PASSWORD": "tzQ8^k.syc9)vXaST-iq!FM4bs8UrEW+",
    "MQTT_CA": remote_device_path + "official/my_root_ca.pem",
    "MQTT_CERT": remote_device_path + "official/client.pem",
    "MQTT_KEY": remote_device_path + "official/client.key",
}

# 测试使用
mqtt_test_50_config = {
    "SERVER_URL": "192.168.20.50",
    "SERVER_PORT": 8883,
    "ACCOUNT": "kibo-swift-term",
    "PASSWORD": "kiboterm@2020",
    "MQTT_CA": "cert/test/my_root_ca.pem",
    "MQTT_CERT": "cert/test/client.pem",
    "MQTT_KEY": "cert/test/client.key",
}

mqtt_test_config = {
    "SERVER_URL": "in.aiot.swiftsec.com.cn",
    "SERVER_PORT": 8883,
    "ACCOUNT": "kibo-swift-term",
    "PASSWORD": "kiboterm@2020",
    "MQTT_CA": "cert/test/my_root_ca.pem",
    "MQTT_CERT": "cert/test/client.pem",
    "MQTT_KEY": "cert/test/client.key",
}

platform_to_config = {
    "Official": mqtt_official_config,
    "Nantong": mqtt_nantong_config,
    "Test": mqtt_test_config,
    "Test_50": mqtt_test_50_config
}

# method name
method_names = {
    "reqRequireLog": {
        "methodName": "reqRequireLog",
        "requestId": "30c9e772-22b8-4446-8084-2e5bde7067f2",
        "payload": {"log_path": ""}},
    "reqRawCmd": {
        "methodName": "reqRawCmd",
        "requestId": "nonce",
        "payload": {"auth": "{}", "cmd": "{}", "nonce": "nonce"}},
}

# mqtt prompt msg

mqtt_prompt_msg = {
    "mqtt_disconnected": [{"problem_type": "4", "message": "mqtt is not connected!", "status": -1}],
    "mqtt_timeout": [{"problem_type": "5", "message": "receive msg timeout", "status": -1}],
}
