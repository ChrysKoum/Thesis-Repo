from pyecore.ecore import EObject, EClass, EAttribute, EReference, EString
from pyecore.ecore import EPackage

# Define the EPackage
hello_world_package = EPackage(name='hello_world_package', nsURI='http://www.example.org/hello_world', nsPrefix='hello_world')

# Define the EClasses
HelloWorldModel = EClass('HelloWorldModel')
Who = EClass('Who')

# Add EClasses to the EPackage
hello_world_package.eClassifiers.append(HelloWorldModel)
hello_world_package.eClassifiers.append(Who)

# Define attributes and references
to_greet = EReference('to_greet', Who, upper=-1, containment=True)
name = EAttribute('name', EString, lower=1)

# Add attributes and references to EClasses
HelloWorldModel.eStructuralFeatures.append(to_greet)
Who.eStructuralFeatures.append(name)

# Optionally: Creating dynamic instances to test the setup
model = HelloWorldModel()
person1 = Who(name="Alice")
person2 = Who(name="Bob")
model.to_greet.extend([person1, person2])

print(f"Model greeting: {[person.name for person in model.to_greet]}")
