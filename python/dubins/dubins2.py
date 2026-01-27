# MIT License
#
# Copyright (c) 2026 Alexandre Loeblein Heinen

"""2D Dubins path generation for CSC configurations."""

from __future__ import annotations

import numpy as np
import logging

from path_type import PathType, directions_from_path_type, Direction

logger = logging.getLogger("dubins")
unit_z = np.array((0.0, 0.0, 1.0))
invalid_vector = np.full((2,), np.nan)


def cartesian_position_from_polar(
    center_position: np.ndarray, radius: float, angle: float
) -> np.ndarray:
    """
    Compute the Cartesian position from polar coordinates.

    Args:
        center_position: Center position as a 2D numpy array.
        radius: Radius from the center.
        angle: Angle in radians.

    Returns:
        Cartesian position as a 2D numpy array.
    """
    x = center_position[0] + radius * np.cos(angle)
    y = center_position[1] + radius * np.sin(angle)
    return np.array((x, y))


def rotate_vector(v: np.ndarray, angle: float) -> np.ndarray:
    """
    Rotate a 2D vector by a given angle.

    Args:
        v: Input vector as a 2D numpy array.
        angle: Angle in radians to rotate the vector.

    Returns:
        Rotated vector as a 2D numpy array.
    """
    rotation_matrix = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    return rotation_matrix @ v


def compute_center_position(
    position: np.ndarray,
    tangent_unit: np.ndarray,
    radius: float,
    direction: Direction,
) -> np.ndarray:
    """
    Compute the center position of the circle.

    Args:
        position: Position as a 2D numpy array.
        tangent_unit: Tangent unit vector as a 2D numpy array.
        radius: Radius of the circle.
        direction: Direction of turn (LEFT=CCW, RIGHT=CW).

    Returns:
        Center position as a 2D numpy array.
    """
    # z-axis is the unit z vector
    tangent_unit_3d = np.array((*tangent_unit, 0.0))  # y-axis
    radial_unit = np.cross(tangent_unit_3d, unit_z)[:2]  # x = y x z
    return position - direction.value * radius * radial_unit


def normalize_vector(v: np.ndarray) -> np.ndarray:
    """
    Normalize a 2D vector.

    Args:
        v: Input vector as a 2D numpy array.

    Returns:
        Normalized vector as a 2D numpy array.
    """
    norm = np.linalg.norm(v)

    if np.isclose(norm, 0.0):
        return np.zeros_like(v)

    return v / norm


