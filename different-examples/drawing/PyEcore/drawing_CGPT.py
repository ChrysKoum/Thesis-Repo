from pyecore.ecore import EClass, EAttribute, EReference, EInt, EPackage

# Package and metamodel definition
package = EPackage(name='drawing')

# EClass definitions
Model = EClass('Model')
DrawCommand = EClass('DrawCommand', abstract=True)
ShapeCommand = EClass('ShapeCommand', abstract=True)
MoveCommand = EClass('MoveCommand', abstract=True)
MoveTo = EClass('MoveTo')
MoveBy = EClass('MoveBy')
Circle = EClass('Circle')
LineTo = EClass('LineTo')
Point = EClass('Point')

# Attribute and reference definitions
commands = EReference('commands', DrawCommand, upper=-1, containment=True)
Model.eStructuralFeatures.append(commands)

position = EReference('position', Point, containment=True)
vector = EReference('vector', Point, containment=True)
radius = EAttribute('radius', EInt)
point = EReference('point', Point, containment=True)
x = EAttribute('x', EInt)
y = EAttribute('y', EInt)

# Setting up inheritance
ShapeCommand.eSuperTypes.append(DrawCommand)
MoveCommand.eSuperTypes.append(DrawCommand)
MoveTo.eSuperTypes.append(MoveCommand)
MoveBy.eSuperTypes.append(MoveCommand)
Circle.eSuperTypes.append(ShapeCommand)
LineTo.eSuperTypes.append(ShapeCommand)

# Adding attributes and references to classes
MoveTo.eStructuralFeatures.append(position)
MoveBy.eStructuralFeatures.append(vector)
Circle.eStructuralFeatures.append(radius)
LineTo.eStructuralFeatures.append(point)
Point.eStructuralFeatures.append(x)
Point.eStructuralFeatures.append(y)

# Finalizing the package
package.eClassifiers.extend([Model, DrawCommand, ShapeCommand, MoveCommand, MoveTo, MoveBy, Circle, LineTo, Point])

# Instantiate the classes
model = Model()
move_to = MoveTo()
point_move = Point()
circle = Circle()
point_circle = Point()

# Set the attributes for the Point associated with MoveTo
point_move.x = 150
point_move.y = 200
move_to.position = point_move

# Set the attributes for the Circle
circle.radius = 50
circle.position = point_circle

# Set the Point attributes for the Circle
point_circle.x = 300
point_circle.y = 300

# Add commands to the Model
model.commands.extend([move_to, circle])

# Now, we could serialize this model to an XMI or JSON format if needed,
# or manipulate it further in memory.

# Example of using the model in Python
print(f"Move command to point ({move_to.position.x}, {move_to.position.y})")
print(f"Draw circle with radius {circle.radius} at point ({circle.position.x}, {circle.position.y})")

# This code will output:
# Move command to point (150, 200)
# Draw circle with radius 50 at point (300, 300)
