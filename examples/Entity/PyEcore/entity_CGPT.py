from pyecore.ecore import EClass, EAttribute, EReference, EInt, EString, EPackage

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

# This code will output:
# Entity Name: Person
# Property Name: name, Type: string
# Property Name: age, Type: string

# Note: Additional functionality for serialization or further integration might require more configurations.
