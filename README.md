# Automatic-Detection-of-Cancer-cells
It involves the implementation of Image Segmentation algorithm and Transfer Learning in Tensorflow for the automatic detection of cancer cells (GUI included) 


This project helps in the segmentation of multiple nuclei from a slide image, its extraction and finally
its classification by a pretrained Inception v3 Model in the TensorFlow framework. 
The results is displayed on the GUI with the addition of performance metrics of the segmentation algorithm 
in terms of Precision and Recall. 

Perfomance metrics :
 -Precision - The accuracy of the algorithm in accordance with the expert analysis. 
 -Recall - The accuracy of detection of the required Nuclei. 
 
 Tools and Platform used : 
 -Python 2.7.13 (interpreter)
 -PyCharm IDE (optional, can be used with normal gedit editor also)
 -Open-CV, regionprops, Tkinter (dependency libraries, along with the general libraries for python coding)
 -TensorFlow (www.tensorflow.org)

Recommended CPU specifications : 
 - LINUX operating systems (ubuntu, kali-linux, etc)
 - Intel i3/i5/i7 or equivalent processor
 - 4 GB RAM
 - Dedicated GPU (for training model)

Before GUI run :
- Change all the path specified in the files Layout.py, Image_Predict.py stating "ROOT DIRECTORY NAME" to the specified directory 
 where the project files are saved in the directory.
 
 
Steps to run the GUI :
1> Open terminal in the folder, and run the script using command 'python Layout.py'
2> Click 'Begin'
3> Select desired image using the 'Choose image' option [select '.BMP' for herlev dataset, not '-d.bmp']
4> To evaluate for Precision and Recall values, click 'Evaluate' and then select the dataset type accordingly
5> To view the segmentation process and also to extract the nuclei for prediction, first click 'Segment' and then 
     select dataset type accordingly
6> Once segmentation process is terminated, click 'Predict' to view the abnormal and normal count of nuclei. 
7> To terminate or start for a new image, close the application and run the script again. 

Thank You.
