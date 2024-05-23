import sys

# Add the path where validator.py is located to the system path
sys.path.append(r'D:\Aristotelio\_0_Thesis\0_Github\5_TextX_PyEcore')

# Now you can import the validate_model function
from validator import validate_model

from pyecore.ecore import EClass, EAttribute, EPackage, EString, EReference

# Create the package
HelloWorldPackage = EPackage(name='helloWorldPackage', nsURI='http://www.example.org/hello', nsPrefix='hello')

# Create the 'Who' class
Who = EClass('Who')
HelloWorldPackage.eClassifiers.append(Who)

# Create the 'name' attribute in 'Who'
name = EAttribute('name', EString, default_value="Unnamed")
Who.eStructuralFeatures.append(name)

# Create the 'HelloWorldModel' class
HelloWorldModel = EClass('HelloWorldModel')
HelloWorldPackage.eClassifiers.append(HelloWorldModel)

# Create the 'to_greet' reference in 'HelloWorldModel'
to_greet = EReference('to_greet', Who, upper=-1, containment=True)
HelloWorldModel.eStructuralFeatures.append(to_greet)
# Create instances
model = HelloWorldModel()
who1 = Who(name="World")
who2 = Who(name="Solar System")
who3 = Who(name="Universe")

# Add instances to the model
model.to_greet.extend([who1, who2, who3])

# Print the names to show default value usage
for person in model.to_greet:
    print(f"Greeting {person.name}!")
# Validate the model
diagnostics, metrics = validate_model(HelloWorldPackage)

print("\nDiagnostics:")
for diagnostic in diagnostics:
    print(diagnostic)

print("\nMetrics:")
for key, value in metrics.items():
    print(f"{key}: {value}")
