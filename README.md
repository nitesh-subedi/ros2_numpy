# ros2_numpy

Note: This is the same as the original ros_numpy package by eric-wieser and ros2_numpy package by box-robotics just edited to be OS independent and installable using pip.

### Pointcloud manipulation is updated `ros2_numpy.pointcloud2` to be compatible with ROS2. It now gives a structured numpy array with the fields `x`, `y`, `z`, `rgb`, `intensity`. The `rgb` field is a 3-tuple of uint8 values. The `intensity` field is a float32 value. The `x`, `y`, `z` fields are float32 values.

<br>

This project is a fork of [ros2_numpy](https://github.com/Box-Robotics/ros2_numpy) to work with ROS 2. It provides tools for converting ROS messages to and from numpy arrays. In the ROS 2 port, the module has been renamed to
`ros2_numpy`. Users are encouraged to update their application code to import
the module as shown below.

```
pip install ros2-numpy
import ros2_numpy as rnp
```

Prefacing your calls like `rnp.numpify(...)` or `rnp.msgify(...)` should help
future proof your codebase while the ROS 2 ports are API compatible.

This module contains two core functions:

* `arr = numpify(msg, ...)` - try to get a numpy object from a message
* `msg = msgify(MessageType, arr, ...)` - try and convert a numpy object to a message

Currently supports:

* `sensor_msgs.msg.PointCloud2` &harr; structured `dict`: # See PointCloud2 message type in ros2

   ```python
   data = {"xyz": np.random.rand(100, 3), "rgb": np.random.rand(100, 3)}
   msg = ros2_numpy.msgify(PointCloud2, data)
   ```

   ```
   data = ros2_numpy.numpify(msg)
   ```

* `sensor_msgs.msg.Image` &harr; 2/3-D `np.array`, similar to the function of `cv_bridge`, but without the dependency on `cv2`
* `nav_msgs.msg.OccupancyGrid` &harr; `np.ma.array`
* `geometry.msg.Vector3` &harr; 1-D `np.array`. `hom=True` gives `[x, y, z, 0]`
* `geometry.msg.Point` &harr; 1-D `np.array`. `hom=True` gives `[x, y, z, 1]`
* `geometry.msg.Quaternion` &harr; 1-D `np.array`, `[x, y, z, w]`
* `geometry.msg.Transform` &harr; 4&times;4 `np.array`, the homogeneous transformation matrix
* `geometry.msg.Pose` &harr; 4&times;4 `np.array`, the homogeneous transformation matrix from the origin

Support for more types can be added with:

```python
@ros2_numpy.converts_to_numpy(SomeMessageClass)
def convert(my_msg):
    return np.array(...)

@ros2_numpy.converts_from_numpy(SomeMessageClass)
def convert(my_array):
    return SomeMessageClass(...)
```

Any extra args or kwargs to `numpify` or `msgify` will be forwarded to your conversion function


## Future work

* Add simple conversions for:

  * `geometry_msgs.msg.Inertia`
