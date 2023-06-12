#!/usr/bin/env python
import rospy
import struct
import os
from rtabmap_ros.msg import UserData
from capra_signal_strength.msg import WifiStrength

# Taken from http://wiki.ros.org/rtabmap_ros/Tutorials/WifiSignalStrengthMappingUserDataUsage

def loop():
    # Setup node and publishers
    rospy.init_node('wifi_signal_pub', anonymous=True)
    for_map_publish = rospy.Publisher('wifi_signal', UserData, queue_size=10)
    raw_publish = rospy.Publisher('wifi_signal_raw', WifiStrength, queue_size=10)
    rate = rospy.Rate(1) # Atleast as fast as rtabmap
    
    while not rospy.is_shutdown():
        
        # Get active wifi interface and its quality
        nmcli_cmd = os.popen('nmcli dev wifi | grep "^*"').read()
        nmcli_list = nmcli_cmd.split()
        
        # A roundabout way to get the active interface
        active_ssid = nmcli_list[1]
        ssid_cmd = os.popen('iwconfig 2>/dev/null | grep -e ' + active_ssid ).read()
        active_interface = ssid_cmd.split()[0]
                
        # Get signal strength information
        ifconfig_cmd = os.popen('iwconfig ' + active_interface + ' | grep -e Bit -e Link').read()
        ifconfig_list = ifconfig_cmd.split()
        
        if len(nmcli_list) <= 6:
            rospy.logerr("Cannot get info from wireless!")
        else:
            # Call the functions to build the msgs
            user_data_msg = put_into_user_data_msg(nmcli_list);
            wifi_strength_msg = put_into_wifi_strength_msg(ifconfig_list);

            for_map_publish.publish(user_data_msg)
            raw_publish.publish(wifi_strength_msg)
        
        rate.sleep()
        
def put_into_user_data_msg(nmcli_list):
    quality = float(nmcli_list[6])
    msg = UserData()
    
    # Sample output of nmcli, the command used:
    #    *       Kabelplus_free  Infra  36    540 Mbit/s  48      <other non-ASCII symbols>
    
    # To make it compatible with c++ map data subscriber example, use dBm
    dBm = quality/2-100
    
    # For debug purposes
    # rospy.loginfo("Network \"%s\": Quality=%d, %f dBm", nmcli_list[1], quality, dBm)
    
    # Create user data [level, stamp].
    # Any format is accepted.
    # However, if CV_8UC1 format is used, make sure rows > 1 as
    # rtabmap will think it is already compressed.
    msg.rows = 1
    msg.cols = 2
    msg.type = 6 # Use OpenCV type (here 6=CV_64FC1): http://ninghang.blogspot.com/2012/11/list-of-mat-type-in-opencv.html
    
    # We should set stamp in data to be able to
    # retrieve it from the saved user data as we need
    # to get precise position in the graph afterward.
    msg.data = struct.pack(b'dd', dBm, rospy.get_time())
    
    return msg;
    
def put_into_wifi_strength_msg(ifconfig_list):
    msg = WifiStrength()
    
    # Sample output of iwconfig, the command used:
    #    Bit Rate=270 Mb/s   Tx-Power=22 dBm
    #    Link Quality=41/70  Signal level=-69 dBm
    
    msg.bit_rate = ifconfig_list[1].split("=")[1] + " " +ifconfig_list[2]
    
    quality_field = ifconfig_list[6].split("=")[1]
    msg.quality = int(quality_field.split("/")[0])
    msg.max_quality = int(quality_field.split("/")[1])
    
    msg.signal_level = int(ifconfig_list[8].split("=")[1])
    
    return msg;

if __name__ == '__main__':
    try:
        loop()
    except rospy.ROSInterruptException:
        pass