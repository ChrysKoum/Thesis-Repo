from pyecore.ecore import EPackage, EClass, EAttribute, EReference, EString, EObject
from pyecore.resources import ResourceSet, URI
import sys

# Add the path where validator.py is located to the system path
sys.path.append(r'D:\Aristotelio\_0_Thesis\0_Github\5_TextX_PyEcore')

# Now you can import the validate_model function
from validator import validate_model

# Create the package
CalcPackage = EPackage(name='CalcPackage', nsURI='http://www.example.org/calc', nsPrefix='calc')

# Create classes
Calc = EClass('Calc')
Assignment = EClass('Assignment')
Expression = EClass('Expression')
Term = EClass('Term')
Factor = EClass('Factor')
Operand = EClass('Operand')

# Add classes to package
CalcPackage.eClassifiers.extend([Calc, Assignment, Expression, Term, Factor, Operand])

# Calc class
assignments = EReference('assignments', Assignment, upper=-1, containment=True)
expression = EReference('expression', Expression, containment=True)
Calc.eStructuralFeatures.extend([assignments, expression])

# Assignment class
variable = EAttribute('variable', EString)
expression = EReference('expression', Expression, containment=True)
Assignment.eStructuralFeatures.extend([variable, expression])

# Expression class
op = EReference('op', Term, upper=-1, containment=True)
Expression.eStructuralFeatures.append(op)

# Term class
op = EReference('op', Factor, upper=-1, containment=True)
Term.eStructuralFeatures.append(op)

# Factor class
sign = EAttribute('sign', EString, default_value='+')
op = EReference('op', Operand, containment=True)
Factor.eStructuralFeatures.extend([sign, op])

# Operand class
op = EAttribute('op', EString)  # This can hold NUMBER, ID, or Expression string representation
Operand.eStructuralFeatures.append(op)

# Custom classes implementation
namespace = {}

class CalcImpl(EObject):
    def __init__(self):
        self.assignments = []
        self.expression = None

    @property
    def value(self):
        for a in self.assignments:
            namespace[a.variable] = a.expression.value
        return self.expression.value

class ExpressionElementImpl(EObject):
    def __init__(self):
        self.op = None

class FactorImpl(ExpressionElementImpl):
    def __init__(self):
        super().__init__()
        self.sign = '+'
        self.op = None

    @property
    def value(self):
        value = self.op.value
        return -value if self.sign == '-' else value

class TermImpl(ExpressionElementImpl):
    @property
    def value(self):
        ret = self.op[0].value
        for operation, operand in zip(self.op[1::2], self.op[2::2]):
            if operation == '*':
                ret *= operand.value
            else:
                ret /= operand.value
        return ret

class ExpressionImpl(ExpressionElementImpl):
    @property
    def value(self):
        ret = self.op[0].value
        for operation, operand in zip(self.op[1::2], self.op[2::2]):
            if operation == '+':
                ret += operand.value
            else:
                ret -= operand.value
        return ret

class OperandImpl(ExpressionElementImpl):
    @property
    def value(self):
        op = self.op
        if type(op) in {int, float}:
            return op
        elif isinstance(op, ExpressionElementImpl):
            return op.value
        elif op in namespace:
            return namespace[op]
        else:
            raise Exception(f'Unknown variable "{op}"')

# Example usage of the model
print("Model: CalcPackage")
print("Classes:")
for cls in CalcPackage.eClassifiers:
    print(f"  Class: {cls.name}")
    for feature in cls.eStructuralFeatures:
        feature_type = 'EAttribute' if isinstance(feature, EAttribute) else 'EReference'
        feature_type_name = feature.eType.name if hasattr(feature.eType, 'name') else str(feature.eType)
        print(f"    {feature_type}: {feature.name} (type: {feature_type_name})")

# Validate the model
diagnostics, metrics = validate_model(CalcPackage)

print("\nDiagnostics:")
for diagnostic in diagnostics:
    print(diagnostic)

print("\nMetrics:")
for key, value in metrics.items():
    print(f"{key}: {value}")
