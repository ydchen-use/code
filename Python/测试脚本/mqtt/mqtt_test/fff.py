import threading
import time
import ssl
import json
import logging
import socket
import paho.mqtt.client as mqtt

import json
import copy


class Response:
    def __init__(self, status, data=None, message='success', page=None, rows=None, total=None):
        self.status = status
        self.message = message
        self.data = data if data is not None else {}
        self.page = page
        self.rows = rows
        self.total = total

    def __clean(self):
        if not self.page:
            del self.page

        if not self.rows:
            del self.rows

        if not self.total:
            del self.total

    def to_string(self):
        _ret_obj = copy.copy(self)
        _ret_obj.__clean()

        try:
            _response = json.dumps(_ret_obj.__dict__)
        except:
            _response = json.dumps({'status': -1, 'message': '系统异常，异常代码[-1]', 'data': {}})
        return _response

    def to_dict(self):
        _ret_obj = copy.copy(self)
        _ret_obj.__clean()

        return _ret_obj.__dict__


class PlatformClient(threading.Thread):
    """
    连接MQTT
    """
    # 平台响应等待超时时间
    MQTT_RSP_TIMEOUT = 30  # 单位：秒

    def __init__(self, request_worker):
        threading.Thread.__init__(self)

        self.cloud_rsp_topic = None
        self.request_worker = request_worker

        # 处理请求线程
        self.request_handle_thread = None

        # 平台响应
        self.cloud_rsp_msg = {}
        self.last_cloud_rsp_time = time.time()

        # 读取MQTT地址，端口， 账号， 密码
        self.server_url = "192.168.20.50"  # cf_def.get('Mqtt', 'server')
        self.server_port = 8883  # int(cf_def.get('Mqtt', 'port'))
        self.user = "kibo-swift-term"  # cf_def.get('Mqtt', 'user')
        self.password = "kiboterm@2020"  # cf_def.get('Mqtt', 'password')

        # 读取mqtt证书
        self.ca = "my_root_ca.pem"  # cf_def.get('Mqtt', 'ca')
        self.client_cert = "client.pem"  # cf_def.get('Mqtt', 'client_certificate')
        self.client_key = "client.key"  # cf_def.get('Mqtt', 'client_key')

        # 初始化mqtt client
        self.client_id = "934db8f509c343079a0d997ee329b358"  # self.__get_client_id__()
        self.device_id = "KIBOBUGEAVDD"  # self.__get_device_id__()
        self.__init_topics__()
        self.async_methods = ['reqFirmwareUpgrade']
        print("Begin to connect mqtt")
        self.mqtt_client = mqtt.Client(self.client_id)

        self.mqtt_client.tls_set(ca_certs=self.ca, certfile=self.client_cert, keyfile=self.client_key,
                                 cert_reqs=ssl.CERT_NONE)
        self.mqtt_client.username_pw_set(self.user, self.password)

        self.mqtt_client.on_connect = self.__on_connect__
        self.mqtt_client.on_disconnect = self.__on_disconnect__
        self.mqtt_client.on_message = self.__on_message__

        # self.mqtt_client.will_set(self.lwt_topic, json.dumps(self.__report_lwt__()), 0, False)

        self.mqtt_is_connected = False
        self.mqtt_run_flag = True

    def __on_message__(self, client, userdata, msg):
        try:
            # 异常保护，防止平台大量消息过来
            if time.time() - self.last_cloud_rsp_time < 1:
                return

            # 对方传过来的是bytes,必须先转成string，再用eval转成dict
            logging.debug("receive cloud msg : |{}|".format(str(msg.payload.decode('utf-8'))))
            # cloud_msg = json.loads(str(msg.payload))
            cloud_msg = json.loads(str(msg.payload.decode('utf-8')))

            if msg.topic == self.cloud_rsp_topic:
                # self.msg_list.pop(cloud_msg['requestId'])
                self.cloud_rsp_msg[cloud_msg['requestId']] = cloud_msg
                logging.debug("receive cloud rsp : {}".format(cloud_msg))
            elif msg.topic == self.cloud_req_topic:  # or msg.topic == self.cloud_broadcast_topic:
                logging.debug("receive cloud req: {}".format(cloud_msg))
                print(f"receive cloud req: {cloud_msg}")

                # start a thread to handle request
                # if self.request_handle_thread is not None:
                #     logging.warning('Last request still running')
                self.request_handle_thread = threading.Thread(target=self.__request_handler__, args=(cloud_msg,))
                self.request_handle_thread.start()


            else:
                logging.error('unknown topic: {}'.format(msg.topic))
        except Exception as e:
            logging.exception('handle mqtt msg failed')

    def __on_disconnect__(self, client, userdata, rc):
        self.mqtt_is_connected = False
        logging.warning("mqtt disconnected!")

    def __on_connect__(self, client, userdata, flags, rc):
        # flags是一个包含代理回复的标志的字典；
        # rc的值决定了连接成功或者不成功：0,1,2,3,4,5
        # 0    连接成功
        # 1    协议版本错误
        # 2    无效的客户端标识
        # 3    服务器无法使用
        # 4    错误的用户名或密码
        # 5    未经授权
        logging.info("platform connected with result code {}, client {}".format(rc, client))
        print("platform connected with result code {}, client {}".format(rc, client))

        if rc != 0:
            self.mqtt_is_connected = False
            return

        # 订阅topic
        _tp_list = [(self.cloud_req_topic, 1)]  # (self.cloud_rsp_topic, 1), (self.cloud_broadcast_topic, 1)
        _ret, _mid = client.subscribe(_tp_list)
        logging.info("platform topic [{}] subscribe result {}".format(_tp_list, _ret))
        print("platform topic [{}] subscribe result {}".format(_tp_list, _ret))
        if _ret != 0:
            self.mqtt_is_connected = False
            return

        self.mqtt_is_connected = True

    def __send_response_to_platform__(self, payload):
        # if len(json.dumps(payload)) <= 20000:
        if self.mqtt_is_connected:
            _rc, _mid = self.mqtt_client.publish(self.rsp_topic, json.dumps(payload), 1)
            logging.debug("response to platform - payload: {}, rc: {}".format(json.dumps(payload), _rc))
        else:
            logging.warning('platform is not connected')
        # else:
        #     logging.warning('response is too large')

    def __pre_handle_response__(self, cloud_msg):
        """
        平台的异步请求请求的响应两次，接收到请求就发一次，处理完成后再发一次
        :param cloud_msg:
        :return:
        """
        if cloud_msg['methodName'] in self.async_methods:
            self.__send_response_to_platform__(payload={
                'methodName': cloud_msg['methodName'],
                'requestId': cloud_msg['requestId'],
                'status': 0,
                'message': 'accepted',
                'timestamp': int(time.time() * 1000),
                'data': {}
            })

    def __request_handler__(self, cloud_msg):
        try:
            # 预处理
            self.__pre_handle_response__(cloud_msg)

            _resp = self.request_worker.handle_request(data=cloud_msg)

            # 后处理，将http请求的回应转换成mqtt的，并上传到平台
            self.__post_handle_response__(cloud_msg, _resp)
        except:
            logging.exception('mqtt handle {} failed'.format(cloud_msg))

    def __post_handle_response__(self, cloud_msg, resp):
        """
        通用的后处理，把http response转换成mqtt 可认的格式，并把结果发给平台
        :param cloud_msg:
        :param resp:
        :return:
        """

        # # 为适应mqtt相应的格式，调整或增加一些字段
        #
        # if type(resp.data) == dict:
        #     _real_data = resp.data
        # elif type(resp.data) == str:
        #     _real_data = {'content': resp.data}
        # else:
        #     _real_data = {}
        # resp.status = 'OK'
        # if 'status' not in _real_data:
        #     _real_data['status'] = resp.status
        # if 'message' not in _real_data and cloud_msg['methodName'] in self.async_methods:
        #     _real_data['message'] = 'updated' if resp.status == 0 or resp.status == 200 else 'failed'

        _full_payload = {
            'methodName': cloud_msg['methodName'],
            'requestId': cloud_msg['requestId'],
            'timestamp': int(time.time() * 1000),
            'deviceId': self.device_id,
            'status': resp.status,
            'data': resp.data,
            'message': resp.message
        }

        self.__send_response_to_platform__(payload=_full_payload)

    def __init_topics__(self):
        # publish相关
        # 主动请求
        # self.req_topic = cf_def.get('Mqtt', 'p2p_topic_tpl').format(device_id=self.device_id,
        #                                                         device_or_cloud='device',
        #                                                         action='req')
        # 发送响应
        self.rsp_topic = f"$kibo/ids/p2p/{self.device_id}/cloud/req"
        # 遗言
        # self.lwt_topic = cf_def.get('Mqtt', 'p2p_topic_tpl').format(device_id=self.device_id,
        #                                                         device_or_cloud='device',
        #                                                         action='lwt')

        # subscribe相关
        # 平台下发的请求
        self.cloud_req_topic = f"$kibo/ids/p2p/{self.device_id}/device/rsp"
        # cf_def.get('Mqtt', 'p2p_topic_tpl').format(device_id=self.device_id,
        # device_or_cloud='cloud',
        # action='req')
        # 平台下发的响应
        # self.cloud_rsp_topic = cf_def.get('Mqtt', 'p2p_topic_tpl').format(device_id=self.device_id,
        #                                                               device_or_cloud='cloud',
        #                                                               action='rsp')

        # 平台下发的广播
        # self.cloud_broadcast_topic = cf_def.get('Mqtt', 'bct_topic_tpl')

    def run(self):
        logging.info(
            'mqtt:{}::{} thread[{}] running'.format(self.server_url, self.server_port, threading.current_thread()))
        logging.debug('current threads: {}'.format(threading.enumerate()))
        while self.mqtt_run_flag:
            try:
                if is_ip_accessible(self.server_url, self.server_port):
                    if not self.mqtt_is_connected:
                        self.mqtt_client.connect(self.server_url, self.server_port, 60)
                        self.mqtt_client.loop_forever()
                else:
                    logging.debug('can not access {}:{}, run flag {}'.format(self.server_url,
                                                                             self.server_port,
                                                                             self.mqtt_run_flag))
                    time.sleep(1)
                    continue
            except Exception as e:
                if self.mqtt_client:
                    self.mqtt_client.disconnect()
                logging.exception('mqtt connect failed')

            # 正常情况，程序不应该执行到这里
            # sleep 1 second, then retry connection
            logging.error('mqtt:{}::{} connection broken'.format(self.server_url, self.server_port))
            self.mqtt_is_connected = False
            time.sleep(1)


