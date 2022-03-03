import sys
import time
import openvr

print("OpenVR test program")

try:
    if openvr.isHmdPresent(): print("VR head set found")
    if openvr.isRuntimeInstalled(): print("Runtime is installed")

    vr_system = openvr.init(openvr.VRApplication_Scene)

    print(openvr.getRuntimePath())
    print(vr_system.getRecommendedRenderTargetSize())
    print(vr_system.isDisplayOnDesktop())

    for i in range(10):
        xform = vr_system.getEyeToHeadTransform(openvr.Eye_Left)
        print(xform)
        sys.stdout.flush()
        time.sleep(0.2)

    openvr.shutdown()

except Exception as e:
    print(e)

    from openvr.glframework.qt5_app import Qt5App
    from openvr.gl_renderer import OpenVrGlRenderer
    from openvr.color_cube_actor import ColorCubeActor
    from openvr.tracked_devices_actor import TrackedDevicesActor

    renderer = OpenVrGlRenderer(multisample=2)
    renderer.append(ColorCubeActor())
    
    controllers = TrackedDevicesActor(renderer.poses)
    controllers.show_controllers_only = False
    renderer.append(controllers)

    with Qt5App(renderer, "PyQt5 OpenVR color cube") as qt5_app:
        qt5_app.run_loop()