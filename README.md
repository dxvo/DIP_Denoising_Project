# Digital Image Restoration
### Description
A Python application that is able to enhance an degraded image by using different filters chosen by user
### Objecttives
- Generate degraded images by adding various type of noise such as: gaussian, uniform, rayleigh, salt, peppers, gaussian and uniform, salt and peppers.  
- Enhance image by applying different type of mean and order-statistic filters
### How to run 
- Compile and run main.py file with all other files in the same directory (no additional argument is needed)
- Please make sure to your current setup has 4 seperate output directory name: Cropped, histogram, Noise and Restored

### Application Instruction 

- **Step 1**: From the main screen - click anywhere to load image 

![image](https://user-images.githubusercontent.com/42792976/49464514-aba07000-f7c0-11e8-9ddc-c1f307ea6cf4.png)

- Step 2: Add noise to original image to generate degraded image
- **Step 3**: Select the type of noise from Menu to add to the image.
		- If Gaussian, Rayleigh and Uniform noise is seleteced - The input will be the noise variance. We assume the mean is 0 for simplicity. 
		- If Salt, peppers or salt and peppers noise is selected - user is prompt to enter the probability (.1 - 0.9 value)
		- For gamma nosie, the user needs to input the variable a and b displacement.

![image](https://user-images.githubusercontent.com/42792976/49464584-e73b3a00-f7c0-11e8-9d3e-2b941464c1f6.png)

- For this tutorial. We will use Gaussian noise with variance value of 30. 
- **Step 4**: User can either choose to compute statistic of the noise (such as variance from histogram) or user can choose to apply filter on the image right the way. 
	* If Filter option is selected, then user can select filter type from the menu. More on this will be eleborate in step 7.
	* We suggest to compute the noise ststistics,so it can be compared later with the restored image histogram. Note that, If you choose to apply filter without computing noise statistics, the compare histogram option will not be available.

![image](https://user-images.githubusercontent.com/42792976/49464833-a7c11d80-f7c1-11e8-8a72-82d8b21199d3.png)

-**Step 5**: 
	* If noise analysis is selected from previous step, please crop a "constant background" area on the image and select "Compute Noise Statistic" to generate the histogram. The image mean and noise variance as well as the coordinate of cropped region are also printed out to screen

![image](https://user-images.githubusercontent.com/42792976/49465537-82351380-f7c3-11e8-9d05-32c4d8babe28.png) 

- **Step 6**: User are given 3 options 
	* Apply Filter: Select this option to apply filter to degraded image 
	* Undo: select this option to select another region on the image 
	* Restart: restart program from beginning with another image 

![image](https://user-images.githubusercontent.com/42792976/49465662-c58f8200-f7c3-11e8-9346-cfbdd3c479ca.png)

- **Step 7**: If user selects "Apply filter" either in step 6 or step 4. Select the available filter type from the menu. Program then asks user to input filter size. Enter filter height and width then submit. The program will display the degraded image and retored image. 

![image](https://user-images.githubusercontent.com/42792976/49466180-0045ea00-f7c5-11e8-90d8-242314cdf584.png)

- **Step 8**: User now needs to compute the noise statistics from restored image. Please follow the same procedure in step 5. The result of this step will be the histogram of the restored image

![image](https://user-images.githubusercontent.com/42792976/49466373-806c4f80-f7c5-11e8-9c36-90be10cd7811.png)

- **Step 9**: Select "Compare Histogram" to compare the noise statistic from the degraded image to restored image. Note that, if user selects "filter option" back in step 4, the compare histogram will not work because it does not have anything to compare to. 

![image](https://user-images.githubusercontent.com/42792976/49466427-a691ef80-f7c5-11e8-8b03-72f50ed7f2e0.png)
