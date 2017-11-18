#include "GCDTest.h"

/******************************************************************************
 *
 * Class 'GCDTest' for testing gcd algorithms.
 *
 * This functions mostly as a wrapper for code that will generate pairs of
 * random numbers and then compute the gcd. We also have the option of
 * applying tests for correctness.
 *
 * The primary entry point for this class is intended to be the function
 * 'runTheTests', which will invoke specific tests.
 *
 * FOR INFORMATION REGUARDING ADDITIONAL LIBRARIES AND FUNCTIONS, PLEASE
 * SEE "GCDTest.h"
 * 
 * Author: Duncan Buell
 * Editor: Audrey Danielle Talley
 * Last Modified: 6 February 2016
 *
 *
 * [COMMENTS IN THIS PROGRAM THAT ARE IN SQUARE BRACKETS AND ALL CAPS ARE
 *  NOT INTENDED TO BE REAL COMMENTS IN THE CODE BUT RATHER DIRECTIONS TO 
 *  YOU, THE 350 STUDENTS, ABOUT HOW TO DOCUMENT CODE AND WHAT TO DOCUMENT.]
 * [THERE MUST ALWAYS BE A HEADER FOR EVERY CLASS THAT OUTLINES THE OVERALL
 *  STRUCTURE OF WHAT'S IN THE CLASS. YOU MUST ALWAYS HAVE YOUR NAME AND YOU
 *  SHOULD ALWAYS HAVE THE DATE OF LAST EDIT.]
 *
**/

/******************************************************************************
 * Constructor
**/
GCDTest::GCDTest()
{
}

/******************************************************************************
 * Destructor
**/
GCDTest::~GCDTest()
{
}

/******************************************************************************
 * General functions.
**/

/******************************************************************************
 * Function to convert a binary number to its bit string.
 * We will add the remainder of dividing the number "n"
 * by 2 to the stack "tempBits" until "n" is zero. Then,
 * we will remove the top element of the stack and add it
 * to the string "bits" to get the final binary conversion.
**/
string GCDTest::convertToBinary(LONG n)
{
  string bits = "";
  stack<int> tempBits; //this stack will store the bits as the math and
  //conversions are done.
  while(n > 0 ){ //getting the reverse binary translation
    tempBits.push( n%2);
    n = n >> 1;
  }
  while(!tempBits.empty()){ //putting the translation in order
    bits += Utils::Format(tempBits.top()); //removing the int from the stack,
    //converting it to a string, and adding it to the binary conversion string
  }
  return bits;
}

/******************************************************************************
 * Function to create the numbers to be tested.
**/
void GCDTest::createNumbers(LONG howManyTests, LONG maxTestNumberSize)
{
  int bitLength = 0;

  cout << "create " << howManyTests << " records" << endl;

  bitLength = this->getBitLength(maxTestNumberSize) + 1;
  for (int i = 0; i < bitLength; ++i)
  {
    this->bitLengthFreqs.push_back(0L);
  }

  // we can hard code the 200 because these are fractions
  for (int i = 0; i < 201; ++i)
  {
    this->shiftFracFreqs.push_back(0L);
  }

  MyRandom myRandom;
  LONG upperLimit = maxTestNumberSize;

  for (int i = 0; i < howManyTests; ++i)
  {
    LONG a = myRandom.randomUniformInt(0, upperLimit);
    LONG b = myRandom.randomUniformInt(0, upperLimit);
    this->veca.push_back(a);
    this->vecb.push_back(b);

    bitLength = this->getBitLength(a);
    ++(this->bitLengthFreqs.at(bitLength));

    bitLength = this->getBitLength(b);
    ++(this->bitLengthFreqs.at(bitLength));
  }

  cout << "done with creation of " << howManyTests << " pairs" << endl;
}

/******************************************************************************
 * Function to format a progress line.
**/
string GCDTest::formatProgress(LONG sub, LONG a, LONG b,
                               LONG g, LONG gbin, LONG g3)
{
  string s = "";
  s += Utils::Format(sub, 11) + " ";
  s += Utils::Format(a, 11) + " ";
  s += Utils::Format(b, 11) + " ";
  s += Utils::Format(g, 6) + " ";
  s += Utils::Format(gbin, 6) + " ";
  s += Utils::Format(g3, 6);
  return s;
}

/**
 * Switch LONGS
 *   This function is used to switch the values of two LONGS
 *
 * Implementation:
 *   -Creates a temporary variable "temp" of type LONG to store
 *    the value of "a"
 *   -Assigns the value of "b" to "a"
 *   -Assigns the value of "temp" to "b"
 * 
 * Paramters:
 *   &a, &b - the two longs to be switched
 * Returns:
 *   void
**/
void GCDTest::switchLONGS( LONG& a, LONG& b){
  LONG temp = a;
  a = b;
  b = temp;
}

