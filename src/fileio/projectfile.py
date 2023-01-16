"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from json import load, dump
from copy import deepcopy

from attr import PropInstType, CompAttr, ProjAttr
from component.compfactory import CompFactory
from component.tabcomp import TabComp
from abstract.abstractfile import AbstractFile

class ProjectFile(AbstractFile):
    def __init__(self, project):
        self.project = project

    def convConn(self, conn):
        tempConn = {}
        for typeName in conn:
            newList = []
            connCompList = conn[typeName]
            for comp in connCompList:
                name = comp.objectName()
                newList.append(name)
            tempConn[typeName] = newList
        return tempConn
        
    
    # Override
    def save(self):
        json = {}
        projProp = deepcopy(self.project.getProperty().getAllPropDict())
        projProp["FN"].setValue("")
        json[ProjAttr.HEADER] = self.convProptoDict(projProp)

        los = []

        for tabcomp in self.project.getAllLO().values():
            tempLO = {}
            tempLO[CompAttr.Property] = self.convProptoDict(tabcomp.getProperty().getAllPropDict())
            lo = tabcomp.getLayout()

            tempComps = []
            for comp in lo.getLOComp():
                tempComp = {}
                tempComp[PropInstType.TYPE] = comp.getName()
                
                tempComp[CompAttr.Property] = self.convProptoDict(comp.getProperty().getAllPropDict())
                tempComp[CompAttr.CONN] = self.convConn(comp.getConnection().getData()[0])
                tempComps.append(tempComp)

            tempLO[ProjAttr.COMPONENTS] = tempComps

            los.append(tempLO)

        json[ProjAttr.LAYOUTS] = los

        with open(self.project.getFileName(), "w") as f:
            dump(json, f)


    # Override
    def load(self):
        json = {}
        nameConn = {}
        with open(self.project.getFileName(), "r") as f:
            json = load(f)
        
        projProp = self.project.getProperty()
        self.convDicttoProp(json[str(ProjAttr.HEADER)], projProp)

        for lo in json[str(ProjAttr.LAYOUTS)]:
            tempLO = TabComp(self.project, lo[str(CompAttr.Property)]["Component Name"])
            self.convDicttoProp(lo[str(CompAttr.Property)], tempLO.getProperty())

            for comp in lo[str(ProjAttr.COMPONENTS)]:
                component = CompFactory.makeComponent(self.project,
                 comp[str(PropInstType.TYPE)],
                  comp[str(CompAttr.Property)]["Component Name"], tempLO.getLayout())

                self.convDicttoProp(comp[str(CompAttr.Property)], component.getProperty())

                nameConn[component.objectName()] = comp[str(CompAttr.CONN)]
                tempLO.getLayout().addComponent(component)
                component.propChanged()
            
            tempLO.propChanged()
            self.project.addLO(tempLO.objectName(), tempLO)
        self.connect(nameConn)


    def connect(self, nameConn: dict):
        for name, connJson in nameConn.items():
            comp = self.project.getComp(name)
            conn = comp.getConnection()

            for signal in connJson:
                conn.appendConnType(signal)
                for receiver in connJson[signal]:
                    conn.appendConn(signal, self.project.getComp(receiver))

        

        
