#!/usr/bin/env python

##Copyright 2009 Thomas Paviot (tpaviot@gmail.com)
##
##This file is part of pythonOCC.
##
##pythonOCC is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##pythonOCC is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import sys
from OCC.Standard import *
from OCC.Utils.Topology import *
from OCC.BRepPrimAPI import *
from OCC.BRepBuilderAPI import *
from OCC.gp import *

class Test(unittest.TestCase):
    
    def testHash(self):
        '''
        Check whether the __hash__ function is equal to HashCode()
        '''
        print 'Test: __hash__ overloading'
        s = Standard_Transient()
        id_s = id(s)
        hash1_s = s.__hash__()
        hash2_s = s.HashCode(pow(2,31)-1)
        self.assertNotEqual(id_s, hash1_s)
        self.assertEqual(hash1_s,hash2_s)

    def testList(self):
        '''
        Test python lists features
        '''
        print 'Test: python lists'
        P1 = gp_Pnt(1,2,3)
        P2 = gp_Pnt(2,3,4)
        P3 = gp_Pnt(5,7,8)
        l = [P1,P2]
        self.assertEqual(P1 in l, True)
        self.assertNotEqual(P3 in l, True)
        self.assertEqual(l.index(P1),0)
        self.assertEqual(l.index(P2),1)
        # Do the same for Vertices (TopoDS_Shape has a HashCode() method overloaded
        V1 = BRepBuilderAPI_MakeVertex(P1).Vertex()
        V2 = BRepBuilderAPI_MakeVertex(P2).Vertex()
        V3 = BRepBuilderAPI_MakeVertex(P3) .Vertex()
        vl = [V1,V2]
        self.assertEqual(V1 in vl, True)
        self.assertNotEqual(V3 in vl, True)
        # index test()
        self.assertEqual(vl.index(V1),0)
        self.assertEqual(vl.index(V2),1)
        # reverse() test
        vl.reverse()
        self.assertEqual(vl.index(V1),1)
        self.assertEqual(vl.index(V2),0)
        
    def  testDict(self):
        '''
        Test python dict features
        '''
        print 'Test: python dicts'
        P1 = gp_Pnt(1,2,3)
        P2 = gp_Pnt(2,3,4)
        d={P1:'P1',P2:'P2'}
        self.assertEqual(d[P1]=='P1',True)
        self.assertEqual(d[P2]=='P2',True)

    def testTopology(self):
        '''
        Checks the Topology.py utility script.
        '''
        print 'Test: Topology'
        def get_shape():
            shape = BRepPrimAPI_MakeBox(10.,10.,10.).Shape()
            self.assertEqual(shape.IsNull(), False)
            topo = Topo(shape)
            return shape
        returned_shape = get_shape()
        self.assertEqual(returned_shape.IsNull(),False)
    
    def testFT1(self):
        '''
        Checks the Standard_Integer & byreference pass parameter
        '''
        print 'Test: Standard_Integer & by reference transformator'
        from OCC.gp import gp_Pnt
        P = gp_Pnt(1,2,3.2)
        self.assertEqual(P.Coord(),(1,2,3.2))
          
    def testStandardIntegerByRefPassedReturned(self):
        '''
        Checks the Standard_Integer & byreference return parameter
        '''
        print 'Test: Standard_Integer & by reference transformator'
        from OCC.ShapeFix import ShapeFix_Solid
        sfs = ShapeFix_Solid()
        sfs.SetFixShellMode(5)
        self.assertEqual(sfs.GetFixShellMode(),5)
        
    def testStandardBooleanByRefPassedReturned(self):
        '''
        Checks the Standard_Boolean & byreference return parameter
        '''
        print 'Test: Standard_Boolean & by reference transformator'
        from OCC.ShapeFix import ShapeFix_Wire
        sfw = ShapeFix_Wire()
        sfw.SetModifyGeometryMode(True)
        self.assertEqual(sfw.GetModifyGeometryMode(),True)
        sfw.SetModifyGeometryMode(False)
        self.assertEqual(sfw.GetModifyGeometryMode(),False)
    
    def testSTLVectorInt(self):
        '''
        Checks the IntVector and DoubleVector classes that are used in the StdMeshers
        module
        '''
        from OCC.StdMeshers import IntVector, StdMeshers_FixedPoints1D
        # The IntVector must be initialized from a list/tuple of integers
        i_v = IntVector([1,2,3,4])
        self.assertEqual(i_v[0],1)
        self.assertEqual(i_v[1],2)
        self.assertEqual(i_v[2],3)
        self.assertEqual(i_v[3],4)
        # If at least one item of the list is not an integer, raise an exception
        self.assertRaises(TypeError,IntVector,[1,2,3,4.0])
        # Test one method of StdMeshers that takes/returns such a parameter type
        from OCC.SMESH import SMESH_Gen
        fixed_points = StdMeshers_FixedPoints1D(1,2,SMESH_Gen())
        fixed_points.SetReversedEdges([1,2,3])
        self.assertEquals(fixed_points.GetReversedEdges(),(1,2,3))
        
    def testSTLVectorDouble(self):
        '''
        Checks the IntVector and DoubleVector classes that are used in the StdMeshers
        module
        '''
        from OCC.StdMeshers import IntVector, StdMeshers_FixedPoints1D
        # The IntVector must be initialized from a list/tuple of floats/integers. Integers will
        # be converted to floats
        d_v = DoubleVector([1.0,2,3.0,4])
        self.assertEqual(d_v[0],1.0)
        self.assertEqual(d_v[1],2.0)
        self.assertEqual(d_v[2],3.0)
        self.assertEqual(d_v[3],4.0)
        # If at least one item of the list is not an float or an integer, raise an exception
        self.assertRaises(TypeError,DoubleVector,[1.0,2.0,3.0,"string"])
        # Test one method of StdMeshers that takes/returns such a parameter type
        from OCC.SMESH import SMESH_Gen
        fixed_points = StdMeshers_FixedPoints1D(1,2,SMESH_Gen())
        fixed_points.SetPoints([1.0,3.0,4.0])
        self.assertEquals(fixed_points.GetPoints(),(1.0,3.0,4.0))
          
    def testDumpToString(self):
        '''
        Checks if the pickle python module works for TopoDS_Shapes
        '''
        print 'Test: pickling of TopoDS_Shapes'
        from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox
        import pickle
        # Create the shape
        box_shape = BRepPrimAPI_MakeBox(100,200,300).Shape()
        pickle.dumps(box_shape)

if __name__ == "__main__":
    unittest.main()
    
