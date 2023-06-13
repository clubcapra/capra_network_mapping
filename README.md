# capra_network_mapping

This package allows to gather information from the current wifi connection and map it in real time.

The `wifi_signal_pub` node publishes two topics:

+ `wifi_signal` with messages of type UserData from rtabmap/msgs. It produces the data required by rtabmap to create MapData objects representing the signal quality.
+ `wifi_signal_raw` with a custom message type of type WifiStrength. It produces a simple human readable message that describes the connection strength. It is easier to reuse for other purposes.

The `wifi_mapper` node publishes a single topic:

+ `wifi_signal_points` of message type PointCloud2. It

## Setup

The `wifi_signal_pub` node finds the current interface by itself, no need to configure it.

However, it requires the wifi symbol topic to be added to the rtabmap launch file. Under the CAPRA architecture, it is under the [markhor_slam launch files](https://github.com/clubcapra/markhor/tree/master/markhor_slam/launch). The arg is named `user_data_async_topic` and its value is `/wifi_signal`.

## Sources

Most of the work was provided by [IntRoLab](https://introlab.3it.usherbrooke.ca) in their [rtabmap_ros](https://github.com/introlab/rtabmap_ros) package and [tutorials](http://wiki.ros.org/rtabmap_ros/Tutorials).

In this case, we used their [Wifi Signal Strength Mapping Tutorial](http://wiki.ros.org/rtabmap_ros/Tutorials/WifiSignalStrengthMappingUserDataUsage) to do this project.
