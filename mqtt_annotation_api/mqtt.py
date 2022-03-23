import paho.mqtt.client as mqtt

class Client(mqtt.Client):
    def __init__(self, host, name, username, password):
        super().__init__(name)
        self.host = host
        self.username_pw_set(username, password)
        self.subscribers = []

    def on_connect(self, client, userdata, flags, rc):
        print("Connected")
        for sub in self.subscribers:
            super().subscribe(sub["topic"])
            self.message_callback_add(sub["topic"], sub["callback"])

    def connect(self):
        super().connect(self.host)

    def subscribe(self, topic):
        def topic_subscribe(callback):
            self.subscribers.append({"topic": topic, "callback": callback})

        return topic_subscribe
