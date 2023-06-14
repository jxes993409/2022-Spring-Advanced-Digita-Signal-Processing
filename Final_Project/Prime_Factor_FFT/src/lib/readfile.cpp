#include <iostream>
#include <fstream>
#include <vector>
#include <complex>
#include "readfile.h"

bool read_input(const char path[], int *N, std::vector<std::complex<double>> &x)
{
  std::ifstream ifs(path, std::ios::in);
  if (!ifs.is_open())
  {
    std::cout << "Failed to open file." << std::endl;
    return false; // EXIT_FAILURE
  }
  double real, imag;
  ifs >> *N;
  while (ifs >> real >> imag) {x.push_back({real, imag});}
  ifs.close();
  return true;
}