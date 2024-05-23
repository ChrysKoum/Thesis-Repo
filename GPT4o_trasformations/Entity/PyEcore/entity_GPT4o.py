import sys

# Add the path where validator.py is located to the system path
sys.path.append(r'D:\Aristotelio\_0_Thesis\0_Github\5_TextX_PyEcore')

# Now you can import the validate_model function
from validator import validate_model

from pyecore.ecore import EClass, EAttribute, EReference, EString, EPackage

# Create the EPackage with the specified namespace URI and prefix
entity_model_package = EPackage(name='EntityModelPackage', nsURI='http://www.example.org/entitymodel', nsPrefix='entitymodel')

# EClass definitions
SimpleType = EClass('SimpleType')
Entity = EClass('Entity')
Property = EClass('Property')
Type = EClass('Type', abstract=True)  # Abstract as it's a base for SimpleType and Entity

# Adding EClass to the package
entity_model_package.eClassifiers.extend([SimpleType, Entity, Property, Type])

# Attributes
simple_type_name = EAttribute('name', EString)
SimpleType.eStructuralFeatures.append(simple_type_name)

entity_name = EAttribute('name', EString)
Entity.eStructuralFeatures.append(entity_name)

property_name = EAttribute('name', EString)
Property.eStructuralFeatures.append(property_name)

# References
properties = EReference('properties', Property, upper=-1, containment=True)
Entity.eStructuralFeatures.append(properties)

property_type = EReference('type', Type)  # Unidirectional reference
Property.eStructuralFeatures.append(property_type)

# Inheritance
SimpleType.eSuperTypes.append(Type)
Entity.eSuperTypes.append(Type)

# Example of instantiation and usage:
# Creating an instance of Entity and SimpleType
entity_example = Entity(name="Person")
simple_type_example = SimpleType(name="string")

# Creating properties
property_name = Property(name="name", type=simple_type_example)
property_age = Property(name="age", type=simple_type_example)

# Adding properties to the entity
entity_example.properties.extend([property_name, property_age])

# Example usage of the model
print(f"Entity Name: {entity_example.name}")
for prop in entity_example.properties:
    print(f"Property Name: {prop.name}, Type: {prop.type.name}")

# Validate the model
diagnostics, metrics = validate_model(entity_model_package)

print("\nDiagnostics:")
for diagnostic in diagnostics:
    print(diagnostic)

print("\nMetrics:")
for key, value in metrics.items():
    print(f"{key}: {value}")
