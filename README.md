# FaceRecognitionTrigger
Using facial recognition to trigger other things from happening. In this case its playing an audio file. Entry to the Tufts 2018 Polyhack.

# How to Run
The dependencies are already installed in an virtualenv env. With python3 and virtualenv installed, you can just run env/Scripts/activate to start the virtual environment. 

In the virtual envrionment, the program can be run by just using python "program_name". None of the scripts take arguments, so you'll have to open up the file and edit the values to make certain changes. 

# Quick demo
By default, recognize.py uses encoding_merge as reference faces, and targets.json as actions for each defined face. encoding_merge has Tufts Computer Science Instructor Mark Sheldon as one of the recognized faces, and targets.json tells recognize.py to play an audio file (wav only). Professor Sheldon's image can be found here: https://engineering.tufts.edu/sites/default/files/newsthumbs/news-201705-sheldon.png

and is recognizable by the program when shown to it.