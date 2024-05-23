This is an example of a simple Entity DSL.

File `entity.tx` contains a grammar of the language.  Each entity DSL model
consists of zero or more simple types definitions and one or more `Entity`
instances.  Each `Entity` instance contains one or more `Property` instance.
Each `Property` has a name conforming to built-in `ID` rule and a type which
can be a reference to either `SimpleType` or `Entity` from the model or one of
two built-in simple types representing basic types (`integer` and `string`, see
file `entity_test.py`).

Example model is given in the file `person.ent`.