/*********************************************************************
 * Binary gcd
 * This computes the gcd of two "LONG" values "a" and "b" using the
 * binary (also known as the subtract and shift) algoriithm.
 * 
 * Implementation of the algorithm:
 *   Preliminary Checks:
 *     -Neither "big" nor "small" can be negative. If either of them 
 *       are, print an error message and return -1.
 *     -If either a or b are zero, return the other number.
 *   Beginning:
 *     -Remove powers of two from "big" until it is an odd number.
 *        Store the number of removed powers in "k_a".
 *     -Remove powers of two from "small" until it is an odd number.
 *        Store the number of removed powers in "k_b".
 *     -If "small" is greater than "big", switch the two numbers.
 *   Loop:
 *     -Condition: Until small is zero
 *     -Subract "big" and "small" and store the absolute value of the
 *       result into "big"
 *     -Shift "big" to the right by one (divide it by two).
 *     -Continue to shift "big" to the right by one until it is an 
 *        odd number. These are the shift that improve efficiency. 
 *        Therefore, we will count each of those shifts and store it
 *        int "free_shift_counter".
 *     -Switch the values of "big" and "small" if small is greater
 *        than big
 *   Closing:
 *     -Find the maximum bit length between "a" and "b" and store it
 *        in "max_bit_length"
 *     -In order to find the correct index in the vector "shiftFracFreqs"
 *        to keep track of the number of free shifts, find the percentage 
 *        of free shifts ("free_shift_counter") per maximum bit length
 *        ("max_bit_length") and save the index as an int ("index")
 *     -Increment the "index" location of "shiftFracFreqs"
 *     -Find the minimum of the count of removed powers of two
 *        (min of "k_a" and "k_b") and store that in "minimum"
 *     -Return the GCD of a and b which is 2 raised to the "minimum"
 *        power multiplied by "big"
 * 
 * Parameters: 
 *   a, b - the values for which to compute the gcd
 * Returns:
 *   the gcd of a and b
 * Other Functions:
 *   LONG GCDTest::switchLONG(LONG& a, LONG& b)
 *   int GCD::Test::getBitLength(LONG n)
**/
LONG GCDTest::gcdBinary(LONG a, LONG b)
{
  int k_a = 0; int k_b = 0; int free_shift_counter = 0; 
  LONG big = a; LONG small = b;
  if( big < 0 || small < 0){
    cerr << "Error: When computing the GCD of two integers, neither "
         << "can be negative.\nSee function \"gcdBinary\" in file "
         << "\"GCDTest.cpp\"\n";
    return -1L;
  }
  if(big == 0L)
    return small;
  else if(small == 0L)
    return big;
  while(big != 0L && big%2 == 0){
    big = big >> 1;
    k_a++; 
  }
  while(small != 0L && small%2 == 0){
    small = small >> 1;
    k_b++;
  }
  if( small > big)
    switchLONGS( big, small );
  while(small != 0){
    big = abs(big - small);
    big = big >> 1;
    while(big != 0L && big%2 == 0){
      big = big >> 1;
      free_shift_counter++;
    }    
   if( small > big)
      switchLONGS(big, small);
  }
  int max_bit_length = max(getBitLength(a), getBitLength(b));
  int index = ((float) free_shift_counter * 100.0/ (float) max_bit_length);
  shiftFracFreqs.at(index)++;
  LONG minimum = min(k_a, k_b);
  return (pow(2, minimum) * big);
}


