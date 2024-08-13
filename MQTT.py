import paho.mqtt.client as mqtt

# Define the MQTT topics
pub_topics = ["radio/freq", "radio/bw", "radio/br", "radio/chksum", "msg/cmd"]
sub_topics = ["msg/telemetry", "msg/payload", "msg/reply"]

# Define the MQTT broker address and port
# broker_address = "10.42.0.236"
broker_address = "test.mosquitto.org"  # "localhost"
broker_port = 1883

globalName = "myGS/"

# Define the on_connect callback function


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to all topics
    for topic in sub_topics:
        print(globalName + topic)
        client.subscribe(globalName + topic)


# Define the on_message callback function


def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")


# Initialize the MQTT client
client = mqtt.Client()

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, broker_port)

# Start the MQTT client loop
client.loop_start()

# Publish messages to the topics
try:
    while True:
        cmd = input("user cmd:").split()
        if len(cmd) > 1:
            topic, value = cmd
        else:
            continue

        if topic not in pub_topics:
            print("Topic not available")
        print(client.publish(globalName + topic, value))
        """
        for i, topic in enumerate(topics):
            message = f"Message from Program 2 to {topic}"
            client.publish(topic, message)
            print(f"Published message to {topic}: {message}")
            time.sleep(1)
        time.sleep(5)  # Delay between each round of publishing
        """
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()

# Stop the MQTT client loop and disconnect
client.loop_stop()
client.disconnect()
