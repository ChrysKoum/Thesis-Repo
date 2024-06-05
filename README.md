# Process for Evaluating TextX to PyEcore Transformation

## Initial Steps

1. **Define the Initial Prompt:**
   - Begin by clearly defining the initial prompt that outlines the requirements and context for the metamodel transformation.

2. **Specify the Grammar:**
   - Provide the TextX grammar that will be transformed into a PyEcore metamodel. This grammar serves as the basis for the transformation process.

3. **Answer Clarification Questions:**
   - Answer any specific questions regarding the details of the transformation. This includes defining package details, containment references, default values, multiplicities, and opposite references.

## Transformation Process

1. **Generate the PyEcore Metamodel:**
   - Based on the initial prompt and grammar, generate the corresponding PyEcore metamodel. Ensure that all elements, attributes, and references are correctly defined.

2. **Add Path for Validator:**
   - Add the path where `validator.py` is located to the system path. This is necessary to validate the metamodel.

   ```python
   import sys

   # Add the path where validator.py is located to the system path
   sys.path.append(r'path_to_validator')
   
   from validator import validate_model
   ```

3. **Evaluate the Metamodel:**
   - **Human Review:**
     - Manually review the metamodel for correctness, completeness, and adherence to best practices.
   - **LLM Review:**
     - Use a Language Learning Model to provide an automated evaluation of the metamodel. The LLM review should consider criteria such as data inheritance, two-way relationship management, serialization/deserialization, notification system, reflexive API usage, containment and multiplicity, default values, package details, element naming and typing, and validation and error handling.

## Evaluation Criteria

The following criteria should be used for evaluating the PyEcore metamodel:

1. **Data Inheritance:**
   - How well does the metamodel utilize data inheritance to define hierarchical relationships between classes?

2. **Two-way Relationship Management:**
   - Does the metamodel correctly implement two-way relationships using opposite references?

3. **Serialization and Deserialization:**
   - How effectively does the metamodel support XMI and JSON serialization/deserialization? Are the necessary configurations and attributes correctly set to enable this?

4. **Notification System:**
   - Does the metamodel leverage the notification system to track changes and updates to objects and their properties?

5. **Reflexive API:**
   - Does the metamodel make full use of the reflexive API to dynamically interact with and introspect model elements?

6. **Containment and Multiplicity:**
   - Are containment relationships correctly defined? Are the multiplicities (lower and upper bounds) appropriately set, especially for unbounded collections (e.g., upper=-1)?

7. **Default Values:**
   - Are default values for attributes properly specified and valid according to their defined types?

8. **Package Details:**
   - Are the package name, namespace URI, and namespace prefix correctly defined and consistent with your project's naming conventions?

9. **Element Naming and Typing:**
   - Are all named elements given meaningful names? Are types correctly set for all attributes and references?

10. **Validation and Error Handling:**
    - Does the metamodel include validation rules to enforce constraints and handle errors effectively?

## Results
To evaluate the performance of ChatGPT-4 in transforming TextX grammars into PyEcore metamodels, let's summarize the provided data and calculate an overall score based on various metrics such as accuracy, number of errors, and improvement after the refinement process.

### Summary of Data

Here is the summary of the transformations:

