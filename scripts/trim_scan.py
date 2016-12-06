#!/usr/bin/env python

"""This node re-publishes /scan to /scan_narrow by artificially
reducing the field of view.  This seems to address a bug in gmapping.

"""
import rospy
import math

from sensor_msgs.msg import LaserScan

class TrimNode(object):
    """ Class that attempts to maintain a fixed distance from
    the obstacle ahead.

    Subscribes to: /scan
    Publishes to: /scan_narrow
    """


    def __init__(self):
        """ Set up the node, publishers and subscribers. """
        rospy.init_node('approach')

        rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.pub = rospy.Publisher('/scan_narrow', LaserScan,
                                       queue_size=10)
       
        rospy.spin()


    def scan_callback(self, scan_msg):
        """ Republish the scan with a narrower field of view """
        old_num_ranges = len(scan_msg.ranges)
        new_num_ranges = int(math.floor(old_num_ranges * .8))
        num_trim = old_num_ranges - new_num_ranges
        start_index = num_trim/2
        end_index = num_trim/2 + new_num_ranges
        new_ranges = scan_msg.ranges[start_index:end_index+1]
        new_angle_min = (scan_msg.angle_min +
                         start_index * scan_msg.angle_increment)
        new_angle_max = (scan_msg.angle_min +
                         end_index * scan_msg.angle_increment)
        scan_msg.ranges = new_ranges
        scan_msg.angle_min = new_angle_min
        scan_msg.angle_max = new_angle_max
        self.pub.publish(scan_msg)
        

if __name__ == "__main__":
    approach = TrimNode()
