# MIT License
#
# Copyright (c) 2026 Alexandre Loeblein Heinen

from __future__ import annotations

from enum import IntEnum


class Direction(IntEnum):
    """Rotation directions for circular arcs."""

    RIGHT = -1  # Clockwise is negative
    LEFT = 1  # Counter-clockwise is positive


class PathType(IntEnum):
    """Dubins path types for CSC configurations."""

    LSL = 0  # Left-Straight-Left (CCW-S-CCW)
    LSR = 1  # Left-Straight-Right (CCW-S-CW)
    RSL = 2  # Right-Straight-Left (CW-S-CCW)
    RSR = 3  # Right-Straight-Right (CW-S-CW)


def path_type_from_directions(
    initial_direction: Direction, final_direction: Direction
) -> PathType:
    """
    Convert initial and final arc directions to Dubins path type.

    Args:
        initial_direction: Direction of the initial arc (LEFT or RIGHT).
        final_direction: Direction of the final arc (LEFT or RIGHT).

    Returns:
        Corresponding PathType.
    """
    if initial_direction == Direction.LEFT:
        if final_direction == Direction.LEFT:
            return PathType.LSL
        elif final_direction == Direction.RIGHT:
            return PathType.LSR
    else:
        if final_direction == Direction.LEFT:
            return PathType.RSL
        elif final_direction == Direction.RIGHT:
            return PathType.RSR

    raise ValueError(
        "Invalid combination of arc directions: "
        f"{initial_direction}, {final_direction}"
    )


def directions_from_path_type(
    path_type: PathType,
) -> tuple[Direction, Direction]:
    """
    Convert Dubins path type to initial and final arc directions.

    Args:
        path_type: The type of the Dubins path.

    Returns:
        A tuple containing the initial and final arc directions.
    """
    if path_type == PathType.LSL:
        return (Direction.LEFT, Direction.LEFT)
    elif path_type == PathType.LSR:
        return (Direction.LEFT, Direction.RIGHT)
    elif path_type == PathType.RSL:
        return (Direction.RIGHT, Direction.LEFT)
    elif path_type == PathType.RSR:
        return (Direction.RIGHT, Direction.RIGHT)

    raise ValueError(f"Invalid Dubins path type: {path_type}")
