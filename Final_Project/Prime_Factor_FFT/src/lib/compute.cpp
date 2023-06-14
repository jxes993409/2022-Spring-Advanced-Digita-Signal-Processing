#include <vector>
#include <cmath>
#include "compute.h"

void prime_factorization(int N, std::vector<prime_factor> &prime)
{
  prime_factor temp;
  if (N == 1) {prime.push_back(temp);}
  for (int i = 0; N > 1; i++)
  {
    int count = 0;
    while (N % prime_number_table[i] == 0)
    {
      N /= prime_number_table[i];
      count++;
    }
    temp.num = prime_number_table[i];
    temp.pow = count;
    if (count) {prime.push_back(temp);}
  }
}

void Prime_Factor_FFT(int N, std::vector<prime_factor> prime, std::vector<std::complex<double>> x, std::vector<std::complex<double>> &X)
{
  int P1 = 1;
  int P2 = 1;
  // N is a prime number, do N-points DFT
  if(prime.size() == 1 && prime[0].pow == 1)
  {
    for (int m = 0; m < N; m++)
    {
      for (int n = 0; n < N; n++)
      {
        X[m] += x[n] * std::exp(std::complex<double>{0, -1} * 2.0 * M_PI * double(m * n) / double(N));
      }
    }
  }
  // N = P1 * P2, P1 is not prime to P2, need twiddle factor
  else if(prime.size() == 1 && prime[0].pow != 1)
  {
    P1 = pow(prime[0].num, prime[0].pow / 2);
    P2 = pow(prime[0].num, prime[0].pow - prime[0].pow / 2);
    for (int m1 = 0; m1 < P2; m1++)
    {
      for (int m2 = 0; m2 < P1; m2++)
      {
        std::complex<double> G2;
        // do P1-points DFT P2 times
        for (int n2 = 0; n2 < P1; n2++)
        {
          std::vector<std::complex<double>> G1(P1);
          std::complex<double> twiddle_factor = std::exp(std::complex<double>{0, -1} * 2.0 * M_PI * double(m1 * n2) / double(N));
          // do P2-points DFT P1 times
          for (int n1 = 0; n1 < P2; n1++)
          {
            G1[n2] += x[n1 * P1 + n2] * std::exp(std::complex<double>{0, -1} * 2.0 * M_PI * double(m1 * n1) / double(P2)); // exp^(-j*2pi*m1*n1/P2)
          }
          G2 += G1[n2] * std::exp(std::complex<double>{0, -1} * 2.0 * M_PI * double(m2 * n2) / double(P1)) * twiddle_factor; // exp^(-j*2pi*m2*n2/P2)
        }
        X[m1 + m2 * P2] = G2;
      }
    }
  }
  // N = P1 * P2, P1 is prime to P2
  else
  {
    for(size_t i = 0; i < prime.size(); i += 2)
    {
      P1 *= pow(prime[i].num, prime[i].pow);
      if((i + 1) == prime.size()) {break;}
      P2 *= pow(prime[i + 1].num, prime[i + 1].pow);
    }
    // find m1[1] and m2[1] to satisfy (m1[1]*P1 + m2[1]*P2) % N = 1
    std::vector<m1_m2> m1_m2_vec(N);
    for (int m1 = 0; m1 < P2; m1++)
    {
      for (int m2 = 0; m2 < P1; m2++)
      {
        if ((m1 * P1 + m2 * P2) % N == 1)
        {
          m1_m2_vec[1].m1 = m1;
          m1_m2_vec[1].m2 = m2;
          goto finish;
        }
      }
    }
    finish:
    // example, if i = 3, then (((m1[1]*3) % P2)*P1 + ((m2[1]*3) % P1)*P2) % N = 3
    // hence, m1[3] = (m1[1]*3) % P2, m2[3] = (m2[1]*3) % P1
    for (int i = 2; i < N; i++)
    {
      m1_m2_vec[i].m1 = (i * m1_m2_vec[1].m1) % P2;
      m1_m2_vec[i].m2 = (i * m1_m2_vec[1].m2) % P1;
    }
    for (int m = 0; m < N; m++)
    {
      int m1 = m1_m2_vec[m].m1;
      int m2 = m1_m2_vec[m].m2;
      std::complex<double> G2;
      // do P1-points DFT P2 times
      for (int n2 = 0; n2 < P1; n2++)
      {
        std::vector<std::complex<double>> G1(P1);
        // do P2-points DFT P1 times
        for (int n1 = 0; n1 < P2; n1++)
        {
          G1[n2] += x[(n1 * P1 + n2 * P2) % N] * std::exp(std::complex<double>{0, -1} * 2.0 * M_PI * double(m1 * P1 * n1) / double(P2)); // exp^(-j*2pi*m1*P1*n1/P2)
        }
        G2 += G1[n2] * std::exp(std::complex<double>{0, -1} * 2.0 * M_PI * double(m2 * P2 * n2) / double(P1)); // exp^(-j*2pi*m2*P2*n2/P1)
      }
      X[m] = (G2);
    }
  }
}