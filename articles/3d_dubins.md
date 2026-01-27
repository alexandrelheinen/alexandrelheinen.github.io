---
layout: default
title: "Dubins Paths: Extending the classical 2D path problem to true 3D space using horn torus geometry"
date: 2026-01-28
description: "Extending the classical 2D path problem to true 3D space using horn torus geometry"
---

<div class="container">
    <a href="../index.html" class="back-link">← Back to Home</a>
    
    <div class="article-content" markdown="1">

# Dubins Paths: Extending the classical 2D path problem to true 3D space using horn torus geometry

<div class="article-meta">
<span class="article-date">{{ page.date | date: "%B %d, %Y" }}</span>
</div>

> **THIS IS A WORK IN PROGRESS ARTICLE**

One of the most significant subjects in robotic motion planning — perhaps the most discussed research topic outside of the machine learning hype — is path or trajectory generation. This remains an intensely complex field, largely because there is no single, universal mathematical representation for a trajectory or a path that satisfies all robotic constraints simultaneously.

When referring to trajectories, even if we fix all other variables at a given moment in time, considering every possible movement a system can perform means choosing a potentially infinite-dimensional function of the system's state over its lifetime. In other words, we are trying to shape a function $$x(t \mid t_0)$$ defined on any arbitrarily long subinterval of what I like to call $$\mathcal{T}_{t \ge t_0} \cong [t_0, \infty)$$. Indeed, this means that at any instant $$t_0 \in \mathcal{T}$$, we make a partition of the set $$\mathcal{T}$$, where we know everything that happens before it and must predict what to do afterwards (i.e., $$\mathcal{T}_{t>t_0}$$), potentially forever.

> Although, even in the literature, we tend to call the time set this fancy $$\mathcal{T}$$, there is no practical difference in assuming that it is homeomorphic to the real numbers, or $$\mathcal{T} \cong \mathbb{R}$$, which makes it lighter to interpret in my opinion.

In other cases, rather than finding an infinite policy for the system trajectory, the problem can be constrained to a finite interval. Usually this is referred to as "going from point A to point B" in non-technical terms. In this case, the goal is to determine a finite trajectory model and includes some terminal constraints about the "point B" state.

For both the finite and infinite trajectory problems, the application of such laws in discrete embedded systems (such as microcontrollers) follows a _receding horizon_ strategy, where the agent plans a sequence of future actions over a fixed time window but only executes the very first step of that plan.

To illustrate this, I will share a short video of my previous work involving a drone flying through treetops. The video shows, as a red line, the predicted position for a limited time horizon at every evolving time instant, representing the function $$x(t \mid t_0)$$. In this context, the trajectory is a dynamic object that is re-evaluated as the system state and environment evolve. 

{% include youtube_short.html id="6UWra-GdOGg" %}

Finally, the introduction above works for _trajectories_, since they explicitly involve time as a parameter. When talking about _paths_, the same reasoning is valid; however, in the particular case of a finite path, the domain of evolution of the system is usually normalized to the unit interval $$\sigma \in [0, 1]$$ to eliminate any dependence on time.

Anyways... The goal of grounding all these complex ideas is to focus more precisely on a staple of mobile robotics: Dubins paths. In this model for finite path planning, the system state is reduced to its pose, and the logic remains static over time. We define an initial and final pose, and the optimal path is drawn from A to B while respecting a maximum curvature constraint.

## Dubins paths from 2D to 3D

In 2D space, this problem is well-characterized. The shortest path is proven to be a composition of circular arcs (C) and straight line segments (S), typically in CSC or CCC configurations. Since CCC paths are only optimal for very short distances (usually when the distance between A and B is less than 4R), most literature focuses on the CSC solution.

When setting initial and final conditions, there are four possible CSC Dubins paths. The literature identifies them as LSL, LSR, RSL, and RSR. While L and R indicate the rotation direction, I prefer the terms CW (clockwise) and CCW (counterclockwise) for clarity, though I can understand why someone might find it confusing throughout a text.

{% include figure.html 
   src="../files/images/dubins_paths_2d.png" 
   alt="2D CSC Dubins paths"
   number="1"
   caption="Representation of the four possible CSC 2D Dubins path"
   source="Personal reproduction (<a href='../python/dubins/plot2.py'>script</a>) of the image from <a href='https://myenigma.hatenablog.com/entry/2017/05/01/144956'>MyEnigma blog</a>" 
%}

Most research assumes the radii of both circles are equal, which is logical for a vehicle with symmetric turning limits. However, the problem extends easily to different radii. Once the radii are fixed, the solution becomes a variation of the belt/pulley problem, or finding the bitangents between two circles.

While 2D planning is straightforward, in the literature, 3D applications often take a shortcut by using "cylindrical" paths: solving the Dubins problem on a 2D plane and adding a linear vertical component. But what if we consider a truly free three-dimensional problem, such as a spherical path where the initial and final arcs are arbitrary and non-coplanar?

The solution lies in two observations. First, once the directions are set, the 2D Dubins path is defined by rotation angles — we can call them azimuth angles — that determine the arc lengths. Second, to extend the reasoning to the 3D case, we must consider the manifold formed by all possible circles passing through a point. In 3D, the span of all circles of a fixed radius passing through a single point with a shared tangent vector defines a horn torus.

Thus, the standard 2D case is simply a coplanar section of this manifold, where the elevation angle of the rotation axis is restricted to 0° or 180° relative to the plane of motion. Moving to true 3D space requires us to solve for two additional degrees of freedom: the initial and final elevation angles of the rotation planes.

> **TODO:** Add image of two collinear tori with the plane and two oblique planes.

## Spherical pulley

{% include youtube.html id="aWfmgsal0JU" %}