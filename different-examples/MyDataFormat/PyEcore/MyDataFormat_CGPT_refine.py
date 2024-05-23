from pyecore.ecore import *
import math

# Initialize package
package = EPackage('geometry')

# Define abstract classes
Point = EClass('Point', abstract=True)
Orientation = EClass('Orientation', abstract=True)

# Define Point classes with documentation
Point2D = EClass('Point2D', superclass=[Point])
Point2D.eAnnotations.append(EAnnotation(source='documentation', details={'description': 'A 2D point in Cartesian coordinate space.'}))
Point3D = EClass('Point3D', superclass=[Point])

# Attributes with better defaults and comments
Point2D.x = EAttribute(eType=EFloat, name='x')
Point2D.y = EAttribute(eType=EFloat, name='y')
Point3D.x = EAttribute(eType=EFloat, name='x')
Point3D.y = EAttribute(eType=EFloat, name='y')
Point3D.z = EAttribute(eType=EFloat, name='z')

# Orientation classes
Orientation2D = EClass('Orientation2D', superclass=[Orientation])
Orientation3D = EClass('Orientation3D', superclass=[Orientation])

Orientation2D.z = EAttribute(eType=EFloat, name='z')
Orientation3D.x = EAttribute(eType=EFloat, name='x')
Orientation3D.y = EAttribute(eType=EFloat, name='y')
Orientation3D.z = EAttribute(eType=EFloat, name='z')

# Time and Date with validation
Time = EClass('Time')
Time.hour = EAttribute(eType=EInt, name='hour')
Time.minute = EAttribute(eType=EInt, name='minute')
Time.second = EAttribute(eType=EInt, name='second', lower=0, upper=1, defaultValue=None)

Date = EClass('Date')
Date.month = EAttribute(eType=EInt, name='month')
Date.day = EAttribute(eType=EInt, name='day')
Date.year = EAttribute(eType=EInt, name='year')

# List and Dictionary structures with advanced handling
List = EClass('List')
ListItem = EClass('ListItem')
NumberItem = EClass('NumberItem', superclass=[ListItem])
StringItem = EClass('StringItem', superclass=[ListItem])
BoolItem = EClass('BoolItem', superclass=[ListItem])

List.items = EReference(eType=ListItem, name='items', containment=True, upper=-1, ordered=True)

NumberItem.value = EAttribute(eType=EFloat, name='value')
StringItem.value = EAttribute(eType=EString, name='value')
BoolItem.value = EAttribute(eType=EBoolean, name='value')

Dict = EClass('Dict')
DictItem = EClass('DictItem')
Dict.items = EReference(eType=DictItem, name='items', containment=True, upper=-1)
DictItem.name = EAttribute(eType=EString, name='name')
DictItem.value = EReference(eType=EObject, name='value', containment=True)

# Adding custom methods for distance calculation
def distance_2d(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def distance_3d(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

Point2D.distance = classmethod(distance_2d)
Point3D.distance = classmethod(distance_3d)

# Register classes
package.eClassifiers.extend([Point, Point2D, Point3D, Orientation, Orientation2D, Orientation3D, Time, Date, List, ListItem, NumberItem, StringItem, BoolItem, Dict, DictItem])

# Save the model
with open('model.ecore', 'wb') as f:
    package.eResource.save(f)
