import paho.mqtt.client as mqtt

HOST = "192.168.10.8"
PORT = 61613


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("/+")


def on_message(client, userdata, msg):
    print(msg.topic+" "+msg.payload.decode("utf-8"))


def test():
    client = mqtt.Client()    # 可能需要设置ClientId
    client.username_pw_set("admin", "password")  # 必须设置，否则会返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 60)
    client.loop_forever()


if __name__ == '__main__':
    test()