def compute_tangent_positions(
    initial_center: np.ndarray,
    final_center: np.ndarray,
    radius: float,
    path_type: PathType,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the tangent positions between two circles.

    Args:
        initial_center: Center of the initial circle as a 2D numpy array.
        final_center: Center of the final circle as a 2D numpy array.
        radius: Radius of the circles.
        path_type: Type of the Dubins path.

    Returns:
        A tuple containing the initial and final tangent positions as 2D numpy arrays.
    """
    offset_position = final_center - initial_center
    distance = np.linalg.norm(offset_position)

    if np.isclose(distance, 0.0):
        raise ValueError("Initial and final circle centers are too close.")

    match path_type:
        case PathType.LSL:
            # Compute outer lower tangent points: angles are both -pi/2
            initial_relative_azimuth = -0.5 * np.pi
            final_relative_azimuth = -0.5 * np.pi

        case PathType.LSR:
            # Compute upper tangent points: from the bottom to the top
            belt_azimuth = np.arccos(2 * radius / distance)
            initial_relative_azimuth = -belt_azimuth
            final_relative_azimuth = np.pi - belt_azimuth

        case PathType.RSL:
            # Compute inner tangent points: from the top to the bottom
            belt_azimuth = np.arccos(2 * radius / distance)
            initial_relative_azimuth = belt_azimuth
            final_relative_azimuth = -np.pi + belt_azimuth

        case PathType.RSR:
            # Compute outer upper tangent points: angles are both +pi/2
            initial_relative_azimuth = 0.5 * np.pi
            final_relative_azimuth = 0.5 * np.pi

        case _:
            raise ValueError(f"Invalid Dubins path type: {path_type}")

    offset_unit = offset_position / distance
    return (
        rotate_vector(offset_unit, initial_relative_azimuth) * radius + initial_center,
        rotate_vector(offset_unit, final_relative_azimuth) * radius + final_center,
    )


def relative_azimuth(
    initial_position: np.ndarray,
    final_position: np.ndarray,
    center_position: np.ndarray,
) -> float:
    """
    Compute the relative azimuth angle from one position to another
    around a center position.

    Args:
        initial_position: Initial position as a 2D numpy array.
        final_position: Final position as a 2D numpy array.
        center_position: Center position as a 2D numpy array.

    Returns:
        Relative azimuth angle in radians
    """
    initial_vector = initial_position - center_position
    final_vector = final_position - center_position

    initial_angle = np.arctan2(initial_vector[1], initial_vector[0])
    final_angle = np.arctan2(final_vector[1], final_vector[0])

    return final_angle - initial_angle


class DubinsPath:
    """
    Container for a 2D Dubins path representation.

    This container holds only the strictly necessary parameters to define a
    Dubins path of type CSC (Circular-Straight-Circular). Any other values
    are computed on demand as properties.
    """

    def __init__(
        self,
        path_type: PathType,
        radius: float,
        initial_position: np.ndarray,
        initial_tangent_unit: np.ndarray,
        final_position: np.ndarray,
        final_tangent_unit: np.ndarray,
    ):
        # Ensure that the tangent vectors are unit vectors
        self.radius = radius
        self.path_type = path_type
        self.initial_position = initial_position
        self.initial_tangent_unit = normalize_vector(initial_tangent_unit)
        self.final_position = final_position
        self.final_tangent_unit = normalize_vector(final_tangent_unit)

        # Compute the circle center positions
        initial_direction, final_direction = directions_from_path_type(path_type)
        self.initial_center_position = compute_center_position(
            self.initial_position,
            self.initial_tangent_unit,
            self.radius,
            initial_direction,
        )
        self.final_center_position = compute_center_position(
            self.final_position,
            self.final_tangent_unit,
            self.radius,
            final_direction,
        )

        # Compute the tangent point angles
        self.initial_tangent_position, self.final_tangent_position = (
            compute_tangent_positions(
                self.initial_center_position,
                self.final_center_position,
                self.radius,
                self.path_type,
            )
        )

    def __repr__(self) -> str:
        name = f"{self.path_type.name} Dubins Path"
        if self.is_valid:
            return (
                f"{name}: L={self.total_length:.2f}, "
                f"a1={np.degrees(self.initial_arc_angle):.0f}°, "
                f"a2={np.degrees(self.final_arc_angle):.0f}°"
            )
        else:
            return f"{name}: INVALID"

    @property
    def is_valid(self) -> bool:
        """Check if the path is valid (non-negative lengths)."""
        return self.total_length >= 0.0

    @staticmethod
    def create_invalid(path_type: PathType) -> DubinsPath:
        """
        Create an invalid DubinsPath instance.

        Args:
            path_type: The type of the Dubins path.

        Returns:
            An invalid DubinsPath instance.
        """
        return DubinsPath(
            path_type,
            radius=np.nan,
            initial_position=invalid_vector,
            initial_tangent_unit=invalid_vector,
            final_position=invalid_vector,
            final_tangent_unit=invalid_vector,
        )

    @property
    def straight_length(self) -> float:
        """Get the length of the straight segment of the Dubins path."""
        return np.linalg.norm(
            self.final_tangent_position - self.initial_tangent_position
        )

    @property
    def initial_arc_angle(self) -> float:
        """Get the angle of the initial arc segment in radians."""
        # Initial arc length from the initial position to the initial tangent position
        direction, _ = directions_from_path_type(self.path_type)
        angle = relative_azimuth(
            self.initial_position,
            self.initial_tangent_position,
            self.initial_center_position,
        )
        return (direction.value * angle) % (2 * np.pi)

    @property
    def initial_arc_length(self) -> float:
        """Get the length of the initial arc segment."""
        return self.radius * self.initial_arc_angle

    @property
    def final_arc_angle(self) -> float:
        """Get the angle of the final arc segment in radians."""
        # Final arc length from the final tangent position to the final position
        _, direction = directions_from_path_type(self.path_type)
        angle = relative_azimuth(
            self.final_tangent_position,
            self.final_position,
            self.final_center_position,
        )
        return (direction.value * angle) % (2 * np.pi)

    @property
    def final_arc_length(self) -> float:
        """Get the length of the final arc segment."""
        return self.radius * self.final_arc_angle

    @property
    def total_length(self) -> float:
        """Get the total length of the Dubins path."""
        return self.initial_arc_length + self.straight_length + self.final_arc_length


if __name__ == "__main__":
    from matplotlib import pyplot

    logging.basicConfig(level=logging.INFO)
    fig = pyplot.figure()
    rows = 3
    cols = 3
    cm = pyplot.get_cmap("tab10")

    initial_tagent_unit = np.array((0.0, 1.0))  # Upward
    final_tagent_unit = np.array((1.0, 0.0))  # Rightward
    radius = 1.0

    for i, (row, col) in enumerate(np.ndindex((rows, cols))):
        ax = fig.add_subplot(rows, cols, i + 1)
        path_type = PathType(i % len(PathType))
        initial_position = np.random.uniform(0.0, 2.0, 2)
        final_position = np.random.uniform(4.0, 6.0, 2)

        try:
            path = DubinsPath(
                path_type,
                radius,
                initial_position,
                initial_tagent_unit,
                final_position,
                final_tagent_unit,
            )
        except Exception as e:
            logger.warning(f"Could not create Dubins path: {e}")
            continue

        color = cm(path_type.value)

        # Plot the initial and final positions
        ax.plot(*initial_position, "s", color=color)
        ax.plot(*final_position, "s", color=color)

        # Plot the tangent positions
        ax.plot(*path.initial_tangent_position, "o", color=color)
        ax.plot(*path.final_tangent_position, "o", color=color)

        # Plot the circle centers
        ax.plot(*path.initial_center_position, "x", color=color)
        ax.plot(*path.final_center_position, "x", color=color)

        initial_direction, final_direction = directions_from_path_type(path.path_type)

        # Draw the arc from the initial positions to the initial tangent position
        initial_arc_angles = np.linspace(
            0.0, initial_direction * path.initial_arc_angle, num=100
        )
        initial_positions = np.array(
            [
                rotate_vector(
                    path.initial_position - path.initial_center_position, angle
                )
                + path.initial_center_position
                for angle in initial_arc_angles
            ]
        )
        ax.plot(initial_positions[:, 0], initial_positions[:, 1], "-", color=color)

        # Draw the arc from the final tangent position to the final position
        final_arc_angles = np.linspace(
            0.0, final_direction * path.final_arc_angle, num=100
        )
        final_positions = np.array(
            [
                rotate_vector(
                    path.final_tangent_position - path.final_center_position, angle
                )
                + path.final_center_position
                for angle in final_arc_angles
            ]
        )
        ax.plot(final_positions[:, 0], final_positions[:, 1], "-", color=color)

        # Plot the straight line segment
        ax.plot(
            [path.initial_tangent_position[0], path.final_tangent_position[0]],
            [path.initial_tangent_position[1], path.final_tangent_position[1]],
            "-",
            color=color,
        )

        # Plot the quiver
        ax.quiver(
            *initial_position,
            *(initial_tagent_unit * radius),
            color=color,
            angles="xy",
            scale_units="xy",
            scale=1.0,
        )
        ax.quiver(
            *final_position,
            *(final_tagent_unit * radius),
            color=color,
            angles="xy",
            scale_units="xy",
            scale=1.0,
        )

        ax.set_title(str(path))
        ax.set_aspect("equal", "box")
        ax.grid(True)
        ax.set_xlim(-2, 8)
        ax.set_ylim(-2, 8)

    # save in .bundle/
    fig.tight_layout()
    pyplot.show()
