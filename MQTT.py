import paho.mqtt.client as mqtt_client
import ssl

globalName = "myGS/"


class Topics:
    # Radio
    freq = f"{globalName}radio/freq"
    bw = f"{globalName}radio/bw"
    cr = f"{globalName}radio/cr"
    plen = f"{globalName}radio/plen"
    sf = f"{globalName}radio/sf"
    txpwr = f"{globalName}radio/txpwr"
    lnag = f"{globalName}radio/lnag"
    chksum = f"{globalName}radio/chksum"
    ackdelay = f"{globalName}radio/ackd"
    ackwait = f"{globalName}radio/ackw"
    rxto = f"{globalName}radio/rxto"

    # Rotator
    daemoncmd = f"{globalName}rot/daemon"
    rothost = f"{globalName}rot/host"
    rotport = f"{globalName}rot/port"
    rotdevice = f"{globalName}rot/dev"
    rotsspeed = f"{globalName}rot/sspeed"
    rotmodel = f"{globalName}rot/model"
    rotselect = f"{globalName}rot/select"
    newpreset = f"{globalName}rot/newpreset"


# Define the MQTT topics
# pub_topics = ["radio/freq", "radio/bw", "radio/br", "radio/chksum", "msg/cmd"]
sub_topics = [
    f"{globalName}msg/telemetry",
    f"{globalName}msg/payload",
    f"{globalName}msg/reply",
]

# Define the MQTT broker address and port
# broker_address = "10.42.0.236"
# broker_address = "test.mosquitto.org"  # "localhost"
# broker_port = 1883


class TLS:
    cafile = None
    cert = None
    key = None

tlsC = TLS()
# Define the on_connect callback function


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to all topics
    for topic in sub_topics:
        print(topic)
        client.subscribe(topic)


# Define the on_message callback function


# def on_message(client, userdata, msg):
#     print(f"Received message on {msg.topic}: {msg.payload.decode()}")


# Initialize the MQTT client
mqttC = mqtt_client.Client()

# TEST: make this configurable
# usingTLS = True
# if usingTLS:
#     mqttC.tls_set(
#         ca_certs='tls/mosquitto.org.crt',
#         certfile="tls/client.crt",
#         keyfile="tls/client.key",
#         tls_version=ssl.PROTOCOL_TLSv1_2,
#     )
#     mqttC.tls_insecure_set(False)


# Assign the callback functions
mqttC.on_connect = on_connect
# mqttC.on_message = on_message

# Connect to the broker
# mqttC.connect(broker_address, broker_port)

# Start the MQTT client loop
# mqttC.loop_start()

# Publish messages to the topics
# try:
#     while True:
#         cmd = input("user cmd:").split()
#         if len(cmd) > 1:
#             topic, value = cmd
#         else:
#             continue
#
#         if topic not in pub_topics:
#             print("Topic not available")
#         print(mqttC.publish(globalName + topic, value))
#         """
#         for i, topic in enumerate(topics):
#             message = f"Message from Program 2 to {topic}"
#             mqttC.publish(topic, message)
#             print(f"Published message to {topic}: {message}")
#             time.sleep(1)
#         time.sleep(5)  # Delay between each round of publishing
#         """
# except KeyboardInterrupt:
#     mqttC.loop_stop()
#     mqttC.disconnect()
#
# # Stop the MQTT client loop and disconnect
# mqttC.loop_stop()
# mqttC.disconnect()
