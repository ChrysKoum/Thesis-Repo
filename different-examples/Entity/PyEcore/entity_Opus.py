from pyecore.ecore import EAttribute, EClass, EObject, EPackage, EString, EReference

# Create the package
EntityPackage = EPackage(name='entityPackage', nsURI='http://www.example.org/entity', nsPrefix='entity')

# Create the 'Type' class as an abstract class
Type = EClass('Type', abstract=True)
EntityPackage.eClassifiers.append(Type)

# Create the 'SimpleType' class, inheriting from 'Type'
SimpleType = EClass('SimpleType')
SimpleType.eSuperTypes.append(Type)  # Correct inheritance setting
name_simple = EAttribute('name', EString)
SimpleType.eStructuralFeatures.append(name_simple)
EntityPackage.eClassifiers.append(SimpleType)

# Create the 'Entity' class, inheriting from 'Type'
Entity = EClass('Entity')
Entity.eSuperTypes.append(Type)  # Correct inheritance setting
name_entity = EAttribute('name', EString)
Entity.eStructuralFeatures.append(name_entity)

# Create the 'Property' class
Property = EClass('Property')
name_prop = EAttribute('name', EString)
type_prop = EReference('type', Type)  # Correct reference to EClass Type
Property.eStructuralFeatures.extend([name_prop, type_prop])
EntityPackage.eClassifiers.append(Property)

# Add properties reference after Property class is defined
properties = EReference('properties', Property, upper=-1, containment=True)
Entity.eStructuralFeatures.append(properties)
EntityPackage.eClassifiers.append(Entity)

# Create the 'EntityModel' class
EntityModel = EClass('EntityModel')
types = EReference('types', SimpleType, upper=-1, containment=True)
entities = EReference('entities', Entity, upper=-1, containment=True)
EntityModel.eStructuralFeatures.extend([types, entities])
EntityPackage.eClassifiers.append(EntityModel)

# Usage example
model = EntityModel()

string_type = SimpleType(name='string')
integer_type = SimpleType(name='integer')
model.types.extend([string_type, integer_type])

person = Entity(name='Person')
name_prop = Property(name='name', type=string_type)
age_prop = Property(name='age', type=integer_type)
person.properties.extend([name_prop, age_prop])

address = Entity(name='Address')
street_prop = Property(name='street', type=string_type)
city_prop = Property(name='city', type=string_type)
country_prop = Property(name='country', type=string_type)
address.properties.extend([street_prop, city_prop, country_prop])

model.entities.extend([person, address])

# Print the model
for entity in model.entities:
    print(f"Entity: {entity.name}")
    for prop in entity.properties:
        print(f"  Property: {prop.name} : {prop.type.name}")