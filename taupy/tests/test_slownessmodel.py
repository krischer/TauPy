import unittest

from taupy.SlownessModel import SlownessModel
from taupy.SlownessModel import SlownessModelError
from taupy.VelocityModel import VelocityModel
from taupy.SlownessLayer import SlownessLayer
from taupy.VelocityLayer import VelocityLayer

class TestSlownessModel(unittest.TestCase):
    def test_createSample(self):
        testmod = SlownessModel(VelocityModel.readVelocityFile('./data/iasp91.tvel'))
        testmod.DEBUG = True
                
        # An error should be raised if vMod.validate fails, or vMod
        # has 0 layers, or the top layer has a 0 S wave velocity. Only
        # the first is testable (I think?); setting the topSVelocity
        # to 0 makes vMod.validate fail.
        with self.assertRaises(SlownessModelError):
            testmod.vMod.layers[0].topSVelocity = 0
            testmod.createSample()

        # test normal execution:
        testmod = SlownessModel(VelocityModel.readVelocityFile('./data/iasp91.tvel'))
        testmod.DEBUG = True
        testmod.createSample()
        self.assertEqual(testmod.radiusOfEarth, 6371)
        self.assertTrue(testmod.validate())

    def test_findCriticalPoints(self):
        testmod = SlownessModel(VelocityModel.readVelocityFile('./data/iasp91.tvel'))
        testmod.DEBUG = True
        # This line would normally run in createSample:
        testmod.radiusOfEarth = testmod.vMod.radiusOfEarth
        # Maybe merge these?

    def test_slownesslayer(self):
        vLayer=VelocityLayer(1, 10, 31, 3, 5, 2, 4)
        a = SlownessLayer.create_from_vlayer(vLayer, True)
        self.assertEqual(a.botP, 1268.0)
        self.assertEqual(a.botDepth, 31.0)
        b = SlownessLayer.create_from_vlayer(vLayer, False)
        self.assertEqual(b.topP, 3180.5)


if __name__ == '__main__':
    unittest.main(buffer=True)