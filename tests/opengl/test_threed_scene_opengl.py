from __future__ import annotations

import numpy as np
import pytest

from manim import ThreeDScene


def test_3dillusion_camera_rotation(using_opengl_renderer):
    scene = ThreeDScene()
    scene.begin_3dillusion_camera_rotation(rate=2, origin_phi=1, origin_theta=0)
    scene.update_mobjects(0.5)
    theta, phi, _ = scene.camera.euler_angles
    assert theta == pytest.approx(0.2 * np.sin(1))
    assert phi == pytest.approx(1 + 0.1 * np.cos(1) - 0.1)

    scene.stop_3dillusion_camera_rotation()
    scene.update_mobjects(0.5)
    assert scene.camera.euler_angles[0] == pytest.approx(0.2 * np.sin(1))


def test_stop_ambient_camera_rotation_only_stops_given_angle(using_opengl_renderer):
    scene = ThreeDScene()
    scene.begin_ambient_camera_rotation(rate=0.1, about="theta")
    scene.begin_ambient_camera_rotation(rate=0.1, about="phi")
    scene.stop_ambient_camera_rotation(about="phi")
    theta, phi, _ = scene.camera.euler_angles.copy()
    scene.update_mobjects(1)
    assert scene.camera.euler_angles[0] == pytest.approx(theta + 0.1)
    assert scene.camera.euler_angles[1] == pytest.approx(phi)


def test_stop_ambient_camera_rotation_keeps_camera_updaters(using_opengl_renderer):
    scene = ThreeDScene()

    def updater(mob, dt):
        pass

    scene.camera.add_updater(updater)
    scene.begin_ambient_camera_rotation()
    scene.stop_ambient_camera_rotation()
    assert scene.camera.get_updaters() == [updater]


def test_ambient_camera_rotation_invalid_angle(using_opengl_renderer):
    scene = ThreeDScene()
    with pytest.raises(ValueError):
        scene.begin_ambient_camera_rotation(about="x")
    with pytest.raises(ValueError):
        scene.stop_ambient_camera_rotation(about="x")
