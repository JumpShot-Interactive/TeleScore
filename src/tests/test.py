"""
Developed By: JumpShot Team
Written by: riscyseven
"""

import sys
import os

from unittest.mock import PropertyMock, patch
from PyQt6.QtWidgets import QApplication, QWidgetItem, QPushButton
from PyQt6.QtCore import QSize
import unittest 
import requests
import time

from layout.abstract_layout.freelayout import FreeLayout
from component.basiccomp.buttoncomp import ButtonComp
from component.element.clock import Clock
from property.property import Property

# Note, these tests might be seperated into different classes in the future.

class gm_resourcetest(unittest.TestCase):
    '''@classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass'''

    def test_retrieveFile(self):
        '''with patch("gm_resources.requests.get") as mocked_get:
            rtn = requests.Response()
            rtn.status_code = 200
            type(rtn).content = "Hello World"
            type(rtn).text = "Hello World"
            type(rtn).ok = True
            mocked_get.return_value = rtn
            print(mocked_get.return_value)
            rtnVal = gm_resources.retrieveFile("https://www.example.com", "Hello")
            #print(rtnVal)
            #self.assertEqual(rtnVal, "Hello World")'''
        pass

class freelayout_test(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.layoutInst = FreeLayout(None)

    def tearDown(self):
        pass

    def test_count(self):
        self.assertEqual(self.layoutInst.count(), 0)
        widgetInst = QPushButton()
        itemInst = QWidgetItem(widgetInst)
        self.layoutInst.addItem(itemInst)

        self.assertEqual(self.layoutInst.count(), 1)

    def test_addItem(self):
        widgetInst = QPushButton()
        itemInst = QWidgetItem(widgetInst)
        self.layoutInst.addItem(itemInst)

        self.assertEqual(self.layoutInst.itemAt(0), itemInst)

    def test_indexOf(self):
        widgetInst = QPushButton()
        itemInst = QWidgetItem(widgetInst)
        self.layoutInst.addItem(itemInst)

        widgetInst1 = QPushButton()
        itemInst1 = QWidgetItem(widgetInst1)
        self.layoutInst.addItem(itemInst1)

        self.assertEqual(self.layoutInst.indexOf(itemInst), 0)
        self.assertEqual(self.layoutInst.indexOf(itemInst1), 1)

    def test_itemAt(self):
        widgetInst = QPushButton()
        itemInst = QWidgetItem(widgetInst)
        self.layoutInst.addItem(itemInst)

        widgetInst1 = QPushButton()
        itemInst1 = QWidgetItem(widgetInst1)
        self.layoutInst.addItem(itemInst1)

        self.assertEqual(self.layoutInst.itemAt(0), itemInst)
        self.assertEqual(self.layoutInst.itemAt(1), itemInst1) 

    def test_spacing(self):
        self.assertEqual(self.layoutInst.spacing(), -1)

    def test_setSpacing(self):
        self.assertEqual(self.layoutInst.spacing(), -1)
        self.layoutInst.setSpacing(2)
        self.assertEqual(self.layoutInst.spacing(), 2)

    def test_takeAt(self):
        widgetInst = ButtonComp("test")
        self.layoutInst.addComponent(widgetInst, QSize(700, 600))

        self.assertEqual(self.layoutInst.count(), 1)

        self.layoutInst.takeAt(0)

        self.assertEqual(self.layoutInst.count(), 0)
        
class clockelement_test(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.clock = Clock()

    def tearDown(self):
        pass

    def test_timer(self):
        pass
        #self.clock.setClockTick(5000) # 5 seconds
        #self.clock.startClock()

        #time.sleep(2)

        #self.clock.stopClock()
        #print(self.clock.getTick())

class property_test(unittest.TestCase):
    testProperty1 = {
        "test1_prop": {
            "TYPE": "TEXTEDIT",
            "VALUE": "Hello World"
        },
    }
    testProperty2 = {
        "test2_prop": {
            "TYPE": "NUMEDIT",
            "VALUE": "Hi World"
        },
    }

    def setUp(self):
        self.app = QApplication([])
        self.property = Property()

    def test_appendPropHead(self):
        self.assertEqual(len(self.property.getList()), 0)
        self.property.appendPropHead("test1", self.testProperty1)
        self.assertEqual(len(self.property.getList()), 1)
        self.assertEqual(self.property.getValue("test1_prop"), "Hello World")

    def test_removeProperty(self):
        self.property.appendPropHead("test1", self.testProperty1)
        self.property.appendPropHead("test2", self.testProperty2)
        self.assertEqual(len(self.property.getList()), 2)
        self.assertEqual(self.property.getValue("test2_prop"), "Hi World")
        self.property.removeProperty("test2")

        self.assertEqual(len(self.property.getList()), 1)
        self.assertEqual(self.property.getValue("test2_prop"), None)
        self.assertEqual(self.property.getValue("test1_prop"), "Hello World")

    def test_getValue(self):
        self.property.appendPropHead("test1", self.testProperty1)
        self.assertEqual(self.property.getValue("test1_prop"), "Hello World")

    def test_changeValue(self):
        self.property.appendPropHead("test1", self.testProperty1)
        self.assertEqual(self.property.getValue("test1_prop"), "Hello World")
        self.property.changeValue("test1_prop", "1")
        self.assertEqual(self.property.getValue("test1_prop"), "1")

        dictInst = self.property.getList()
        dictInst2 = self.property.getAll()

        self.assertEqual(dictInst["test1"]["PROPERTIES"]["test1_prop"]["VALUE"], "1")
        self.assertEqual(dictInst2["test1_prop"]["VALUE"], "1")



if __name__ == '__main__':
    unittest.main()
