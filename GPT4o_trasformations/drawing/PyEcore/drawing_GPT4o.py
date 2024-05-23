import sys

# Add the path where validator.py is located to the system path
sys.path.append(r'D:\Aristotelio\_0_Thesis\0_Github\5_TextX_PyEcore')

# Now you can import the validate_model function
from validator import validate_model

from pyecore.ecore import EClass, EAttribute, EReference, EInt, EPackage
from pyecore.resources import ResourceSet, URI
from pyecore.notification import EObserver, Kind

# Package and metamodel definition
DrawPackage = EPackage(name='DrawPackage', nsURI='http://www.example.org/draw', nsPrefix='draw')

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
DrawPackage.eClassifiers.extend([Model, DrawCommand, ShapeCommand, MoveCommand, MoveTo, MoveBy, Circle, LineTo, Point])

# Example usage
# Helper function to create instances of the EClass with EAttributes
def create_instance(eclass, **kwargs):
    instance = eclass()
    for key, value in kwargs.items():
        setattr(instance, key, value)
    return instance

model = create_instance(Model)

# Create Point instances
point1 = create_instance(Point, x=5, y=10)
point2 = create_instance(Point, x=10, y=10)
point3 = create_instance(Point, x=20, y=20)
point4 = create_instance(Point, x=5, y=-7)
point5 = create_instance(Point, x=10, y=10)

# Create DrawCommand instances
move_to_command = create_instance(MoveTo, position=point1)
line_to_command1 = create_instance(LineTo, point=point2)
line_to_command2 = create_instance(LineTo, point=point3)
move_by_command = create_instance(MoveBy, vector=point4)
circle_command = create_instance(Circle, radius=10)
line_to_command3 = create_instance(LineTo, point=point5)

# Add commands to the model
model.commands.extend([move_to_command, line_to_command1, line_to_command2, move_by_command, circle_command, line_to_command3])

for command in model.commands:
    if isinstance(command, MoveTo):
        print(f"Move to position ({command.position.x}, {command.position.y})")
    elif isinstance(command, LineTo):
        print(f"Line to point ({command.point.x}, {command.point.y})")
    elif isinstance(command, MoveBy):
        print(f"Move by vector ({command.vector.x}, {command.vector.y})")
    elif isinstance(command, Circle):
        print(f"Draw circle with radius {command.radius}")

# Serialization Example
rset = ResourceSet()
resource = rset.create_resource(URI('model.xmi'))
resource.append(model)
resource.save()

# Notification System Example
class PrintNotification(EObserver):
    def notifyChanged(self, notification):
        print(f'Notification: {notification}')

# Create an observer instance and observe the model
observer = PrintNotification()
observer.observe(model)

# Add a command to trigger the notification
new_point = create_instance(Point, x=15, y=25)
new_move_to_command = create_instance(MoveTo, position=new_point)
model.commands.append(new_move_to_command)

diagnostics, metrics = validate_model(DrawPackage)

print("\nDiagnostics:")
for diagnostic in diagnostics:
    print(diagnostic)

print("\nMetrics:")
for key, value in metrics.items():
    print(f"{key}: {value}")
