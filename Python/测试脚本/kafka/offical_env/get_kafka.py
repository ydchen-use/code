import json

from kafka import KafkaConsumer


consumer = KafkaConsumer(# 'ids_asset_task_detail_device_req',# ids_alert_pkg_req
                         # 'ids_access_point_req',
                         "ids_alert_pkg_req",
                         sasl_mechanism="PLAIN",
                         security_protocol='SASL_SSL',
                         sasl_plain_username='consumer',
                         sasl_plain_password='cons-sec@Gd~CTrH]-sV[g]h',
                         ssl_check_hostname=False,
                         ssl_cafile='CARoot.pem',
                         ssl_certfile='certificate.pem',
                         ssl_keyfile='key.pem',
                         bootstrap_servers=['k1.swiftsec.com.cn:9092','k2.swiftsec.com.cn:9092','k3.swiftsec.com.cn:9092'],
                         # bootstrap_servers=['192.168.20.50:9092'],
                         # auto_offset_reset='earliest',
                         api_version=(1, 1, 1)
                         )
for msg in consumer:
    if "KIBOVSIPSUGZ" in str(msg.value):
        print(str(msg.value))
