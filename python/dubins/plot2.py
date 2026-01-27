# MIT License
#
# Copyright (c) 2026 Alexandre Loeblein Heinen

"""Plotting utilities for 2D Dubins paths."""

from __future__ import annotations

from matplotlib import pyplot
import numpy as np
import os
import logging

from path_type import Direction, PathType, directions_from_path_type
from dubins2 import DubinsPath, rotate_vector

logger = logging.getLogger("dubins")


def plot_dubins_path(ax: pyplot.Axes, path: DubinsPath) -> None:
    """
    Plot a single Dubins path on the given Axes.

    Args:
        ax: Matplotlib Axes to plot on.
        path: DubinsPath instance to plot.
    """
    # Get a color from colormap
    cm = pyplot.get_cmap("tab10")
    color = cm(path.path_type.value)
    
    # Plot the initial and final positions
    ax.plot(*path.initial_position, "s", color=color, label=path.path_type.name)
    ax.plot(*path.final_position, "s", color=color)
    
    # Plot the tangent positions
    ax.plot(*path.initial_tangent_position, "o", color=color)
    ax.plot(*path.final_tangent_position, "o", color=color)
    
    # Plot the circle centers
    ax.plot(*path.initial_center_position, "x", color=color)
    ax.plot(*path.final_center_position, "x", color=color)
    
    initial_direction, final_direction = directions_from_path_type(path.path_type)
    
    # Draw the arc from the initial position to the initial tangent position
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
    
    # Plot the tangent vectors
    ax.quiver(
        *path.initial_position,
        *(path.initial_tangent_unit * path.radius),
        color=color,
        angles="xy",
        scale_units="xy",
        scale=1.0,
    )
    ax.quiver(
        *path.final_position,
        *(path.final_tangent_unit * path.radius),
        color=color,
        angles="xy",
        scale_units="xy",
        scale=1.0,
    )


def plot_dubins_paths(
    paths: list[DubinsPath],
    title: str = "Dubins Paths",
    file_name: str = "dubins_paths_2d.png",
) -> None:
    """
    Plot multiple Dubins paths.

    Args:
        paths: List of DubinsPath instances to plot.
        title: Title of the plot.
        file_name: Name of the output file.
    """
    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(title)

    for path in paths:
        plot_dubins_path(ax, path)

    ax.set_aspect("equal", adjustable="box")
    ax.legend()
    pyplot.grid()

    # Find the project root directory
    my_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(my_dir))
    images_dir = os.path.join(root_dir, "files", "images")

    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    file_path = os.path.join(images_dir, file_name)
    pyplot.savefig(file_path)
    pyplot.close()

    logger.info("Dubins paths plot saved to %s", file_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Plot a sample set of Dubins paths for demonstration
    initial_position = np.array([0.0, 0.0])
    final_position = np.array([-5.0, 5.0])
    initial_tangent_unit = np.array([1.0, 0.0])
    final_tangent_unit = np.array([1.0, 1.0]) / np.sqrt(2)
    radius = 1.0

    args = dict(
        initial_position=initial_position,
        final_position=final_position,
        initial_tangent_unit=initial_tangent_unit,
        final_tangent_unit=final_tangent_unit,
        radius=radius,)
    
    paths = [DubinsPath(path_type=pt, **args) for pt in PathType]
    plot_dubins_paths(paths)