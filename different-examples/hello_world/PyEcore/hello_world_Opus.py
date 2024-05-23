from pyecore.ecore import *

class HelloWorldModel(EObject):
    to_greet = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, to_greet=None):
        super().__init__()
        if to_greet:
            self.to_greet.extend(to_greet)

class Who(EObject):
    name = EAttribute(eType=EString)

    def __init__(self, name=None):
        super().__init__()
        if name:
            self.name = name

HelloWorldModel.to_greet.eType = Who

# Create instances
hello_world = HelloWorldModel()
who1 = Who(name="Alice")
who2 = Who(name="Bob")

# Add Who instances to HelloWorldModel
hello_world.to_greet.extend([who1, who2])

# Print the model
print("HelloWorldModel:")
for who in hello_world.to_greet:
    print("- Name:", who.name)