| TextX Grammar       | Initial Prompts | Initial Errors | Initial LLM Review Score | Initial Metrics    | Improved Prompts | Improved Errors | Improved LLM Review Score | Improved Metrics  | Accuracy (AIP) | Notes                                                                                                                                                       |
|---------------------|------------------|----------------|--------------------------|---------------------|------------------|-----------------|---------------------------|--------------------|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Hello World         | 2                | 0              | 91%                      | TP: 0, FP: 5, FN: 0 | 1                | 0               | 95%                       | TP: 0, FP: 5, FN: 0 | 93%             |                                                                                                                                                             |
| Drawing             | 3                | 1              | 80%                      | TP: 0, FP: 17, FN: 0| 3                | 0               | 90%                       | TP: 0, FP: 17, FN: 0| 91%             |                                                                                                                                                             |
| Entity              | 4                | 1              | 83%                      | TP: 0, FP: 10, FN: 0| 4                | 1               | 80%                       | TP: 0, FP: 10, FN: 0| 77%             |                                                                                                                                                             |
| Expression Calc     | 6                | 2              | 78%                      | TP: 0, FP: 16, FN: 0| 3                | 2               | 85%                       | TP: 0, FP: 16, FN: 0| 79%             |                                                                                                                                                             |
| IBM_Rhapsody        | 4                | 1              | 85%                      | TP: 0, FP: 22, FN: 0| 2                | 1               | 95%                       | TP: 0, FP: 22, FN: 0| 94%             |                                                                                                                                                             |
| JSON                | 3                | 0              | 60%                      | TP: 0, FP: 15, FN: 0| 1                | 0               | 70%                       | TP: 0, FP: 15, FN: 0| 78%             |                                                                                                                                                             |
| MyDataFormat        | 5                | 1              | 70%                      | TP: 0, FP: 40, FN: 0| 2                | 0               | 75%                       | TP: 0, FP: 40, FN: 0| 80%             |                                                                                                                                                             |
| PyFlies             | 3                | 0              | 85%                      | TP: 2, FP: 82, FN: 0| 1                | 0               | 95%                       | TP: 0, FP: 82, FN: 0| 92%             |                                                                                                                                                             |
| Robot               | 2                | 1              | 80%                      | TP: 1, FP: 14, FN: 0| 1                | 0               | 83%                       | TP: 1, FP: 14, FN: 0| 82%             | Better results after including core imports and avoiding unsupported PyEcore imports                                                                         |
| StateMachine        | 1                | 0              | 70%                      | TP: 0, FP: 19, FN: 0| 3                | 2               | 90%                       | TP: 0, FP: 20, FN: 0| 82%             |                                                                                                                                                             |
| Workflow            | 1                | 0              | 85%                      | TP: 0, FP: 14, FN: 0| 1                | 0               | 90%                       | TP: 0, FP: 14, FN: 0| 88%             |                                                                                                                                                             |

### Metrics Calculation

To calculate the overall performance, we will use the following approach:
1. **Average Initial LLM Review Score:** Sum of initial scores divided by the number of grammars.
2. **Average Improved LLM Review Score:** Sum of improved scores divided by the number of grammars.
3. **Overall Accuracy (AIP):** Sum of accuracy (AIP) divided by the number of grammars.
4. **Error Reduction:** Compare the initial and improved number of errors.

#### 1. Average Initial LLM Review Score
\[ \text{Average Initial Score} = \frac{91 + 80 + 83 + 78 + 85 + 60 + 70 + 85 + 80 + 70 + 85}{11} = 78.18\% \]

#### 2. Average Improved LLM Review Score
\[ \text{Average Improved Score} = \frac{95 + 90 + 80 + 85 + 95 + 70 + 75 + 95 + 83 + 90 + 90}{11} = 86.36\% \]

#### 3. Overall Accuracy (AIP)
\[ \text{Overall Accuracy (AIP)} = \frac{93 + 91 + 77 + 79 + 94 + 78 + 80 + 92 + 82 + 82 + 88}{11} = 84.18\% \]

#### 4. Error Reduction
The total initial errors are 7, and the total improved errors are 6, showing a reduction in errors.

### Final Evaluation

Based on the above calculations:
- **Initial Average Score:** 78.18%
- **Improved Average Score:** 86.36%
- **Overall Accuracy (AIP):** 84.18%
- **Error Reduction:** 14.3% reduction in the number of errors.

### Conclusion

The performance of ChatGPT-4 in transforming TextX grammars into PyEcore metamodels is quite satisfactory, especially after refinement:
- It demonstrates a significant improvement in scores after additional prompts and refinement.
- The overall accuracy (AIP) is relatively high, suggesting a strong alignment with expected outcomes.
- Error reduction indicates effective troubleshooting and optimization through the refinement process.

**Overall Score: 84.18%**

This score reflects the model's ability to accurately transform grammars and improve with targeted prompts and corrections.

**Detailed Results Google Sheet**
- The results of the evaluation, including scores and comments from both human and LLM reviews, can be found in the following spreadsheet:
  [Results Spreadsheet](https://docs.google.com/spreadsheets/d/1B7szJMXmRjEzR6IoRBZKPP0nYUB0yLLz73dRh5k28e8/edit?usp=sharing)
