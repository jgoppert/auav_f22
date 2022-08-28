#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

import rospy
import message_filters
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32, Bool
import numpy as np


class Referee(Node):
    
    def __init__(self):
        super().__init__('referee')
        # publications
        self.pub_score = self.create_publisher(Float32, 'score', queue_size=10)

        # subscriptions
        self.sub_rover = rospy.Subscriber(Odometry, 'rover', self.rover_callback, 10)
        self.sub_drone = rospy.Subscriber(Odometry, 'drone', self.drone_callback, 10)
        self.sub_drone_ready = rospy.Subscriber(Bool, 'drone_ready', self.drone_ready_callback, 10)
        self.sub_rover_finished = rospy.Subscriber(Bool, 'rover_finished', self.rover_finished_callback, 10)

        # attributes
        self.drone_position = None
        self.rover_position = None
        self.drone_ready = False
        self.rover_finished = False
        self.start = None
        self.sum = 0
        self.samples = 0

    def drone_callback(self, odom):
        self.drone_position = odom.pose.pose.position

    def rover_callback(self, odom):
        """score when we see the rover, use last known drone position"""
        self.rover_position = odom.pose.pose.position

        # if time expired
        if self.rover_finished:
            self.get_logger().warn('trial finished, final score: %f', self.score)
            rospy.signal_shutdown('finished')
            return

        # abort if no drone position
        if self.drone_position is None:
            return

        distance = np.linalg.norm(np.array([
            self.rover_position.x - self.drone_position.x,
            self.rover_position.y - self.drone_position.y,
            self.rover_position.z - self.drone_position.z]))
        inst_score = 0
        if (distance <  5):
            inst_score = 1 - np.abs(distance - 1)/4
        self.sum += inst_score
        self.samples += 1
        self.score = self.sum/self.samples
        self.get_logger().info('distance: %f, inst score: %f, sum: %f samples: %10d, score: %f',
                distance, inst_score, self.sum, self.samples, self.score)
        self.pub_score.publish(Float32(self.score))

    def drone_ready_callback(self, msg):
        self.drone_ready = msg.data

    def rover_finished_callback(self, msg):
        self.rover_finished = msg.data


def main(args=None):
    rclpy.init(args=args)
    referee = Referee()
    rclpy.spin(referee)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
