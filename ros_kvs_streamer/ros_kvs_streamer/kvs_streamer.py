#################################################################################
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.          #
#                                                                               #
#   Licensed under the Apache License, Version 2.0 (the "License").             #
#   You may not use this file except in compliance with the License.            #
#   You may obtain a copy of the License at                                     #
#                                                                               #
#       http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                               #
#   Unless required by applicable law or agreed to in writing, software         #
#   distributed under the License is distributed on an "AS IS" BASIS,           #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    #
#   See the License for the specific language governing permissions and         #
#   limitations under the License.                                              #
#################################################################################
"""A class for Kvs Streamer"""
import rospy

from subprocess import Popen
from threading import Event, Thread
from ros_kvs_streamer.ros_util import ROSUtil
from sensor_msgs.msg import Image


class KvsStreamer(object):
    """
    Kvs streamer class
    """
    _kvs_node_name_formats = ["/{}/kinesis_video_streamer",
                              "/{}/h264_video_encoder"]

    def __init__(self,
                 topic: str,
                 namespace: str,
                 stream_name: str,
                 stream_region: str,
                 use_proxy_topic: bool = False,
                 publish_rate: float = 0.0) -> None:
        """
        Kvs streamer constructor
        - Using proxy topic will repeatedly publish the last frame received periodically with given publish_rate.

        Args:
            topic (str): ros image topic that will be publish to kvs
            namespace (str): ros namespace that will be used for
                             both kinesis_video_streamer and h264_video_encoder node
            stream_name (str): AWS kinesis video stream service stream name
            stream_region (str): AWS kinesis video stream service stream region
            use_proxy_topic (bool): flag whether to use proxy ROS topic.
            publish_rate (float): the publish rate in seconds for proxy topic.
        """
        self._topic = topic
        self._proxy_topic = topic + '_proxy'
        self._namespace = namespace
        self._stream_name = stream_name
        self._stream_region = stream_region

        self._use_proxy_topic = use_proxy_topic
        self._kvs_proxy_publisher = None
        self._kvs_publisher_thread = None
        self._thread_terminate_event = Event()
        self._frame = None
        self._publish_rate = 0.0 if publish_rate < 0.0 else publish_rate

    def start(self) -> None:
        """
        Class method to start kvs streamer
        """
        topic = self._topic
        if self._use_proxy_topic:
            rospy.Subscriber(self._topic, Image, self._on_frame_received)
            self._kvs_proxy_publisher = rospy.Publisher(self._proxy_topic, Image,
                                                        queue_size=1)
            self._kvs_publisher_thread = Thread(target=self._kvs_frame_publisher)
            self._kvs_publisher_thread.start()
            topic = self._proxy_topic
        KvsStreamer.start_kvs(
            topic=topic,
            namespace=self._namespace,
            stream_name=self._stream_name,
            stream_region=self._stream_region)

    def _on_frame_received(self, frame: Image) -> None:
        """
        On frame received from ROS topic.

        Args:
            frame (Image): frame received.
        """
        self._frame = frame

    def _kvs_frame_publisher(self) -> None:
        """
        Proxy ROS topic publisher thread.
        """
        while not self._thread_terminate_event.wait(self._publish_rate):
            if self._frame:
                self._kvs_proxy_publisher.publish(self._frame)

    def stop(self) -> None:
        """
        Class method to stop kvs streamer
        """
        if self._kvs_publisher_thread:
            self._thread_terminate_event.set()
            self._kvs_publisher_thread.join()
            self._kvs_publisher_thread = None
        KvsStreamer.stop_kvs(
            namespace=self._namespace)

    @staticmethod
    def start_kvs(topic: str,
                  namespace: str,
                  stream_name: str,
                  stream_region: str = "us-east-1") -> None:
        """
        static method to start kvs streamer

        Args:
            topic (str): ros image topic that will be publish to kvs
            namespace (str): ros namespace that will be used for
                             both kinesis_video_streamer and h264_video_encoder node
            stream_name (str): AWS kinesis video stream service stream name
            stream_region (str): AWS kinesis video stream service stream region
        """
        if not any([ROSUtil.is_ros_node_alive(node_name_format.format(namespace))
                    for node_name_format in KvsStreamer._kvs_node_name_formats]):
            Popen("roslaunch ros_kvs_streamer kinesis_video_streamer.launch "
                  "topic:={} stream_name:={} stream_region:={} "
                  "__ns:={}".format(topic,
                                    stream_name,
                                    stream_region,
                                    namespace),
                  shell=True,
                  executable="/bin/bash")
            Popen("roslaunch ros_kvs_streamer h264_video_encoder.launch "
                  "topic:={} "
                  "__ns:={}".format(topic,
                                    namespace),
                  shell=True,
                  executable="/bin/bash")
            ROSUtil.wait_for_rosnode(
                alive_nodes=[node_name_format.format(namespace)
                             for node_name_format in KvsStreamer._kvs_node_name_formats])
        else:
            rospy.loginfo("[KvsStreamer] kvs streamer and encoder cannot start because they have "
                          "already started for {}".format(namespace))

    @staticmethod
    def stop_kvs(namespace: str) -> None:
        """
        Static method to stop kvs streamer

        Args:
            namespace (str): kvs stream namespace
        """
        if all([ROSUtil.is_ros_node_alive(node_name_format.format(namespace))
                for node_name_format in KvsStreamer._kvs_node_name_formats]):
            Popen("rosnode kill /{}/kinesis_video_streamer".format(namespace),
                  shell=True,
                  executable="/bin/bash")
            Popen("rosnode kill /{}/h264_video_encoder".format(namespace),
                  shell=True,
                  executable="/bin/bash")
            ROSUtil.wait_for_rosnode(
                dead_nodes=[node_name_format.format(namespace)
                            for node_name_format in KvsStreamer._kvs_node_name_formats])
        else:
            rospy.loginfo("[KvsStreamer] kvs streamer and encoder cannot stop because they never "
                          "started for {}".format(namespace))
