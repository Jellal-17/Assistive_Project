#!/usr/bin/env python3
import rospy
import math
import copy

from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped

import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class sim_nav_goals():
    def __init__(self):
        rospy.init_node('sim_nav_goals', anonymous=True)

        self.counter = 0
        
        client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        client.wait_for_server()

        rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.poseCallback, queue_size=10)
        
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():            
        
            msg = PoseStamped()
            msg.header.frame_id = 'map'
            if self.counter % 2 == 0:
                # First pose
                theta = 0.0  # Orientation angle
                msg.pose.position.x = 0.0
                msg.pose.position.y = 0.5
                msg.pose.position.z = 0.0
                msg.pose.orientation.x = 0.0
                msg.pose.orientation.y = 0.0
                msg.pose.orientation.z = math.sin(theta/2)
                msg.pose.orientation.w = math.cos(theta/2)
            else:
                # Second pose
                theta = 0.0  # Orientation angle
                msg.pose.position.x = -3.0
                msg.pose.position.y = 1.0
                msg.pose.position.z = 0.0
                msg.pose.orientation.x = 0.0
                msg.pose.orientation.y = 0.0
                msg.pose.orientation.z = math.sin(theta/2)
                msg.pose.orientation.w = math.cos(theta/2)
                        
            msg.header.stamp = rospy.Time.now()
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = "map"
            goal.target_pose.header.stamp = rospy.Time.now()
            goal.target_pose = msg
            client.send_goal(goal)
            wait = client.wait_for_result()
    
            if not wait:
                rospy.logerr("Action server is not available.")
                rospy.signal_shutdown("Action server is not available.")
            else:
                x = client.get_result()
                
            self.counter += 1
            rate.sleep()

    def poseCallback(self, p):
        theta = 2*math.atan2(p.pose.pose.orientation.z, p.pose.pose.orientation.w)
        st = 'sim: Pose:x={x:.2f}m, y={y:.2f}m, yaw={th:.2f}rad'.format(x=p.pose.pose.position.x, y=p.pose.pose.position.y, th=theta)
        rospy.loginfo(st)

if __name__ == '__main__':
    try:
        control = sim_nav_goals()
    except rospy.ROSInterruptException:
        pass
