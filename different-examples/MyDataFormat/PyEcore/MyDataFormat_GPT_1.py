from pyecore.ecore import EObject, EClass, EAttribute, EReference, EInt, EFloat, EString, EBoolean

# Abstract classes for Point and Orientation using EClass
Point = EClass('Point', abstract=True)
Point2D = EClass('Point2D', superclass=[Point])
Point3D = EClass('Point3D', superclass=[Point])

Orientation = EClass('Orientation', abstract=True)
Orientation2D = EClass('Orientation2D', superclass=[Orientation])
Orientation3D = EClass('Orientation3D', superclass=[Orientation])

# Adding attributes to classes
Point2D.eStructuralFeatures.append(EAttribute('x', EFloat))
Point2D.eStructuralFeatures.append(EAttribute('y', EFloat))
Point3D.eStructuralFeatures.append(EAttribute('x', EFloat))
Point3D.eStructuralFeatures.append(EAttribute('y', EFloat))
Point3D.eStructuralFeatures.append(EAttribute('z', EFloat))
Orientation2D.eStructuralFeatures.append(EAttribute('z', EFloat))
Orientation3D.eStructuralFeatures.append(EAttribute('x', EFloat))
Orientation3D.eStructuralFeatures.append(EAttribute('y', EFloat))
Orientation3D.eStructuralFeatures.append(EAttribute('z', EFloat))

# Define the Time and Date classes
Time = EClass('Time')
Time.eStructuralFeatures.extend([
    EAttribute('hour', EInt),
    EAttribute('minute', EInt),
    EAttribute('second', EInt, lower=0, upper=1)  # Optional
])

Date = EClass('Date')
Date.eStructuralFeatures.extend([
    EAttribute('month', EInt),
    EAttribute('day', EInt),
    EAttribute('year', EInt)
])

# Define the List and Dict classes for recursive structures
List = EClass('List')
ListItem = EClass('ListItem')
Dict = EClass('Dict')
DictItem = EClass('DictItem')

List.eStructuralFeatures.append(EReference('items', ListItem, containment=True, upper=-1))
Dict.eStructuralFeatures.append(EReference('items', DictItem, containment=True, upper=-1))
DictItem.eStructuralFeatures.append(EAttribute('name', EString))
DictItem.eStructuralFeatures.append(EReference('value', ListItem))  # Assuming ListItem can be any type

# Final adjustments and connections
ListItem.eStructuralFeatures.extend([
    EAttribute('number', EFloat),
    EAttribute('integer', EInt),
    EAttribute('string', EString),
    EAttribute('boolean', EBoolean),
    EReference('list', List),
    EReference('dict', Dict),
    EReference('object', EObject)  # Placeholder for specific types
])
