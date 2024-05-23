from pyecore.ecore import *

package = EPackage('helloworld')

class HelloWorldModel(EObject, metaclass=MetaEClass):
    abstract = True
    to_greet = EReference(upper=-1, containment=True)  # Do NOT set eType here

class Who(EObject, metaclass=MetaEClass):
    name = EAttribute(eType=EString)

package.eClassifiers.extend([HelloWorldModel, Who])

# NOW set the eType:
HelloWorldModel.to_greet.eType = Who 

# Example Usage
model = HelloWorldModel()
person1 = Who(name='Alice')
person2 = Who(name='Bob')
model.to_greet.extend([person1, person2])

for person in model.to_greet:
    print('Hello, ' + person.name + '!')

# Output:
# Hello, Alice!
# Hello, Bob!