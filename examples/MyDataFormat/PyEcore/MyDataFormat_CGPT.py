from pyecore.ecore import EObject, EClass, EAttribute, EReference, EInt, EFloat, EString, EBoolean, EPackage

# Package definition
package = EPackage('geometry')

# Abstract classes
Point = EClass('Point', abstract=True)
Orientation = EClass('Orientation', abstract=True)

# Derived classes for Points
Point2D = EClass('Point2D', superclass=[Point])
Point3D = EClass('Point3D', superclass=[Point])

# Attributes for Point2D
Point2D.x = EAttribute(eType=EFloat, name='x')
Point2D.y = EAttribute(eType=EFloat, name='y')

# Attributes for Point3D
Point3D.x = EAttribute(eType=EFloat, name='x')
Point3D.y = EAttribute(eType=EFloat, name='y')
Point3D.z = EAttribute(eType=EFloat, name='z')

# Derived classes for Orientations
Orientation2D = EClass('Orientation2D', superclass=[Orientation])
Orientation3D = EClass('Orientation3D', superclass=[Orientation])

# Attributes for Orientation2D
Orientation2D.z = EAttribute(eType=EFloat, name='z')

# Attributes for Orientation3D
Orientation3D.x = EAttribute(eType=EFloat, name='x')
Orientation3D.y = EAttribute(eType=EFloat, name='y')
Orientation3D.z = EAttribute(eType=EFloat, name='z')

# Classes for Time and Date
Time = EClass('Time')
Date = EClass('Date')

# Attributes for Time
Time.hour = EAttribute(eType=EInt, name='hour')
Time.minute = EAttribute(eType=EInt, name='minute')
Time.second = EAttribute(eType=EInt, name='second', lower=0, upper=1)  # Optional

# Attributes for Date
Date.month = EAttribute(eType=EInt, name='month')
Date.day = EAttribute(eType=EInt, name='day')
Date.year = EAttribute(eType=EInt, name='year')

# List and Dictionary structures
List = EClass('List')
Dict = EClass('Dict')
ListItem = EClass('ListItem')
DictItem = EClass('DictItem')

# List attributes
List.items = EReference(eType=ListItem, name='items', containment=True, upper=-1)

# ListItem choices (includes recursive references)
ListItem.value = EReference(eType=EObject, name='value', containment=True)

# Dict attributes
Dict.items = EReference(eType=DictItem, name='items', containment=True, upper=-1)

# DictItem attributes
DictItem.name = EAttribute(eType=EString, name='name')
DictItem.value = EReference(eType=EObject, name='value', containment=True)

# Registering classes in the package
package.eClassifiers.extend([Point, Point2D, Point3D, Orientation, Orientation2D, Orientation3D, Time, Date, List, Dict, ListItem, DictItem])

# Adding package to the global registry
EPackage.Registry[package.nsURI] = package

# Your PyEcore metamodel is now ready to be used for further modeling and generating instances.
with open('model.ecore', 'w') as f:
    package.eResource.save(f)