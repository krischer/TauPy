#!/usr/bin/env python
"""
Package for storage and manipulation of seismic earth models.
"""

from header import TauPException


class VelocityLayer(object):
    """
    The VelocityLayer class stores and manipulates a singly layer. An
    entire velocity model is implemented as an Vector of layers.
    """
    def __init___(self, layer_number, topDepth, botDepth, topPVelocity,
                  botPVelocity, topSVelocity, botSVelocity, topDensity=2.6,
                  botDensity=2.6, topQp=1000, botQp=1000, topQs=2000,
                  botQs=2000):
        self.layer_number = int(layer_number)
        self.topDepth = float(topDepth)
        self.botDepth = float(botDepth)
        self.topPVelocity = float(topPVelocity)
        self.botPVelocity = float(botPVelocity)
        self.topSVelocity = float(topSVelocity)
        self.botSVelocity = float(botSVelocity)
        self.topDensity = float(topDensity)
        self.botDensity = float(botDensity)
        self.topQp = float(topQp)
        self.botQp = float(botQp)
        self.topQs = float(topQs)
        self.botQs = float(botQs)

    @property
    def thickness(self):
        """
        Thickness of the layer.
        """
        return self.botDepth - self.topDepth

    def evaluateAtBottom(self, materialProperty):
        materialProperty = materialProperty.lower()
        if materialProperty == "p":
            return self.botPVelocity
        elif materialProperty == "s":
            return self.botSVelocity
        elif materialProperty in "rd":
            return self.botDensity
        raise TauPException("Unknown material property.")

    def evaluateAtTop(self, materialProperty):
        materialProperty = materialProperty.lower()
        if materialProperty == "p":
            return self.topPVelocity
        elif materialProperty == "s":
            return self.topSVelocity
        elif materialProperty in "rd":
            return self.topDensity
        raise TauPException("Unknown material property.")

    def evaluateAt(self, depth, materialProperty):
        thickness = self.thickness
        materialProperty = materialProperty.lower()
        if materialProperty == "p":
            slope = (self.botPVelocity - self.topPVelocity) / thickness
            return slope * (depth - self.topDepth) + self.topPVelocity
        elif materialProperty == "s":
            slope = (self.botSVelocity - self.topSVelocity) / thickness
            return slope * (depth - self.topDepth) + self.topSVelocity
        elif materialProperty in "rd":
            slope = (self.botDensity - self.topDensity) / thickness
            return slope * (depth - self.topDepth) + self.topDensity
        raise TauPException("Unknown material property.")

    def __str__(self):
        description = "Layer %i (%.1f - %.1f)" % (
            self.layer_number, self.topDepth, self.botDepth)
        description += " P " + self.topPVelocity + " " + self.botPVelocity
        description += " S " + self.topSVelocity + " " + self.botSVelocity
        description += " Density " + self.topDensity + " " + self.botDensity
        return description