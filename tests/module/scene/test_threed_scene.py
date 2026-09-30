import numpy as np
import pytest

from manim import DEGREES, Circle, Square, ThreeDScene


def test_fixed_mobjects():
    scene = ThreeDScene()
    s = Square()
    c = Circle()
    scene.add_fixed_in_frame_mobjects(s, c)
    assert set(scene.mobjects) == {s, c}
    assert set(scene.camera.fixed_in_frame_mobjects) == {s, c}
    scene.remove_fixed_in_frame_mobjects(s)
    assert set(scene.mobjects) == {s, c}
    assert set(scene.camera.fixed_in_frame_mobjects) == {c}
    scene.add_fixed_orientation_mobjects(s)
    assert set(scene.camera.fixed_orientation_mobjects) == {s}
    scene.remove_fixed_orientation_mobjects(s)
    assert len(scene.camera.fixed_orientation_mobjects) == 0


def test_set_to_default_angled_camera_orientation():
    scene = ThreeDScene()

    scene.set_to_default_angled_camera_orientation(phi=45 * DEGREES)

    assert scene.camera.get_phi() == 45 * DEGREES
    assert scene.camera.get_theta() == -135 * DEGREES


def test_stop_ambient_camera_rotation_keeps_3dillusion_rotation():
    scene = ThreeDScene()
    scene.begin_3dillusion_camera_rotation(origin_phi=1, origin_theta=0)
    scene.begin_ambient_camera_rotation(rate=1)
    scene.stop_ambient_camera_rotation()
    scene.update_mobjects(0.5)
    assert scene.camera.get_theta() == pytest.approx(0.2 * np.sin(0.5))


def test_stop_3dillusion_camera_rotation_keeps_ambient_rotation():
    scene = ThreeDScene()
    scene.begin_ambient_camera_rotation(rate=1)
    scene.begin_3dillusion_camera_rotation()
    scene.stop_3dillusion_camera_rotation()
    theta = scene.camera.get_theta()
    scene.update_mobjects(0.5)
    assert scene.camera.get_theta() == pytest.approx(theta + 0.5)
