import rclpy
from rclpy.node import Node as RosNode

rclpy.init(args=None)

class Node(RosNode):
    def __init__(self, name, topics={}, qos_profile=0):
        super().__init__(name)
        self.qos_profile = qos_profile
        self.subscribers = []
        self.timed_subscriber_memory = {}
        self.pubs = {}
        for topic, msg_type in topics.items():
            self.pubs[topic] = self.create_publisher(
                topic=topic,
                msg_type=msg_type,
                qos_profile=qos_profile
            )

    def spin(self):
        for sub in self.subscribers:
            self.create_subscription(
                topic=sub["topic"],
                callback=sub["callback"],
                msg_type=sub["type"],
                qos_profile=self.qos_profile
            )
        
        rclpy.spin(self)

    def subscribe(self, topic, msg_type):
        def subscribe_decorator(callback):
            self.subscribers.append({
                "topic": topic, 
                "callback": callback,
                "type": msg_type
            })

        return subscribe_decorator

    def subscribe_timed(self, rate, topic, msg_type):
        def timed_decorator(callback):
            self.timed_subscriber_memory[topic] = None

            self.subscribers.append({
                "topic": topic, 
                "callback": lambda msg: self.timed_subscriber_memory.update({topic: msg}),
                "type": msg_type
            })

            self.create_timer(
                timer_period_sec=rate,
                callback=lambda: (
                    callback(self.timed_subscriber_memory[topic]) 
                    if self.timed_subscriber_memory[topic] 
                    else False
                )
            )

        return timed_decorator

    def timed(self, rate):
        def timed_decorator(callback):
            self.create_timer(
                timer_period_sec=rate,
                callback=callback
            )

        return timed_decorator

    def publish(self, topic, msg):
        self.pubs[topic].publish(msg)

    def destroy_node(self):
        super().destroy_node()
        rclpy.shutdown()