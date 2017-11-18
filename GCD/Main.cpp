#include "Main.h"

/****************************************************************
 * Main program for Homework 1.
 *
 * Author/copyright:  Duncan Buell. All rights reserved.
 * Submitted by: Audrey Danielle Talley
 * Last Modified: 17 January 2016
 *
**/

static const string TAG = "Main: ";

/*********************************************************************
**/
int main(int argc, char *argv[])
{
  LONG howManyTests;
  LONG maxTestNumberSize;
  double timeNew = 0.0;
  string dataFileName = "";
  string timeString = "";

  Scanner inScanner;

  GCDTest gcdTest;

  Utils::CheckArgs(1, argc, argv, "datafilefilename");
  dataFileName = static_cast<string>(argv[1]);

  cout << TAG << "Beginning execution\n";

  cout << TAG << "datafile  '" << dataFileName << "'\n";

  timeString = Utils::timecall("beginning", timeNew);
  cout << timeString << endl;

  inScanner.openFile(dataFileName);

  howManyTests = inScanner.nextLONG();
  maxTestNumberSize = inScanner.nextLONG();

  cout << "start the computation" << endl;


  gcdTest = GCDTest();
  gcdTest.createNumbers(howManyTests, maxTestNumberSize);


  timeString = Utils::timecall("done creation", timeNew);
  cout << timeString << endl;

  timeString = Utils::timecall("before gcdtest", timeNew);
  cout << timeString << endl;

  gcdTest.runTheTests();

  timeString = Utils::timecall("after gcdtest", timeNew);
  cout << timeString << endl;
  cout << gcdTest.stringifyBitLengthFreqs() << endl;
  cout << gcdTest.stringifyShiftFracFreqs() << endl;
  
  cout << TAG << "Ending execution\n";

  timeString = Utils::timecall("ending", timeNew);
  cout << timeString << endl;

  return 0;
}


