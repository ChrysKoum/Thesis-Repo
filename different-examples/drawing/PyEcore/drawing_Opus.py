from pyecore.ecore import EAttribute, EClass, EObject, EPackage, EInt, EReference

# Create the package
DrawingPackage = EPackage(name='drawingPackage', nsURI='http://www.example.org/drawing', nsPrefix='drawing')

# Create the 'Point' class
Point = EClass('Point')
DrawingPackage.eClassifiers.append(Point)

# Create 'x' and 'y' attributes in 'Point'
x = EAttribute('x', EInt)
y = EAttribute('y', EInt)
Point.eStructuralFeatures.extend([x, y])

# Create the 'DrawCommand' class
DrawCommand = EClass('DrawCommand', abstract=True)
DrawingPackage.eClassifiers.append(DrawCommand)

# Create the 'MoveCommand' class, inheriting from 'DrawCommand'
MoveCommand = EClass('MoveCommand', superclass=DrawCommand, abstract=True)
DrawingPackage.eClassifiers.append(MoveCommand)

# Create the 'MoveTo' class, inheriting from 'MoveCommand'
MoveTo = EClass('MoveTo', superclass=MoveCommand)
position = EReference('position', Point, containment=True)
MoveTo.eStructuralFeatures.append(position)
DrawingPackage.eClassifiers.append(MoveTo)

# Create the 'MoveBy' class, inheriting from 'MoveCommand'
MoveBy = EClass('MoveBy', superclass=MoveCommand)
vector = EReference('vector', Point, containment=True)
MoveBy.eStructuralFeatures.append(vector)
DrawingPackage.eClassifiers.append(MoveBy)

# Create the 'ShapeCommand' class, inheriting from 'DrawCommand'
ShapeCommand = EClass('ShapeCommand', superclass=DrawCommand, abstract=True)
DrawingPackage.eClassifiers.append(ShapeCommand)

# Create the 'Circle' class, inheriting from 'ShapeCommand'
Circle = EClass('Circle', superclass=ShapeCommand)
radius = EAttribute('radius', EInt)
Circle.eStructuralFeatures.append(radius)
DrawingPackage.eClassifiers.append(Circle)

# Create the 'LineTo' class, inheriting from 'ShapeCommand'
LineTo = EClass('LineTo', superclass=ShapeCommand)
point = EReference('point', Point, containment=True)
LineTo.eStructuralFeatures.append(point)
DrawingPackage.eClassifiers.append(LineTo)

# Create the 'Model' class
Model = EClass('Model')
commands = EReference('commands', DrawCommand, upper=-1, containment=True)
Model.eStructuralFeatures.append(commands)
DrawingPackage.eClassifiers.append(Model)

# Usage example
model = Model()

move_to = MoveTo(position=Point(x=10, y=20))
move_by = MoveBy(vector=Point(x=5, y=5))
circle = Circle(radius=30)
line_to = LineTo(point=Point(x=50, y=60))

model.commands.extend([move_to, move_by, circle, line_to])

# Print the model
for command in model.commands:
    if isinstance(command, MoveTo):
        print(f"MoveTo: ({command.position.x}, {command.position.y})")
    elif isinstance(command, MoveBy):
        print(f"MoveBy: ({command.vector.x}, {command.vector.y})")
    elif isinstance(command, Circle):
        print(f"Circle: radius={command.radius}")
    elif isinstance(command, LineTo):
        print(f"LineTo: ({command.point.x}, {command.point.y})")