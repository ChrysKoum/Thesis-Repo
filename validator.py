import pyecore.ecore as Ecore
from pyecore.ecore import EDataType, EEnum, EStructuralFeature, EAttribute, ETypedElement, EClass, EReference, EString, EPackage, EObject
from pyecore.utils import dispatch
from enum import unique, Enum
from collections import namedtuple

# Definition of error levels and diagnostics
@unique
class Level(Enum):
    OK = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITIC = 4

Diagnostic = namedtuple('Diagnostic', ['rule_id', 'level', 'elements', 'message'])

OK_diagnostic = Diagnostic(None, Level.OK, set(), None)

# Definition of validation rules
def no_name(named_element):
    """
    Check if the name feature of an object is set
    """
    print(f"Validating no_name for {named_element}")
    if named_element.name:
        return OK_diagnostic
    eclass_name = named_element.eClass.name
    return Diagnostic('no_name', Level.ERROR, {named_element},
                      '{} instances must have a name'.format(eclass_name))

def same_name_in_namespace(obj, container):
    """
    Check if two objects own the same name in the same namespace
    """
    print(f"Validating same_name_in_namespace for {obj}")
    problematic_elements = set()
    for element in (e for e in container if e is not obj):
        if element.name == obj.name:
            problematic_elements.add(element)
    if not problematic_elements:
        return OK_diagnostic
    problematic_elements.add(obj)
    message = 'These objects have the same name in the namespace: {}'.format(
        [e.name for e in problematic_elements])
    return Diagnostic('same_name', Level.ERROR, problematic_elements, message)

def no_type(typed_element):
    """
    Check if the type of an element is well set
    """
    print(f"Validating no_type for {typed_element}")
    if typed_element.eType:
        return OK_diagnostic
    eclass_name = typed_element.eClass.name
    message = '{} instances must have a type.'.format(eclass_name)
    return Diagnostic('no_type', Level.ERROR, {typed_element}, message)

def validate_multiplicity(feature):
    """
    Check if the multiplicity of a feature is valid
    """
    print(f"Validating validate_multiplicity for {feature}")
    if feature.upper is not None and feature.lower is not None and feature.upper != -1 and feature.upper < feature.lower:
        message = 'Multiplicity upper bound cannot be less than lower bound for {}.'.format(feature.name)
        return Diagnostic('invalid_multiplicity', Level.ERROR, {feature}, message)
    return OK_diagnostic

def validate_unique_names_within_container(container):
    """
    Validate that all elements within a container have unique names
    """
    print(f"Validating validate_unique_names_within_container for {container}")
    names = set()
    for element in container.eContents:
        if element.name in names:
            return Diagnostic('duplicate_names', Level.ERROR, {element},
                              'Duplicate name found: {}'.format(element.name))
        names.add(element.name)
    return OK_diagnostic

def validate_containment(reference):
    """
    Validate that containment references are properly set
    """
    print(f"Validating validate_containment for {reference}")
    if reference.containment and reference.eOpposite and reference.eOpposite.containment:
        return Diagnostic('invalid_containment', Level.ERROR, {reference, reference.eOpposite},
                          'Both {} and its opposite {} are containment references'.format(reference.name, reference.eOpposite.name))
    return OK_diagnostic

def get_python_type(edatatype):
    """
    Return the corresponding Python type for an EDataType
    """
    if edatatype.name == 'EString':
        return str
    elif edatatype.name == 'EInt':
        return int
    elif edatatype.name == 'EBoolean':
        return bool
    # Add more type mappings as necessary
    return None

def validate_default_value(attribute):
    """
    Validate default value against the attribute type
    """
    print(f"Validating validate_default_value for {attribute}")
    if attribute.default_value is not None:
        if isinstance(attribute.eType, EEnum):
            if attribute.default_value not in [literal.name for literal in attribute.eType.eLiterals]:
                return Diagnostic('invalid_default_value', Level.ERROR, {attribute},
                                  f'Default value {attribute.default_value} is not a valid literal of {attribute.eType.name}')
        elif isinstance(attribute.eType, EDataType):
            python_type = get_python_type(attribute.eType)
            if python_type is not None and not isinstance(attribute.default_value, python_type):
                return Diagnostic('invalid_default_value', Level.ERROR, {attribute},
                                  f'Default value {attribute.default_value} is not of type {python_type.__name__}')
        else:
            if not isinstance(attribute.default_value, attribute.eType.getEClassifier().__class__):
                return Diagnostic('invalid_default_value', Level.ERROR, {attribute},
                                  f'Default value {attribute.default_value} is not of type {attribute.eType.name}')
    return OK_diagnostic


