#include "MyRandom.h"

/******************************************************************************
 *3456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789
 * Class 'MyRandom' for the queueing theory computation.
 *
 * This class has the CERT-acceptable random number functions for:
 *   (double) normal distribution from a mean and std dev
 *   (double) uniform distribution from a lower to an upper bound
 *   (int) uniform distribution from a lower to an upper bound
 *
 * Author: Duncan A. Buell
 * Submitted by: Audrey Danielle Talley
 * Date last modified: 20 April 2015
**/

/******************************************************************************
 * Constructor
**/
MyRandom::MyRandom()
{
  std::default_random_engine generator;
}

/******************************************************************************
 * Destructor
**/
MyRandom::~MyRandom()
{
}

/******************************************************************************
 * Accessors and Mutators
**/

/******************************************************************************
 * General functions.
**/

/******************************************************************************
 * Function 'randomNormal'.
 * This generates 'double' random numbers normally distributed with
 * mean 'mean' and standard deviation 'dev'.
 *
 * Parameters:
 *   mean - the mean of the normally distributed RNs
 *   dev - the standard deviation of the normally distributed RNs
 *
 * Returns:
 *   the random number as a 'double'
**/
double MyRandom::randomNormal(double mean, double dev)
{
  assert(dev >= 0.0);
  std::normal_distribution<double> distribution(mean, dev);
  double r = distribution(this->generator);
  return r;
}

/******************************************************************************
 * Function 'randomUniformDouble'.
 * This generates 'double' random numbers uniformly distributed from
 * 'lower' to 'upper' inclusive.
 *
 * Parameters:
 *   lower - the smallest value of the RNs
 *   upper - the largest value of the RNs
 *
 * Returns:
 *   the random number as a 'double'
**/
double MyRandom::randomUniformDouble(double lower, double upper)
{
  assert(lower <= upper);
  std::uniform_real_distribution<double> distribution(lower, upper);
  double r = distribution(this->generator);
  return r;
}

/******************************************************************************
 * Function 'randomUniformInt'.
 * This generates 'int' random numbers uniformly distributed from
 * 'lower' to 'upper' inclusive.
 *
 * Parameters:
 *   lower - the smallest value of the RNs
 *   upper - the largest value of the RNs
 *
 * Returns:
 *   the random number as an 'int'
**/
int MyRandom::randomUniformInt(int lower, int upper)
{
  assert(lower <= upper);
  std::uniform_int_distribution<int> distribution(lower, upper);
  int r = distribution(this->generator);
  return r;
}
