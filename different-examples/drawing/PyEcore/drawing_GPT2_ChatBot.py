from pyecore.ecore import EPackage, EClass, EAttribute, EReference, EInt, EEnum, EEnumLiteral

# Create the Ecore package
DrawingPackage = EPackage(name='drawingPackage', nsURI='http://www.example.org/drawing', nsPrefix='drawing')

# Enumerations for keywords
MoveType = EEnum('MoveType', literals=['move'])
DirectionType = EEnum('DirectionType', literals=['to', 'by'])
ShapeType = EEnum('ShapeType', literals=['line', 'circle'])

# EClass declarations
Model = EClass('Model')
DrawCommand = EClass('DrawCommand', abstract=True)

ShapeCommand = EClass('ShapeCommand', abstract=True)
MoveCommand = EClass('MoveCommand', abstract=True)

MoveTo = EClass('MoveTo')
MoveBy = EClass('MoveBy')
LineTo = EClass('LineTo')
Circle = EClass('Circle')
Point = EClass('Point')

# Adding classifiers to the package
DrawingPackage.eClassifiers.extend([Model, DrawCommand, ShapeCommand, MoveCommand, 
                                     MoveTo, MoveBy, LineTo, Circle, Point, 
                                     MoveType, DirectionType, ShapeType])

# Model has a list of DrawCommands
Model.commands = EReference('commands', DrawCommand, containment=True, upper=-1)

# MoveTo and MoveBy - using Enums
MoveTo.moveType = EAttribute('moveType', MoveType, default_value=MoveType.move)
MoveTo.directionType = EAttribute('directionType', DirectionType, default_value=DirectionType.to)
MoveTo.position = EReference('position', Point, containment=True)

MoveBy.moveType = EAttribute('moveType', MoveType, default_value=MoveType.move)
MoveBy.directionType = EAttribute('directionType', DirectionType, default_value=DirectionType.by)
MoveBy.vector = EReference('vector', Point, containment=True)

# Shape definitions
LineTo.shapeType = EAttribute('shapeType', ShapeType, default_value=ShapeType.line)
LineTo.point = EReference('point', Point, containment=True)

Circle.shapeType = EAttribute('shapeType', ShapeType, default_value=ShapeType.circle)
Circle.radius = EAttribute('radius', EInt)

# Define Point
Point.x = EAttribute('x', EInt)
Point.y = EAttribute('y', EInt)

# Inheritance structure
DrawCommand.eSuperTypes.append(MoveCommand)
DrawCommand.eSuperTypes.append(ShapeCommand)

MoveCommand.eSuperTypes.append(MoveTo)
MoveCommand.eSuperTypes.append(MoveBy)

ShapeCommand.eSuperTypes.append(LineTo)
ShapeCommand.eSuperTypes.append(Circle)