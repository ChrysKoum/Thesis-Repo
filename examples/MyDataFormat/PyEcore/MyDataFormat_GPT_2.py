from pyecore.ecore import EObject, EClass, EAttribute, EReference, EInt, EString, EFloat, EBoolean
from pyecore.ecore import EPackage

# Define the EPackage
package = EPackage('textx_metamodel')

# Base class for generic objects
class GenericObject(EObject):
    pass

# Point class hierarchy
Point = EClass('Point')
Point2D = EClass('Point2D', superclass=[Point])
Point2D.eStructuralFeatures.append(EAttribute('x', EFloat))
Point2D.eStructuralFeatures.append(EAttribute('y', EFloat))
Point3D = EClass('Point3D', superclass=[Point])
Point3D.eStructuralFeatures.append(EAttribute('x', EFloat))
Point3D.eStructuralFeatures.append(EAttribute('y', EFloat))
Point3D.eStructuralFeatures.append(EAttribute('z', EFloat))

# Orientation class hierarchy
Orientation = EClass('Orientation')
Orientation2D = EClass('Orientation2D', superclass=[Orientation])
Orientation2D.eStructuralFeatures.append(EAttribute('z', EFloat))
Orientation3D = EClass('Orientation3D', superclass=[Orientation])
Orientation3D.eStructuralFeatures.append(EAttribute('x', EFloat))
Orientation3D.eStructuralFeatures.append(EAttribute('y', EFloat))
Orientation3D.eStructuralFeatures.append(EAttribute('z', EFloat))

# Time and Date classes
Time = EClass('Time')
Time.eStructuralFeatures.append(EAttribute('hour', EInt))
Time.eStructuralFeatures.append(EAttribute('minute', EInt))
Time.eStructuralFeatures.append(EAttribute('second', EInt, lower=0, upper=1, default_value=None))

Date = EClass('Date')
Date.eStructuralFeatures.append(EAttribute('month', EInt))
Date.eStructuralFeatures.append(EAttribute('day', EInt))
Date.eStructuralFeatures.append(EAttribute('year', EInt))

# List and Dictionary structures
List = EClass('List')
List.eStructuralFeatures.append(EReference('items', GenericObject, containment=True, upper=-1))

Dict = EClass('Dict')
Dict.eStructuralFeatures.append(EReference('items', EClass('DictItem'), containment=True, upper=-1))

DictItem = EClass('DictItem')
DictItem.eStructuralFeatures.append(EAttribute('name', EString))
DictItem.eStructuralFeatures.append(EReference('value', GenericObject, containment=True))

# Add classes to package
package.eClassifiers.extend([Point, Point2D, Point3D, Orientation, Orientation2D, Orientation3D, Time, Date, List, Dict, DictItem, GenericObject])

# Generate and compile the metamodel
package._ecore = True
