# Gaze Detection Project

## Directory Contents
current_systems_notes/ - contains notes about current gaze estimation systems\
scripts/ - contains a script for processing a video using OpenFace and comparing the output data with 

## State of the Project
I have currently tested the code on two videos contained in the "Khaled gazecoding harmonization" folder within the OSF repository. 10123B.24.M.TL2-24-B.mov has generated an accuracy of around 86\%, while 7292A.25.M.HABLA25-1.mov has generated an accuracy of around 79\%, which means that the generated output is pretty accurate but might still be fine-tuned by looking at inconsistencies between the generated and the hand-coded outputs.

## To-Do
- Test code on more Marchman videos to find accuracies
- Fine-tune the numbers within the reformat_data method within the code