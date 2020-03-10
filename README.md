# Naive-Bayes-Classifier-Spam-Ham

A Naive Bayes Classifier built without the use of libraries to classify emails as Spam or Ham

1. nblearn.py:

nblearn.py will be invoked in the following way:
>python3 nblearn.py /path/to/input
And output a model file called nbmodel.txt
  1.1 Reading data
  The argument is a data directory. The script should search through the directory recursively looking for
  subdirectories containing the folders: "ham" and "spam". Note that there can be multiple "ham" and "spam" folders in the data directory. Emails are stored in files with the extension ".txt" under these directories. 
  1.2 Learning the model 
  You will need to estimate and store P(spam) and P(ham) as well as conditional probabilities P(token|spam) and P(token|ham) for all    unique tokens. These probabilities should be stored in the model file nbmodel.txt. The format of the file is up to you but your nbclassify.py program must be able to read it. 

2. nbclassify.py

nbclassify.py will be invoked in the following way:
>python3 nbclassify.py /path/to/input
The argument is again a data directory but you should not make any assumptions about the structure of
the directory. Instead, you should search the directory for files with the extension ".txt". nbclassify.py
should read the parameters of a naïve Bayes model from the file nbmodel.txt, and classify each ".txt"
file in the data directory as "ham" or "spam", and write the result to a text file called nboutput.txt in the
format below:

LABEL path_1
LABEL path_2
⋮

3. nbevaluate.py

nbevaluate.py will be invoked in the following way:
>python3 nbevaluate.py nboutput_filename
nboutput_filename is the output file of nbclassify.py described above. For each line in the file,
nbevaluate.py will split the line into the guessed label and file path. nbevaluate.py will search for ham or
spam in the path to determine the true label of the example (i.e., “spam” or “ham”). If neither is found,
then it will skip to the next line in the file. Otherwise, the true label will be compared to the guessed
label. You will need to maintain counts allowing you to calculate precision, recall and F1 score for both
spam and ham and print them once all output has been processed. You will include these values in your
report. Note that your program should not crash if no labeled examples are seen and you should be
careful to avoid dividing by zero
