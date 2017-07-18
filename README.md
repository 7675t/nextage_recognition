# nextage_recognition

## Template matching 

### Check with image files

To check the template matching with image files, 

```
$ roslaunch match_template_with_file.launch scene_image:=scene-1.png template_image:=template-1.png
```

The red rectangle shows the most matched region.

You can use rqt and dynamic reconfigure to change the method and
threshold to detect the template.

### Check with camera image stream

To check the template matching with a camera interactively, 
you bring up your camera like:

```
$ rosrun libuvc_camera camera_node __ns:=camera
```

Then launch the matching launch file as:

```
$ roslaunch nextage_recognition match_template_with_camera.launch
```

You need to specify the template image. Drag the rectangular region in 'Scene Image' window to specify the template image.

You can get the template postition in the image as:
```
$ rostopic echo match_template/pixel_position
```

## Locate 3D position using a plane constraint

If you know the target object on a plane, you can use
gaze_plane_projector to calculate the 3D position of the target.

```
$ roslaunch nextage_recognition detect_object_on_plane.launch
```

The projecto plane is set by the parameter 'plane_frame_id'. The default is 'map'. The x-y plane of the frame is the projection plane.

You can see projected point on the plane as:

```
$ rostopic echo /gaze_plane_projector/point
```
