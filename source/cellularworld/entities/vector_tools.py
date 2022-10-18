import numpy
import math

ZERO_DIRECTION = numpy.array([1., 0.])


def magnitude(vector):
    return numpy.linalg.norm(vector)


def unit_vector(vector):
    _magnitude = magnitude(vector)
    if _magnitude == 0:
        return numpy.array([0., 0.])
    return vector / _magnitude


def direction_angle(vector):
    if all(vector == 0):
        return 0
    normalised_strength = unit_vector(vector)
    dot_product = numpy.dot(normalised_strength, ZERO_DIRECTION)
    radians = numpy.arccos(dot_product)
    degrees = numpy.rad2deg(radians)
    if normalised_strength[1] < 0:
        degrees += 180
    return degrees


def direction_vector(angle):
    theta = numpy.deg2rad(angle)
    rotation_matrix = numpy.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
    vector = numpy.dot(rotation_matrix, ZERO_DIRECTION)
    return vector
