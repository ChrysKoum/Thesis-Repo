from pyecore.ecore import EAttribute, EClass, EObject, EPackage, EString, EReference

# Create the package
HelloWorldPackage = EPackage(name='helloWorldPackage', nsURI='http://www.example.org/hello', nsPrefix='hello')

# Create the 'Who' class
Who = EClass('Who')
HelloWorldPackage.eClassifiers.append(Who)

# Create the 'name' attribute in 'Who'
name = EAttribute('name', EString, default_value="GPT")
Who.eStructuralFeatures.append(name)

# Create the 'HelloWorldModel' class
HelloWorldModel = EClass('HelloWorldModel')
HelloWorldPackage.eClassifiers.append(HelloWorldModel)

# Create the 'to_greet' reference in 'HelloWorldModel'
to_greet = EReference('to_greet', Who, upper=-1, containment=True)
HelloWorldModel.eStructuralFeatures.append(to_greet)

# Generate Python classes from the Ecore model
# (No need to retrieve from a registry, use the classes directly)

# Usage example
model = HelloWorldModel()
who1 = Who(name=" Alice ")
who2 = Who(name=" Bob ")
who3 = Who(name="")  # This will use the default value "GPT"

model.to_greet.extend([who1, who2, who3])

# Print the names to show that whitespace is trimmed and default is used
for person in model.to_greet:
    trimmed_name = person.name.strip()
    print(f"Greeting {trimmed_name if trimmed_name else name.default_value}!")
