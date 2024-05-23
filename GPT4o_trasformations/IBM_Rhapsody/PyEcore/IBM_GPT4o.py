from pyecore.ecore import EAttribute, EClass, EPackage, EReference, EString, EDouble, EObject
import sys

# Add the path where validator.py is located to the system path
sys.path.append(r'D:\Aristotelio\_0_Thesis\0_Github\5_TextX_PyEcore')

# Now you can import the validate_model function
from validator import validate_model

# Define the package
package_name = 'rhapsodyMM'
namespace_uri = 'http://www.example.org/rhapsody'
namespace_prefix = 'rh'

RhapsodyPackage = EPackage(name=package_name, nsURI=namespace_uri, nsPrefix=namespace_prefix)

# Create the 'RhapsodyModel' class
RhapsodyModel = EClass('RhapsodyModel')
header = EAttribute('header', EString, default_value="Default Header")
RhapsodyModel.eStructuralFeatures.append(header)

# Create the 'Object' class
Object = EClass('Object')
obj_name = EAttribute('name', EString, default_value="UnnamedObject")
Object.eStructuralFeatures.append(obj_name)

# Create the 'Property' class
Property = EClass('Property')
prop_name = EAttribute('name', EString, default_value="UnnamedProperty")
Property.eStructuralFeatures.append(prop_name)

# Define the 'Value' class and its subclasses
Value = EClass('Value', abstract=True)
StringValue = EClass('StringValue', superclass=(Value,))
string_value = EAttribute('value', EString, default_value="")
StringValue.eStructuralFeatures.append(string_value)

NumberValue = EClass('NumberValue', superclass=(Value,))
number_value = EAttribute('value', EDouble, default_value=0.0)
NumberValue.eStructuralFeatures.append(number_value)

GUIDValue = EClass('GUIDValue', superclass=(Value,))
guid_value = EAttribute('value', EString, default_value="")
GUIDValue.eStructuralFeatures.append(guid_value)

IDValue = EClass('IDValue', superclass=(Value,))
id_value = EAttribute('value', EString, default_value="")
IDValue.eStructuralFeatures.append(id_value)

# Set the type of 'values' reference in 'Property' to 'Value'
values = EReference('values', Value, upper=-1, containment=True)
Property.eStructuralFeatures.append(values)

# Relate 'properties' in 'Object' to 'Property' class
properties = EReference('properties', Property, upper=-1, containment=True, opposite='object')
Property.eStructuralFeatures.append(EReference('object', Object, opposite=properties))
Object.eStructuralFeatures.append(properties)

# Relate 'children' in 'Object' to 'Object' class
children = EReference('children', Object, upper=-1, containment=True, opposite='parent')
Object.eStructuralFeatures.append(EReference('parent', Object, opposite=children))
Object.eStructuralFeatures.append(children)

# Add root reference in 'RhapsodyModel' to 'Object'
root = EReference('root', Object, containment=True)
RhapsodyModel.eStructuralFeatures.append(root)

# Add classes to the package
RhapsodyPackage.eClassifiers.extend([
    RhapsodyModel, Object, Property, Value,
    StringValue, NumberValue, GUIDValue, IDValue
])

# Example Usage
model = RhapsodyModel(header="Sample Header")
root_object = Object(name="RootObject")
model.root = root_object

prop1 = Property(name="prop1")
str_value = StringValue(value="Hello")
prop1.values.append(str_value)
root_object.properties.append(prop1)

# Add nested Object
child_object = Object(name="ChildObject")
root_object.children.append(child_object)

# Add property to child object
child_prop = Property(name="childProp")
num_value = NumberValue(value=123.456)
child_prop.values.append(num_value)
child_object.properties.append(child_prop)

# Verify the structure
print(f"Model header: {model.header}")
print(f"Root object name: {model.root.name}")
print(f"Root object properties: {[(p.name, [v.value for v in p.values]) for p in model.root.properties]}")
print(f"Root object children: {[(child.name, [(p.name, [v.value for v in p.values]) for p in child.properties]) for child in model.root.children]}")

# Validate the model
diagnostics, metrics = validate_model(RhapsodyPackage)

print("\nDiagnostics:")
for diagnostic in diagnostics:
    print(diagnostic)

print("\nMetrics:")
for key, value in metrics.items():
    print(f"{key}: {value}")