class Worker:
    def __init__(self):
        self.method_map = {
            # http and new mqtt request
            # modify:编辑、修改 ; handle: 操作 ; require: 请求
            "test": test,
        }

    @staticmethod
    def __parse_request_(request):
        """
        parse django data or mqtt data
        :param data:
        :param request_type:
        :return:
        """
        _method, _payload = None, None

        data = request

        _method = None if 'methodName' not in data else data['methodName']

        _payload = None if 'payload' not in data else data['payload']
        _payload['requestId'] = data['requestId']
        # if _payload:
        #     _payload['requestId'] = '' if 'requestId' not in data else data['requestId']
        #     _payload['deviceId'] = '' if 'deviceId' not in data else data['deviceId']

        return _method, _payload

    def handle_request(self, data):
        _method, _payload = self.__parse_request_(data)
        logging.debug("method:{}, payload:{}".format(_method, _payload))
        if _payload is None or _method is None or type(_payload) == list:
            _resp = Response(-1, message='系统异常，请重试')
        elif _method not in self.method_map:
            _resp = Response(-1, message='系统异常，请重试')
        else:
            _tmp_payload = _payload
            if 'content' in _payload and type(_payload) == dict:
                _tmp_payload = _payload.copy()
                del _tmp_payload['content']
            logging.info('receive method |{}| payload |{}|'.format(_method, _tmp_payload))

            _resp = self.method_map[_method](_payload)
        return _resp


def test(payload):
    return Response(1)


def is_ip_accessible(ip_address, port):
    _ret = -1
    _sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _ret = sock.connect_ex((ip_address, port))
    except:
        pass
    finally:
        if _sock:
            _sock.close()

    return _ret == 0


if __name__ == '__main__':
    worker = Worker()
    mqtt_client = PlatformClient(worker)

    mqtt_client.run()
