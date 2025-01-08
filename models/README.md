## Folder Structure

- `Datasets/` : Contains the datasets used for training and testing the models. The subfolder `Complete/` contains the final dataset used for training the multilayer model. More info on the [README](https://github.com/nicollorens12/SentinelX/tree/main/models/Datasets) inside the folder.

- `HierarchicalModel/` : Contains the trained models and it's tag encoding.

## Notebooks

- `DataAnalysis.ipynb`: Contains the data analysis of the initial (much smaller) dataset. It was used to understand the data and make the first performance test with simple models.

- `HCLevelStudy.ipynb`: With the problem reflected on *DataAnalysis.ipynb* the imbalance of the dataset was identified, which led to poor performance on minority classes. With the objective of improving this, a hierarchical model was proposed. This notebook contains the study of the hierarchical model and the training of the 3 levels. The third level was the one that should improve performance on minority classes but it was not achieved eventhough we implemented synthetic data augmentation methods like SMOTE. 

- `HCLevel3Study.ipynb`: This notebook contains the study of the third level of the hierarchical model. The objective was to improve the performance of the minority classes. We made the decision to combine 2 more years of data of the original dataset. We had to remove some variables that were not present in the new data. We also implemented synthetic data augmentation methods like SMOTE and ADASYN. With this, we tried again a TensorFlow which didn't get the performance we wanted. We tried a new aproach XGBoost which gave us much better results. 

- `HCCompleteStudy.ipynb`: Using the new bigger dataset, we trained the three different models:
    - **Random Forest Classifier**: as seen on `HCLevelStudy.ipynb` showed the best performance for deciding between a benign and malign traffic.

    - **MLP Classifier**: as seen on `HCLevelStudy.ipynb` showed the best performance for deciding between the different types of malign traffic.

    - **XGBoost Classifier**: as seen on `HCLevel3Study.ipynb` showed the best performance for deciding between the different types of malign WebAttack traffic. This kind of attacks were more difficult to detect correctly because they don't generate a lot of traffic.

- `HC_Performance_Test.ipynb`: This notebook contains the performance test of the final hierarchical model. We trained the 3 models with the complete dataset, saved the trained models and encodings and tested them with the test dataset. Here we can see the performance of the models and the confusion matrix of the test dataset. Which obtained an average precision of 99%.