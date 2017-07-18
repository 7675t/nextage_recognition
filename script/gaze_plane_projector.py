#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import tf
from tf import TransformListener
from geometry_msgs.msg import PointStamped, Vector3Stamped

# input geometry_msgs/Vector3Stamped
# 平面はframe_idをパラメータで与え、その座標系のxy平面とする
# output geometry_msgs/PointStamped

# rotate vector v1 by quaternion q1 
def qv_mult(q1, v1):
    v1 = tf.transformations.unit_vector(v1)
    q2 = list(v1)
    q2.append(0.0)
    return tf.transformations.quaternion_multiply(
        tf.transformations.quaternion_multiply(q1, q2), 
        tf.transformations.quaternion_conjugate(q1)
    )[:3]

class VectorPlaneProjector:
    def __init__(self):
        self.nh = rospy.init_node('vector_plane_projector')
        self.tf = TransformListener()
        self.plane_frame_id = rospy.get_param('~plane_frame_id', 'map')
        rospy.Subscriber("gaze_vector", Vector3Stamped, self.vector_cb)
        self.pub_ = rospy.Publisher('~point', PointStamped, queue_size=1)

    def vector_cb(self, vector_msg):
        vector_frame_id = vector_msg.header.frame_id
        self.tf.waitForTransform(
            self.plane_frame_id, vector_frame_id, rospy.Time(0), rospy.Duration(1.0))
        vector = self.tf.transformVector3(self.plane_frame_id, vector_msg)
        position, quaternion = self.tf.lookupTransform(self.plane_frame_id, vector_frame_id, rospy.Time(0))
        # calculate projected point
        # a x + b y + c z = d
        # x = ax t + dx, y = ay t + dy , z = az t + dz
        (ax, ay, az) = (vector.vector.x, vector.vector.y, vector.vector.z)
        (dx, dy, dz) = position
        # z=0平面との交点を求める
        # 交点が無い場合
        if az == 0:
            return 
        t = - dz / az
        x = ax * t + dx
        y = ay * t + dy
        point = PointStamped()
        point.header = vector.header
        point.point.x = x
        point.point.y = y
        point.point.z = 0
        self.pub_.publish(point)

if __name__ == '__main__':
    node = VectorPlaneProjector()

    rospy.spin()