/*********************************************************************
 * Naive gcd function.
 * This computes the gcd of two 'LONG' values 'a' and 'b' using the
 * standard naive algorithm that uses division.
 *
 * Implementation of the algorithm:
 * We initially assign 'big' <-- 'a' and 'small' <-- 'b'.
 * We then ensure that 'big' and 'small' are nonnegative.
 * If either is zero, then the gcd is the other value.
 * Now loop: 
 *     Set 'rem' to the value of 'big' modulo 'small' 
 *     While 'rem' is still positive:
 *         'big' <-- 'small'         
 *         'small' <-- 'rem'         
 *         'rem' <-- 'big' modulo ''small'         
 *     When the loop finishes, return 'small' as the gcd
 * 
 * Note: We permit 'a' and 'b' to be negative and return the gcd of
 *       the absolute values of 'a' and 'b'.
 * Note: If we start with 'a' < 'b', then the first step just flips the
 *       order, and after that we will always have 'small' < 'big'.
 * Note: The test for 'big' being 0 covers the case when both inputs are 0
 *       and we return 0 as the gcd.
 * Note: The test for 'small' being 0 ensures we don't try to mod down
 *       by 0, which isn't well defined.
 * 
 * Parameters:
 *   a, b - the values for which to compute the gcd
 * Returns::
 *   the gcd of a and b
 *
 * [NOTE CAREFULLY HERE ALL THE 'NOTES'. THEY POINT OUT THE SPECIAL CASES
 *  AND HOW THEY ARE HANDLED.]
**/
LONG GCDTest::gcdNaive(LONG a, LONG b)
{

  LONG big, small, rem;
  big = a;
  small = b;
  if (big < 0L)
    big = -big;
  if (small < 0L)
    small = -small;
  if (0L == big)
    return(small);
  else if (0L == small)
    return(big);
  else
  {
    rem = big % small;
    while (rem != 0L)
    {
      big = small;
      small = rem;
      rem = big % small;
    }
    return(small);
  }
}

/*********************************************************************
 * Get Bit Length
 *  -This function finds the bit length of a long number "n"
 * 
 * Implementation:
 *   Preliminary Checks
 *     -If the given number "n" is zero, return zero
 *     -If the given number "n" is negative, return 32
 *   Function
 *     -Find the result of log base 2 of the number and increment
 *      that number by 1
 *     -Return the integer representation of  the result (like 
 *      floor(result))
 * 
 * Parameters: 
 *  -LONG n (the number you want the bit length of)
 * 
 * Returns
 *  -result (the bit length)
**/
int GCDTest::getBitLength(LONG n)
{
  if (0 == n) return 0; // this is a fudge

  if (n < 0) return 32;

  return ((int) (log2(n) +1));
}

/*********************************************************************
**/
void GCDTest::runTheTests()
{
  double timeNew;
  string timestring;

  // test binary
  // the 'true' variable says we want to do the additional test on
  //     the quotients a/g and b/g to try to verify that in fact our
  //     gcd is correct
  timestring = Utils::timecall("bef binary true", timeNew);
  cout << timestring << endl;
  testBinary(true);
  timestring = Utils::timecall("aft binary true", timeNew);
  cout << timestring << endl;

  cout << "done with the computation" << endl;
}

/*********************************************************************
 * This function simply turns the 'vector' of bit length frequencies
 * into a readable formatted string for printing by the function
 * that called it.
**/
string GCDTest::stringifyBitLengthFreqs()
{
  string s = "Frequencies of bit lengths\n";
  int i = 0;
  for(vector<LONG>::iterator iter = bitLengthFreqs.begin(); 
            iter != bitLengthFreqs.end(); iter++, i++){
    if( *iter != 0L ){
      s += Utils::Format(to_string(i), 3, "right");
      s += Utils::Format(to_string(*iter), 5, "right");
      s+="\n";
    }
  }
  return s;
}

/*********************************************************************
 * This function simply turns the 'vector' of shift fractions
 * frequencies into a readable formatted string for printing by the
 * function that called it. 
**/
string GCDTest::stringifyShiftFracFreqs()
{
  string s = "Frequencies of shift fractions\n";
  int i = 0;
  for(vector<LONG>::iterator iter = shiftFracFreqs.begin(); 
            iter != shiftFracFreqs.end(); iter++, i++){
    if( *iter != 0L ){
    /*
    	s += ("  " + to_string(i));
    	s += ( "    " + to_string(*iter) + "\n");
    */
      s += Utils::Format(to_string(i), 3, "right");
      s += Utils::Format(to_string(*iter), 5, "right");
      s+="\n";
    }
  }
  s += "\n";  
  return s;
}

/*********************************************************************
**/
void GCDTest::testBinary(bool extraTest)
{
  LONG a, aa, b, bb, g, gg;
  LONG testlimit = (LONG) this->veca.size()/10;

  for (UINT i = 0; i < this->veca.size(); ++i)
  {
    a = this->veca.at(i);
    b = this->vecb.at(i);
    g = this->gcdBinary(a, b);

    if (0 == (i % testlimit))
    {
      cout << this->formatProgress(i, a, b, -1, g, -1) << endl;
    }

    if (extraTest)
    {
      aa = a/g;
      bb = b/g;
      gg = this->gcdNaive(aa, bb);
      if (gg != 1)
      {
        cout << "ERROR " << a << " " << b << " " << g << endl;
        exit(0);
      }
    }
  }
}

