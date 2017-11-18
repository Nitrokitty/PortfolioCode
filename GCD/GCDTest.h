/****************************************************************
 * Header file for the gcd test.
 *
 * Author/copyright:  Duncan Buell
 * Editor: Audrey Danielle Talley
 * Date: 6  February 2016
 *
 * Additional Function(s):
 *   switchLONGS(LONG& a, LONG& b)
 *     - This function will switch the address locations for two 
 *       LONG numbers
 *     - This function is used in the "gcdBinary" function
 *   log2(double x)
 *     - This function will return the log base 2 of a 
 *       double number
 *     - This function is used in the "getBitLength" function
 *     - This function is located in the math library and
 *       therefore the "math.h" header file must be included
 *   stack<class T> stack_name
 *     - This function will create a stack in memory to store
 *       values of type "T"
 *     - This function is used in the "convertToBinary" function
 *     - This function is located in the stack library and 
 *       therefore the "stack.h" header file must be included
 *     
 * Additional Libraries:
 *    Math.h
 *     - For usage see "log2" in the above section "Additional 
 *       Functions"
 *    Stack.h
 *     - For usage see "stack" in the above section "Additional
 *       Functions"
 *
**/

#ifndef GCDTEST_H
#define GCDTEST_H

#include <iostream>
#include <vector>
#include <math.h>
#include <stack>
using namespace std;

#include "../../Utilities/Scanner.h"
#include "../../Utilities/ScanLine.h"

#include "MyRandom.h"

class GCDTest
{
public:
  GCDTest();
  virtual ~GCDTest();

  void createNumbers(LONG howManyTests, LONG maxTestNumberSize);
  void runTheTests();
  string stringifyBitLengthFreqs();
  string stringifyShiftFracFreqs();

private:
  vector<LONG> bitLengthFreqs;
  vector<LONG> shiftFracFreqs;
  vector<LONG> veca;
  vector<LONG> vecb;

  string convertToBinary(LONG n);
  string formatProgress(LONG sub, LONG a, LONG b,
                        LONG g, LONG gbin, LONG g3);
  LONG gcdBinary(LONG a, LONG b);
  LONG gcdNaive(LONG a, LONG b);
  void switchLONGS(LONG& a, LONG& b);
  int getBitLength(LONG n);

  void testBinary(bool extraTest);

};

#endif
