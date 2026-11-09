# About RATs 🐁
RATs are rapid assessment tests that the bootcamp participants can use in order to rapidly assess their knowledge about a certain topic. 
The following section will guide us on how to create a set of RATs 🐁 on a new topic.


## Adding Multiple Questions on a Topics to Our RATs 🐁

To do this, we need to create a new JSON file to store the questions and create a corresponding Jupyter Notebook file to display the assessment questions.

### STEP 1: Create a New JSON File

1. **Create a New JSON File**: Under the folder `RATs/questions/` we start by creating a new JSON file to store the assessment questions regarding a new topic.

2. **Define the Assessment Questions**: We add multiple questions in JSON format. Each assessment question should include the following properties:

   - `"question"`: The text of the assessment question.
   - `"type"`: The type of the question, such as "multiple_choice," "many_choice," or another appropriate type.
   - `"answers"`: An array of possible answers with correctness information.
     - Each answer should include:
       - `"answer"`: The text of the answer option.
       - `"correct"`: A Boolean value indicating whether the answer is correct (true) or not (false).
       - `"feedback"`: Feedback associated with the answer, displayed upon selection.

   This [source](https://github.com/jmshea/jupyterquiz#multiplemany-choice-questions) nicely shows the Multiple/Many Choice questions schema.  
   Here's an example of multiple assessment questions.

   ```json
   [
       
    {
        "question": "Check all statements on KNN that are correct.",
        "type": "many_choice",
        "answers": [
            {
                "answer": "KNN can be used for classification.",
                "correct": true,
                "feedback": "That's correct! KNN is a supervised learning algorithm and can be used for classification. "
            },
            {
                "answer": "KNN can be used for regression.",
                "correct": true,
                "feedback": "That's correct! KNN is a supervised learning algorithm and can be used for regression. "
            },
            {
                "answer": "KNN is an unsupervised learning algorithm.",
                "correct": false,
                "feedback": "Sorry, that was wrong. KNN is a supervised learning algorithm. Please try again"
            },
            {
                "answer": "KNN has longer training time than prediction time.",
                "correct": false,
                "feedback": "Sorry, that was wrong. At training time, KNN doesn't need to do distance calculations, while the prediction time is high, as distances between test data and training data points have to be calculated (to decide which are its closest neighbors). Please try again"
            },
            {
                "answer": "KNN makes assumptions about the functional form of the problem being solved.",
                "correct": false,
                "feedback": "Sorry, that was wrong. KNN is a non-parametric algorithm and does not make any assumption on data distribution! Please try again"
            }
        ]
    },
    {
        "question": "Is it important to scale the data when applying KNN? What do you answer?",
        "type": "multiple_choice",
        "answers": [
            {
                "answer": "No, KNN will find the nearest neighbors despite different scales.",
                "correct": false,
                "feedback": "Sorry, that was wrong. Please try again"
            },
            {
                "answer": "Yes, it is computationally more efficient. The results would be the same, but Gradient Descent will find the minimum faster.",
                "correct": false,
                "feedback": "Sorry, that was wrong. Please try again"
            },
            {
                "answer": "It depends. You don't need to scale when using Euclidean distance. For Manhattan distance you should use scaled data.",
                "correct": false,
                "feedback": "Sorry, that was wrong. Please try again"
            },
            {
                "answer": "Yes, KNN is based on similarity measurement,  which is sensitive to scaling.",
                "correct": true,
                "feedback": "Correct. Algorithms based on similarity measurements are sensitive to scaling. The similarity is measured by calculating distances between points. If the features don't have the same scale, the feature with the larger scale will have a bigger influence of the outcome than smaller scaled features. To avoid this, you should scale your data before using KNN."
            }
        ]
    }
   ]
   ```

3. **Save the JSON File**: We save the new JSON file with a descriptive name (our convention is *number_New_Topic_questions.json*, e.g., `01_Git_questions.json`).

### STEP 2: Create a Jupyter Notebook file

Under the folder `RATs/` we create a new Jupyter Notebook file, corresponding to the newly created JSON file. The Jupyter Notebook file should contain three cells:
  
The `1st` is a markdown cell containing the title. 
    
The `2nd` is a code cell that
+ imports necessary libraries
+ defines the path to the JSON file, containing the questions
+ imports a JSON file with color information to customize the quiz appearence (To set the RATs colors please refers to the instructions on [how_to_set_the_color_scheme](how_to_set_the_color_scheme.md)).

```py 
from jupyterquiz import display_quiz
import json

# Import questions
path = "questions/number_New_Topic_questions.json"

# Import colors
dict_name = "RAT_colors.json"

with open(dict_name, 'r') as f:
color_dict = json.load(f)
```

The `3rd` is a code cell that 
+ uses a display_quiz function to render the questions

```python
display_quiz(path, colors=color_dict) 
```

### STEP 3: Change Jupyter Cells setting
On the jupyter-book to only see the quiz but not the code that generates it, we need to properly add Tags to the Jupyter Notebook file cells:

|**Cell**|**Tag**|
|:---:|:--:| 
| 2nd|remove-cell|
|3rd| remove-input|

This [source](https://github.com/microsoft/vscode-jupyter-cell-tags#jupyter-cell-tags-support-in-vs-code) clearly explains how to add Tag to jupyter notebook cells.

### STEP 4: Save Jupyter Notebook and update _toc.yml
After making sure that all the cells works properly, we
+ save the Jupyter Notebook (our name convention is *number_New_Topic_RAT.ipynb*, e.g, `01_Git_RAT.ipynb`) 
+ update the *caption: Rapid Assessment Test* in the
[_toc.yml](../DSBOOK/_toc.yml) file.




