# 1. ROS KVS Stramer

Generic ROS1 kinesis video streamer

## 1.1 License

The source code is released under [Apache 2.0](https://aws.amazon.com/apache-2-0/).

## 1.2 Resources
* [ROS KVS streamer](https://github.com/aws-deepracer/ros-kvs-streamer)

# 2. Open source packages from github

Under the condition that RoboMaker team does not bloom release these packages for Ubuntu20:04 and ROS Noetic, they have to be built from source.
.git and .github are removed to track these code in code.amazon.com. Otherwise, these packages will be track as sudmodules.

## 2.1 utils-common

https://github.com/aws-robotics/utils-common at commit b70e9416968ca5a56fd263ff9c96c80793a7230f

ROS AWS Utils Common Library

## 2.2 utils-ros1

https://github.com/aws-robotics/utils-ros1 at commit d4d64f73727149fd8885f13581a74d5ca6dcfb6c

AWS Utils Library for ROS1 with patch https://github.com/aws-robotics/utils-ros1/pull/36 to support ROS Noetic with Ubuntu20:04 SDK

## 2.3 kinesisvideo-encoder-common

https://github.com/aws-robotics/kinesisvideo-encoder-common at commit b798a06cca43891170d33da3aa329648c864a418

ROS H264 Video Encoding Library for Amazon Kinesis Video Streams

## 2.4 kinesisvideo-encoder-ros1

https://github.com/aws-robotics/kinesisvideo-encoder-ros1.git at commit d2e3fb3e72fc481e18b8c29e4d831707e453d276

h264_video_encoder

## 2.5 kinesisvideo-common

https://github.com/aws-robotics/kinesisvideo-common at commit b0b4d9f011454a22957383cf3ef5c781e2384a96

ROS Kinesis Service Common Library

## 2.6 kinesisvideo-ros1

https://github.com/aws-robotics/kinesisvideo-ros1 at commit ad9014035ca16d5b212c4f58ffcbb346a53b441b

kinesis_video_streamer

# 3. Setup

## 3.1 setup
download all required GitHub repo as specified in section 2 and patch them.
```
chmod +x setup.sh
./setup.sh
```

Follow standard ros procedure to build
```
colcon build
```

## 3.2 aws configure
follow this https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html to configure aws credential
which grant kvs permission to the running docker instance.

# 4. Launch and run
There are two ways to launch kvs streamer for byoa through launch file or python script

## 4.1 using launch file
In order to launch through launch file, one need to use h264_video_encoder.launch and kinesis_video_streamer.launch with corresponding argument and ns.

* `ns`: ros node namespace. For example `“/agent0”`
* `topic`: ros topic that will be published to kinesis video stream server. For example, `"/agent0/follow_camera/zed/rgb/image_rect_color"`
* `stream_name`: AWS kinesis video stream service stream name. For example, `"byoa_test_stream"`.
* `stream_region`: AWS kinesis video stream service stream region. For example, `"us-east-1"`.

```
    <include file="$(find ros_kvs_streamer)/launch/h264_video_encoder.launch" ns="/agent0">
      <arg name="topic" value="/agent0/follow_camera/zed/rgb/image_rect_color" />
    </include>

    <include file="$(find ros_kvs_streamer)/launch/kinesis_video_streamer.launch" ns="/agent0">
      <arg name="topic" value="/agent0/follow_camera/zed/rgb/image_rect_color" />
      <arg name="stream_name" value="byoa_test_stream" />
      <arg name="stream_region" value="us-east-1" />
    </include>
```

## 4.2 using python script
Besides using launch file, one can also using python script KvsStreamer which warp both h264_video_encoder.launch and kinesis_video_streamer.launch to start kvs through popen subprocess call to start launch file.

There are two ways to start/stop kvs streamer by using class instantiation or static method. Here are the use case for each of them.

* Clase instantiation.
    * start/stop kvs service are in the same module. In this case, one does not need to keep track of namespace and KvsStreamer instance will track all internal parameters.
* Static method
    * start/stop kvs service are in multiple modules. In this case one need to track the namespace to stop after it is started at another module.

```
from ros_kvs_streamer.kvs_streamer import KvsStreamer

#############################
# start using static method #
#############################
KvsStreamer.start(
    namespace="agent0",
    topic="/agent0/follow_camera/zed/rgb/image_rect_color",
    stream_name="byoa_test_stream",
    stream_region="us-east-1")

############################
# stop using static method #
############################
KvsStreamer.stop(
    namespace="agent0") 

#############################
# using class instantiation #
#############################
kvs_streamer = KvsStreamer(
    namespace="agent0",
    topic="/agent0/follow_camera/zed/rgb/image_rect_color",
    stream_name="byoa_test_stream",
    stream_region="us-east-1")
    
# start
kvs_streamer.start()

# stop
kvs_streamer.stop()
```

# 5. checkout kvs stream
Log into your aws account that you set up permission for step 3 through isengard, go to `Kinesis Video Streams` service and then `video streams` tab on the left. Then, search for the `stream_name` that you specified.
