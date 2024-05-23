from pyecore.ecore import EClass, EAttribute, EReference, EPackage, EString, EFloat, EBoolean
import sys

# Add the path where validator.py is located to the system path
sys.path.append(r'D:\Aristotelio\_0_Thesis\0_Github\5_TextX_PyEcore')

# Now you can import the validate_model function
from validator import validate_model

# Create the package
JSONPackage = EPackage('JSONPackage', nsURI='http://www.example.org/json', nsPrefix='json')

# Define the EClasses
File = EClass('File')
JSONPackage.eClassifiers.append(File)

Array = EClass('Array')
JSONPackage.eClassifiers.append(Array)

Value = EClass('Value')
JSONPackage.eClassifiers.append(Value)

Object = EClass('Object')
JSONPackage.eClassifiers.append(Object)

Member = EClass('Member')
JSONPackage.eClassifiers.append(Member)

# Define the attributes
STRING = EAttribute('STRING', EString)
FLOAT = EAttribute('FLOAT', EFloat)
BOOL = EAttribute('BOOL', EBoolean)

Value.eStructuralFeatures.extend([STRING, FLOAT, BOOL])

# Define the references
values = EReference('values', Value, upper=-1, containment=True)
Array.eStructuralFeatures.append(values)

members = EReference('members', Member, upper=-1, containment=True)
Object.eStructuralFeatures.append(members)

key = EAttribute('key', EString)
value = EReference('value', Value, containment=True)
Member.eStructuralFeatures.extend([key, value])

# File can contain either an Array or an Object
File.eStructuralFeatures.extend([
    EReference('array', Array, containment=True, upper=1),
    EReference('object', Object, containment=True, upper=1)
])

# Example usage
example_file = File()
example_object = Object()
example_member = Member(key="name", value=Value(STRING="John Doe"))
example_object.members.append(example_member)
example_file.object = example_object

# Print out the JSON structure
for member in example_file.object.members:
    print(f"Key: {member.key}, Value: {member.value.STRING}")

# Validate the model
diagnostics, metrics = validate_model(JSONPackage)

print("\nDiagnostics:")
for diagnostic in diagnostics:
    print(diagnostic)

print("\nMetrics:")
for key, value in metrics.items():
    print(f"{key}: {value}")