# Ecore validator, it binds rules with specific EObjects
class EcoreValidator(object):
    @dispatch
    def do_switch(self, obj):
        return set()

    def apply_rules(self, obj, rules):
        diagnostics = []
        for rule in rules:
            diagnostic = rule(obj)
            if diagnostic.level is not Level.OK:
                diagnostics.append(diagnostic)
        return diagnostics

    @do_switch.register(EClass)
    def validate_EClass(self, eclass):
        print(f"Validating EClass {eclass}")
        eclassifiers = eclass.ePackage.eClassifiers
        same_name = lambda obj: same_name_in_namespace(obj, eclassifiers)
        return self.apply_rules(eclass, [no_name, same_name])

    @do_switch.register(EStructuralFeature)
    def validate_EStructuralFeature(self, feature):
        print(f"Validating EStructuralFeature {feature}")
        all_features = feature.eContainingClass.eAllStructuralFeatures()
        same_name = lambda obj: same_name_in_namespace(obj, all_features)
        rules = [no_name, same_name, no_type, validate_multiplicity]
        if isinstance(feature, EReference):
            rules.append(validate_containment)
        elif isinstance(feature, EAttribute):
            rules.append(validate_default_value)
        return self.apply_rules(feature, rules)

    @do_switch.register(ETypedElement)
    def validate_ETypedElement(self, typed):
        print(f"Validating ETypedElement {typed}")
        return self.apply_rules(typed, [no_type])

    @do_switch.register(EPackage)
    def validate_EPackage(self, epackage):
        print(f"Validating EPackage {epackage}")
        rules = [no_name]
        if epackage.eSuperPackage:
            parent_package = epackage.eSuperPackage.eSubpackages
            same_name = lambda obj: same_name_in_namespace(obj, parent_package)
            rules.append(same_name)
        return self.apply_rules(epackage, rules)

    @do_switch.register(EObject)
    def validate_EObject(self, eobject):
        print(f"Validating EObject {eobject}")
        return self.apply_rules(eobject, [validate_unique_names_within_container])

# The generic validate function that applies a validator to a model root
def validate(root, validator):
    diagnostics = [*validator.do_switch(root)]
    for element in root.eAllContents():
        diagnostics.extend(validator.do_switch(element))
    return diagnostics

# A dedicated validator for ecore
def validate_ecore(root):
    return validate(root, EcoreValidator())

# Function to calculate precision, recall, and F1 score
def calculate_metrics(diagnostics, total_elements):
    print("Total elements:", total_elements)
    print("Diagnostics:", diagnostics)
    
    true_positives = len([d for d in diagnostics if d.level == Level.ERROR])
    false_positives = total_elements - true_positives
    false_negatives = 0  # Assuming human review ensures no false negatives

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print("True Positives:", true_positives)
    print("False Positives:", false_positives)
    print("False Negatives:", false_negatives)
    
    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'true_positives': true_positives,
        'false_positives': false_positives,
        'false_negatives': false_negatives
    }

def validate_model(model):
    diagnostics = validate_ecore(model)
    total_elements = len(list(model.eAllContents())) + 1  # +1 for the root element
    metrics = calculate_metrics(diagnostics, total_elements)
    return diagnostics, metrics

# Example usage
if __name__ == "__main__":
    from pyecore.ecore import EAttribute, EClass, EReference, EString, EPackage

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
    to_greet = EReference('to_greet', Who, upper=-1, lower=0, containment=True)
    HelloWorldModel.eStructuralFeatures.append(to_greet)

    # Generate Python classes from the Ecore model
    # (No need to retrieve from a registry, use the classes directly)

    # Usage example
    model = HelloWorldModel()
    who1 = Who(name="Alice")
    who2 = Who(name="Bob")
    who3 = Who(name="")  # This will use the default value "GPT"

    model.to_greet.extend([who1, who2, who3])

    # Print the names to show that whitespace is trimmed and default is used
    for person in model.to_greet:
        trimmed_name = person.name.strip()
        print(f"Greeting {trimmed_name if trimmed_name else name.default_value}!")

    # Validate the model
    diagnostics, metrics = validate_model(HelloWorldPackage)

    print("\nDiagnostics:")
    for diagnostic in diagnostics:
        print(diagnostic)

    print("\nMetrics:")
    for key, value in metrics.items():
        print(f"{key}: {value}")
