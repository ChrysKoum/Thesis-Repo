from pyecore.ecore import EEnum, EAttribute, EClass, EReference, EDataType

# Importing required datatypes
from datetime import time, date

# Defining Enum for Orientation
class Orientation(EEnum):
    ORIENTATION_2D = 0
    ORIENTATION_3D = 1

# Define the metamodel classes
class Point(EClass):
    pass

class Point2D(Point):
    x = EAttribute(eType=EDataType('float'))
    y = EAttribute(eType=EDataType('float'))

class Point3D(Point):
    x = EAttribute(eType=EDataType('float'))
    y = EAttribute(eType=EDataType('float'))
    z = EAttribute(eType=EDataType('float'))

class OrientationType(EClass):
    pass

class Orientation2D(OrientationType):
    z = EAttribute(eType=EDataType('float'))

class Orientation3D(OrientationType):
    x = EAttribute(eType=EDataType('float'))
    y = EAttribute(eType=EDataType('float'))
    z = EAttribute(eType=EDataType('float'))

class Time(EDataType):
    hour = EAttribute(eType=EDataType('int'))
    minute = EAttribute(eType=EDataType('int'))
    second = EAttribute(eType=EDataType('int'), default_value=0)

class Date(EDataType):
    month = EAttribute(eType=EDataType('int'))
    day = EAttribute(eType=EDataType('int'))
    year = EAttribute(eType=EDataType('int'))

class List(EDataType):
    items = EAttribute(eType=EDataType('list'))

class ListItem(EDataType):
    value = EAttribute(eType=EDataType('object'))

class Dict(EDataType):
    items = EAttribute(eType=EDataType('dict'))

class DictItem(EDataType):
    name = EAttribute(eType=EDataType('str'))
    value = EReference(ordered=False, unique=True)

class DictType(EDataType):
    pass

# Creating the metamodel package
from pyecore.ecore import EPackage, EClassifier, EReference
from pyecore.resources import ResourceSet
from pyecore.resources import URI

Point.eSubpackages.append(OrientationType)
OrientationType.eSubpackages.append(Date)
Date.eSubpackages.append(List)
List.eSubpackages.append(Dict)
Dict.eSubpackages.append(DictType)

package = EPackage('MyPackage')
package.eSubpackages.append(Point)
package.eSubpackages.append(Time)

package


# Use this package like:
# rset = ResourceSet()
# rset.append(package)
# myinstance = package.Point2D()
# myinstance.x = 10.0
# myinstance.y = 20.0
# # ...
