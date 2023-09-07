import numpy as np
from sensor_msgs.msg import PointCloud2, PointField
import array
import sys
import time
from .registry import converts_from_numpy, converts_to_numpy

@converts_to_numpy(PointCloud2)
def point_cloud2_to_array(msg):
    """
    Convert a sensor_msgs/PointCloud2 message to a NumPy array. The fields
    in the PointCloud2 message are mapped to the fields in the NumPy array
    as follows:
    * x, y, z -> X, Y, Z
    * rgb -> RGB
    * intensity -> I
    * other fields are ignored
    """
    # Get the index of the "rgb" and "intensity" fields in the PointCloud2 message
    field_names = [field.name for field in msg.fields]
    # Check if the "rgb" field is present
    if "rgb" in field_names:
        rgb_idx = field_names.index("rgb")
        rgb_flag = True
    else:
        rgb_flag = False

    if "intensity" in field_names:
        intensity_idx = field_names.index("intensity")
        intensity_flag = True
    else:
        intensity_flag = False

    # Convert the PointCloud2 message to a NumPy array
    pc_data = np.frombuffer(
        msg.data, dtype=np.uint8).reshape(-1, msg.point_step)
    xyz = pc_data[:, 0:12].view(dtype=np.float32).reshape(-1, 3)
    if rgb_flag:
        rgb = pc_data[:, rgb_idx:rgb_idx+3][:, ::-1]
    if intensity_flag:
        intensity = pc_data[:, intensity_idx:intensity_idx +
                            2].view(dtype=np.uint16)

    # return the arrays in a dictionary
    if rgb_flag and intensity_flag:
        return {"xyz": xyz, "rgb": rgb, "intensity": intensity}

    if rgb_flag and not intensity_flag:
        return {"xyz": xyz, "rgb": rgb}

    if not rgb_flag and intensity_flag:
        return {"xyz": xyz, "intensity": intensity}

    if not rgb_flag and not intensity_flag:
        return {"xyz": xyz}


@converts_from_numpy(PointCloud2)
def array_to_point_cloud2(np_array, frame_id='base_link'):
    """
    Convert a numpy array to a PointCloud2 message. The numpy array must have a "xyz" field
    and can optionally have a "rgb" field and a "intensity" field.
    """
    # Check if the "rgb" field is present
    rgb_flag = "rgb" in np_array.keys()
    intensity_flag = "intensity" in np_array.keys()

    # Create the PointCloud2 message
    msg = PointCloud2()
    msg.header.frame_id = frame_id
    current_time = time.time()
    msg.header.stamp.sec = int(current_time)
    msg.header.stamp.nanosec = int((current_time - msg.header.stamp.sec) * 1e9)
    msg.height = 1
    msg.width = np_array["xyz"].shape[0]
    msg.fields = [
        PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
        PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1)]

    if rgb_flag:
        msg.fields.append(PointField(name='rgb', offset=12,
                          datatype=PointField.UINT32, count=1))
    if intensity_flag:
        msg.fields.append(PointField(name='intensity', offset=16,
                          datatype=PointField.UINT16, count=1))
    msg.is_bigendian = sys.byteorder != 'little'
    # Check if message is dense
    msg.is_dense = not np.isnan(np_array["xyz"]).any()

    # Calculate the point_step and row_step
    if rgb_flag and intensity_flag:
        msg.point_step = 18
    if rgb_flag and not intensity_flag:
        msg.point_step = 16
    if not rgb_flag and intensity_flag:
        msg.point_step = 14
    if not rgb_flag and not intensity_flag:
        msg.point_step = 12        

    msg.row_step = msg.point_step * msg.width

    # The PointCloud2.data setter will create an array.array object for you if you don't
    # provide it one directly. This causes very slow performance because it iterates
    # over each byte in python.
    # Here we create an array.array object using a memoryview, limiting copying and
    # increasing performance.
    if rgb_flag and intensity_flag:
        memory_view = memoryview(np.hstack(np_array["xyz"].astype(np.float32).tobytes(
        ), np_array["rgb"].astype(np.uint32).tobytes(), np_array["intensity"].astype(np.uint16).tobytes()))

    if rgb_flag and not intensity_flag:
        memory_view = memoryview(np.hstack((np_array["xyz"].astype(np.float32).tobytes(
        ), np_array["rgb"].astype(np.uint32).tobytes())))

    if not rgb_flag and intensity_flag:
        memory_view = memoryview(np.hstack(np_array["xyz"].astype(np.float32).tobytes(
        ), np_array["intensity"].astype(np.uint16).tobytes()))
    
    if not rgb_flag and not intensity_flag:
        memory_view = memoryview(np_array["xyz"].astype(np.float32).tobytes())

    if memory_view.nbytes > 0:
        array_bytes = memory_view.cast("B")
    else:
        # Casting raises a TypeError if the array has no elements
        array_bytes = b""

    as_array = array.array("B")
    as_array.frombytes(array_bytes)
    msg.data = as_array

    return msg
