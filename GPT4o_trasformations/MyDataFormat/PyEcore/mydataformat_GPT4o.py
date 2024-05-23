from pyecore.ecore import EAttribute, EClass, EPackage, EReference, EString, EInt, EFloat, EBoolean
import sys

# Add the path where validator.py is located to the system path
sys.path.append(r'D:\Aristotelio\_0_Thesis\0_Github\5_TextX_PyEcore')

# Now you can import the validate_model function
from validator import validate_model


# Create the package
geometryPackage = EPackage(name='geometryPackage', nsURI='http://www.example.org/geometry', nsPrefix='geom')

# Create the 'Point' abstract class
Point = EClass('Point', abstract=True)
geometryPackage.eClassifiers.append(Point)

# Create the 'Point2D' class
Point2D = EClass('Point2D', superclass=[Point])
Point2D.eStructuralFeatures.append(EAttribute('x', EFloat))
Point2D.eStructuralFeatures.append(EAttribute('y', EFloat))
geometryPackage.eClassifiers.append(Point2D)

# Create the 'Point3D' class
Point3D = EClass('Point3D', superclass=[Point])
Point3D.eStructuralFeatures.append(EAttribute('x', EFloat))
Point3D.eStructuralFeatures.append(EAttribute('y', EFloat))
Point3D.eStructuralFeatures.append(EAttribute('z', EFloat))
geometryPackage.eClassifiers.append(Point3D)

# Create the 'Orientation' abstract class
Orientation = EClass('Orientation', abstract=True)
geometryPackage.eClassifiers.append(Orientation)

# Create the 'Orientation2D' class
Orientation2D = EClass('Orientation2D', superclass=[Orientation])
Orientation2D.eStructuralFeatures.append(EAttribute('z', EFloat))
geometryPackage.eClassifiers.append(Orientation2D)

# Create the 'Orientation3D' class
Orientation3D = EClass('Orientation3D', superclass=[Orientation])
Orientation3D.eStructuralFeatures.append(EAttribute('x', EFloat))
Orientation3D.eStructuralFeatures.append(EAttribute('y', EFloat))
Orientation3D.eStructuralFeatures.append(EAttribute('z', EFloat))
geometryPackage.eClassifiers.append(Orientation3D)

# Create the 'Time' class
Time = EClass('Time')
Time.eStructuralFeatures.append(EAttribute('hour', EInt))
Time.eStructuralFeatures.append(EAttribute('minute', EInt))
Time.eStructuralFeatures.append(EAttribute('second', EInt, default_value=None))
geometryPackage.eClassifiers.append(Time)

# Create the 'Date' class
Date = EClass('Date')
Date.eStructuralFeatures.append(EAttribute('month', EInt))
Date.eStructuralFeatures.append(EAttribute('day', EInt))
Date.eStructuralFeatures.append(EAttribute('year', EInt))
geometryPackage.eClassifiers.append(Date)

# Create the 'ListItem' abstract class
ListItem = EClass('ListItem', abstract=True)
geometryPackage.eClassifiers.append(ListItem)

# Create the 'List' class
List = EClass('List', superclass=[ListItem])
List.eStructuralFeatures.append(EReference('items', ListItem, upper=-1, containment=True))
geometryPackage.eClassifiers.append(List)

# Create the 'DictType' abstract class
DictType = EClass('DictType', abstract=True)
geometryPackage.eClassifiers.append(DictType)

# Create the 'Dict' class
Dict = EClass('Dict', superclass=[DictType])
Dict.eStructuralFeatures.append(EReference('items', ListItem, upper=-1, containment=True))
geometryPackage.eClassifiers.append(Dict)

# Create the 'DictItem' class
DictItem = EClass('DictItem')
DictItem.eStructuralFeatures.append(EAttribute('name', EString))
DictItem.eStructuralFeatures.append(EReference('value', DictType, containment=True))
geometryPackage.eClassifiers.append(DictItem)

# Define basic types
NUMBER = EClass('NUMBER', superclass=[ListItem, DictType])
NUMBER.eStructuralFeatures.append(EAttribute('value', EFloat))
geometryPackage.eClassifiers.append(NUMBER)

STRING = EClass('STRING', superclass=[ListItem, DictType])
STRING.eStructuralFeatures.append(EAttribute('value', EString))
geometryPackage.eClassifiers.append(STRING)

BOOL = EClass('BOOL', superclass=[ListItem, DictType])
BOOL.eStructuralFeatures.append(EAttribute('value', EBoolean))
geometryPackage.eClassifiers.append(BOOL)

# Define OBJECT class
OBJECT = EClass('OBJECT', superclass=[ListItem, DictType])
geometryPackage.eClassifiers.append(OBJECT)

# Example usage
# Create instances dynamically
Point2DInstance = Point2D()
Point2DInstance.x = 10.0
Point2DInstance.y = 20.0

Point3DInstance = Point3D()
Point3DInstance.x = 10.0
Point3DInstance.y = 20.0
Point3DInstance.z = 30.0

# Print out the values
print(f"Point2D: x={Point2DInstance.x}, y={Point2DInstance.y}")
print(f"Point3D: x={Point3DInstance.x}, y={Point3DInstance.y}, z={Point3DInstance.z}")

# Validate the model
diagnostics, metrics = validate_model(geometryPackage)

print("\nDiagnostics:")
for diagnostic in diagnostics:
    print(diagnostic)

print("\nMetrics:")
for key, value in metrics.items():
    print(f"{key}: {value}")