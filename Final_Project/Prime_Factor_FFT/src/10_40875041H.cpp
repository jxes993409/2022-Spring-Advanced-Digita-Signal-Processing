#include <iostream>
#include <vector>
#include <complex>
#include "./lib/readfile.h"
#include "./lib/compute.h"

int main(int argc, char *argv[])
{
  int N;
  std::vector<std::complex<double>> x;
  std::vector<prime_factor> prime;
  // read file
  if(!read_input(argv[1], &N, x)) {return -1;}
  // do prime factorization for N
  prime_factorization(N, prime);
  std::vector<std::complex<double>> X(N);
  // do Prime Factor FFT
  Prime_Factor_FFT(N, prime, x, X);
  // output X
  for (auto i: X) std::cout << i << std::endl;
  return 0;
}