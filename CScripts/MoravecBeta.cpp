#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <string>
#include <string.h>
#include <time.h>

using namespace std;
//input 0 = call
//input 1 = filename: The file should contain one line of data delimited by spaces
//input 2 = width
//input 3 = height
//input 4 = radius

//Inialize functions
void getSection(float in[], float out[], int, int, int);
void calcDifference(float in1[], float in2[], float out[], int, int, int);
void calcSquare(float in[], float out[], int, int, int);
float getSum( float on[], int out, int, int);

int main(int argc, char *argv[])
{
	//clock
        double begin = clock();

	//initialization
	cout << "Initializing Variables\n";
	char *cTemp = new char[10];
	char *fileName = new char[50];
        snprintf(cTemp, 10, "%s", argv[2]);      //changing the data type of the file name of the input array to a string
        int width = atoi(cTemp); //need to convert the image width from char -> number
        snprintf(cTemp, 10, "%s", argv[3]);      //changing the data type of the file name of the input array to a string
        int height = atoi(cTemp);
        snprintf(cTemp, 10, "%s", argv[4]);      //changing the data type of the file name of the input array to a string
        int radius = atoi(cTemp);
	int size = (sizeof(argv[1])*sizeof(char));
	char *argLine = new char[size];
        snprintf(argLine, size, "%s", argv[1]);    //changing the data type of the file name of the input array to a string
	string line = string(argLine);

	//array setup
	cout << "Setting up array\n";
	float *image = new float[height*width];
	string num;
	for(int i = 0; i < width*height; i++){
		num = line.substr(0, line.find(" "));
		image[i] = atoi(num.c_str());
		line = line.substr(line.find(" ")+1, line.length());
	}

	//Function Arrays
	cout << "setting up array variables\n";
	float *moravec = new float[height*width];
	memset(moravec, 0, width*height*sizeof(float));
	float *piece = new float[(radius*2+1)*(radius*2+1)];
	float *section = new float[(radius*2+1)*(radius*2+1)];
	float *temp = new float[(radius*2+1)*(radius*2+1)];
	
	//Looping Through Input
	cout << "Looping\n";
	for(int j = radius*2; j < height-radius*2; j++){ 
		for( int i = radius*2; i < width-radius*2; i++){
			getSection( image, piece, (j*width)+i, radius, width);
			
			//loop through section 
			for( int jj = -radius; jj <= radius; jj++){
				for( int ii = -radius; ii <= radius; ii++){
					//section operations
					getSection( image, section, (j+jj)*width + i+ii, radius, width);
					calcDifference( piece, section, temp, 0, radius, (radius*2+1)*(radius*2+1)); 
					calcSquare(temp, temp, 0, radius, (radius*2+1)*(radius*2+1));
					int fin = getSum(temp, 0, radius, (radius*2+1)*(radius*2+1));					
					//update output
					moravec[(j*width)+i] += fin;

				}//end ii
			}//end jj

		}//end for i
	}//end for j
	fstream outputFile;
	outputFile.open("results.txt", fstream::out);
	for( int i = 0; i < width*height; i++){
		outputFile << moravec[i];
		if( (i+1)%width == 0 && (i+1) != width*height){
			outputFile << endl;
		}
		else{
			outputFile << " ";
		}
	}//end output Array

	outputFile.close();
	//clean up
	delete[] moravec;
	delete[] piece;
	delete[] section;
	delete[] temp;
	delete[] cTemp;
	delete[] argLine;
	delete[] fileName;

	fstream timeFile;
	timeFile.open("time.txt", ios_base::app);
	timeFile << (clock() - begin)/(double) CLOCKS_PER_SEC << endl;
	timeFile.close();

	return 0;
}//end main



//functions
void getSection( float oldArray[], float newArray[], int index, int radius, int width){
	int row = index / (width);
	int col = index % (width);
	int newIndex = 0;
	for(int j = - radius; j <= radius; j++){
		for( int i = - radius; i <= radius; i++){
			newArray[newIndex] = oldArray[(col+j)*width+(row+i)];
			newIndex++;
		}
	}
}//end getSection

void calcDifference( float a1[], float a2[], float newArray[], int index, int radius, int width){
	for( int i = index; i < width; i++)
		newArray[i] = a1[i] - a2[i];
}//end calcDifference

void calcSquare( float a[], float newArray[], int index, int radius, int width){
	for( int i = index; i < width; i++)
		newArray[i] = (a[i])*(a[i]);
}//end calcSquare

float getSum( float a[], int index, int radius, int width){
	int sum = 0;
	for( int i = index; i < width; i++)
		sum += a[i];
	return sum;
}//end getSum
