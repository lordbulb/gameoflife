import unittest
from gameoflife import *

class GameTest(unittest.TestCase):

    def testEmpty(self):
        self.game=Board()
        self.game.generation()
        self.assertEquals({},self.game.points)

    def testOneDies(self):
        self.game=Board()
        self.game.add_cell((1,1))
        self.game.generation()
        self.assertEquals({},self.game.points)

    def testBlock(self):
        self.game=Board()
        self.game.add_cell((1,1))
        self.game.add_cell((1,2))
        self.game.add_cell((2,1))
        self.game.add_cell((2,2))
        self.game.generation()
        self.game.generation()
        self.game.generation()
        self.assertEquals({(1,1):3,(1,2):3,(2,1):3,(2,2):3, },self.game.points)
        self.game.kill((1,1))
        self.game.generation()
        self.assertEquals({(1,1):3,(1,2):3,(2,1):3,(2,2):3, },self.game.points)

    def testBlockDies(self):
        self.game=Board()
        self.game.add_cell((1,1))
        self.game.add_cell((1,2))
        self.game.add_cell((2,1))
        self.game.add_cell((2,2))
        self.game.add_cell((0,1))
        self.game.generation()
        self.game.generation()
        self.game.generation()
        self.game.generation()
        self.assertEquals({},self.game.points)

    def testBlinker(self):
        self.game=Board()
        self.game.add_cell((0,0))
        self.game.add_cell((0,1))
        self.game.add_cell((0,2))
        self.game.generation()
        self.assertEquals({(0,1):2, (-1,1):1, (1,1):1},self.game.points)
        self.game.generation()
        self.assertEquals({(0,1):2, (0,0):1, (0,2):1},self.game.points)

class HexTest(unittest.TestCase):

    def testEmpty(self):
        self.game=Hexa_Board()
        self.game.generation()
        self.assertEquals({},self.game.points)

    def testOneDies(self):
        self.game=Hexa_Board()
        self.game.add_cell((1,1))
        self.game.generation()
        self.assertEquals({},self.game.points)

    def testBlock(self):
        self.game=Hexa_Board()
        self.game.add_cell((1,1))
        self.game.add_cell((1,2))
        self.game.add_cell((2,1))
        self.game.add_cell((2,2))
        self.game.generation()
        self.game.generation()
        self.game.generation()
        self.assertEquals({(1,1):3,(1,2):2,(2,1):2,(2,2):3, },self.game.points)
        self.game.kill((1,2))
        self.game.generation()
        self.assertEquals({(1,1):2,(2,1):2,(2,2):2, },self.game.points)

    def testBlockDies(self):
        self.game=Hexa_Board()
        self.game.add_cell((1,1))
        self.game.add_cell((1,2))
        self.game.add_cell((2,1))
        self.game.add_cell((2,2))
        self.game.add_cell((1,0))
        self.game.generation()
        self.game.generation()
        self.game.generation()
        self.assertEquals({},self.game.points)

    def testBlinker(self):
        self.game=Hexa_Board()
        self.game.add_cell((1,0))
        self.game.add_cell((2,1))
        self.game.add_cell((2,2))
        self.game.add_cell((3,0))
        self.game.generation()
        self.assertEquals({(2,0):1, (2,1):3, (3,1):1, (1,1):1},self.game.points)
        self.game.generation()
        self.assertEquals({(1,0):1, (2,1):3, (3,0):1, (2,2):1},self.game.points)

if __name__ == "__main__":
    unittest.main()
