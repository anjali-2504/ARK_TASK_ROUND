#include <iostream>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
using namespace std;


const int sizen = 256;
#define MAX_THREAD 4

long long costMatrixA[sizen][sizen];
long long costMatrixB[sizen][sizen];

long long productMat[sizen][sizen];
long long MincostMat[sizen][sizen];
long long MaxcostMat[sizen][sizen];

int step_i = 0;


typedef long long datatype;


typedef datatype mat[sizen][sizen]; // mat[2**M,2**M]  for divide and conquer mult.
typedef struct
{
        int ra, rb, ca, cb;
} corners; // for tracking rows and columns.
// A[ra..rb][ca..cb] .. the 4 corners of a matrix.
 
// set A[a] = I
void identity(long long A[][sizen], corners a)
{
    int i, j;
    for (i = a.ra; i < a.rb; i++)
        for (j = a.ca; j < a.cb; j++)
            A[i][j] = (datatype) (i == j);
}
 
// set A[a] = k
void set(long long A[][sizen], corners a, datatype k)
{
    int i, j;
    for(i = a.ra; i < a.rb; i++)
        for (j = a.ca; j < a.cb; j++)
            A[i][j] = k;
}
 
// set A[a] = [random(l..h)].

// Print A[a]

 
// C[c] = A[a] + B[b]
void add(long long A[][sizen], long long B[][sizen],long long C[][sizen], corners a, corners b, corners c)
{
    int rd = a.rb - a.ra;
    int cd = a.cb - a.ca;
    int i, j;
    for (i = 0; i < rd; i++)
    {
        for (j = 0; j < cd; j++)
        {
            C[i + c.ra][j + c.ca] = A[i + a.ra][j + a.ca] + B[i + b.ra][j
 + b.ca];
        }
    }
}
 
// C[c] = A[a] - B[b]
void sub(long long A[][sizen],long long B[][sizen],long long C[][sizen], corners a, corners b, corners c)
{
    int rd = a.rb - a.ra;
    int cd = a.cb - a.ca;
    int i, j;
    for (i = 0; i < rd; i++)
    {
        for (j = 0; j < cd; j++)
        {
            C[i + c.ra][j + c.ca] = A[i + a.ra][j + a.ca] - B[i + b.ra][j
                    + b.ca];
        }
    }
}
 
// Return 1/4 of the matrix: top/bottom , left/right.
void find_corner(corners a, int i, int j, corners *b)
{
    int rm = a.ra + (a.rb - a.ra) / 2;
    int cm = a.ca + (a.cb - a.ca) / 2;
    *b = a;
    if (i == 0)
        b->rb = rm; // top rows
    else
        b->ra = rm; // bot rows
    if (j == 0)
        b->cb = cm; // left cols
    else
        b->ca = cm; // right cols
}
 
// Multiply: A[a] * B[b] => C[c], recursively.
void mul(long long A[][sizen],long long B[][sizen],long long C[][sizen], corners a, corners b, corners c)
{
    corners aii[2][2], bii[2][2], cii[2][2], p;
    long long  S[sizen][sizen], T[sizen][sizen];
    mat P[7];
    int i, j, m, n, k;
 
    // Check: A[m n] * B[n k] = C[m k]
    m = a.rb - a.ra;
 assert(m==(c.rb-c.ra));
    n = a.cb - a.ca;
  assert(n==(b.rb-b.ra));
    k = b.cb - b.ca;
   assert(k==(c.cb-c.ca));
   assert(m>0);
 
    if (n == 1)
    {
        C[c.ra][c.ca] += A[a.ra][a.ca] * B[b.ra][b.ca];
        return;
    }
 
    // Create the 12 smaller matrix indexes:
    //  A00 A01   B00 B01   C00 C01
    //  A10 A11   B10 B11   C10 C11
    for (i = 0; i < 2; i++)
    {
        for (j = 0; j < 2; j++)
        {
            find_corner(a, i, j, &aii[i][j]);
            find_corner(b, i, j, &bii[i][j]);
            find_corner(c, i, j, &cii[i][j]);
        }
    }
    
    p.ra = p.ca = 0;
    p.rb = p.cb = m / 2;
 
#define LEN(A) (sizeof(A)/sizeof(A[0]))
    for (i = 0; i < LEN(P); i++)
        set(P[i], p, 0);
 
#define ST0 set(S,p,0); set(T,p,0)
 
    // (A00 + A11) * (B00+B11) = S * T = P0
    ST0;
    add(A, A, S, aii[0][0], aii[1][1], p);
    add(B, B, T, bii[0][0], bii[1][1], p);
    mul(S, T, P[0], p, p, p);
 
    // (A10 + A11) * B00 = S * B00 = P1
    ST0;
    add(A, A, S, aii[1][0], aii[1][1], p);
    mul(S, B, P[1], p, bii[0][0], p);
 
    // A00 * (B01 - B11) = A00 * T = P2
    ST0;
    sub(B, B, T, bii[0][1], bii[1][1], p);
    mul(A, T, P[2], aii[0][0], p, p);
 
    // A11 * (B10 - B00) = A11 * T = P3
    ST0;
    sub(B, B, T, bii[1][0], bii[0][0], p);
    mul(A, T, P[3], aii[1][1], p, p);
 
    // (A00 + A01) * B11 = S * B11 = P4
    ST0;
    add(A, A, S, aii[0][0], aii[0][1], p);
    mul(S, B, P[4], p, bii[1][1], p);
 
    // (A10 - A00) * (B00 + B01) = S * T = P5
    ST0;
    sub(A, A, S, aii[1][0], aii[0][0], p);
    add(B, B, T, bii[0][0], bii[0][1], p);
    mul(S, T, P[5], p, p, p);
 
    // (A01 - A11) * (B10 + B11) = S * T = P6
    ST0;
    sub(A, A, S, aii[0][1], aii[1][1], p);
    add(B, B, T, bii[1][0], bii[1][1], p);
    mul(S, T, P[6], p, p, p);
 
    // P0 + P3 - P4 + P6 = S - P4 + P6 = T + P6 = C00
    add(P[0], P[3], S, p, p, p);
    sub(S, P[4], T, p, p, p);
    add(T, P[6], C, p, p, cii[0][0]);
 
    // P2 + P4 = C01
    add(P[2], P[4], C, p, p, cii[0][1]);
 
    // P1 + P3 = C10
    add(P[1], P[3], C, p, p, cii[1][0]);
 
    // P0 + P2 - P1 + P5 = S - P1 + P5 = T + P5 = C11
    add(P[0], P[2], S, p, p, p);
    sub(S, P[1], T, p, p, p);
    add(T, P[5], C, p, p, cii[1][1]);
 
}



void initialise()
{
    for(int i=0;i<sizen;i++)
    for(int j=0;j<sizen;j++)
    {
        MincostMat[i][j]=0;
        MaxcostMat[i][j]=0;
    }
}


//Simple recursion  which returns the minimum cost of going from i,j to n,n
long long FindMinCostA(int i, int j, int n)
{
    //going out of bounds
    if (i >= n||j>=n)
        return 0;
    //going out of bounds
   // else if (j >= n)
     //   return 0;
    //reaching the last cell
    else if (i == n - 1 && j == n - 1)
        {MincostMat[i][j]=costMatrixA[i][j];
            return costMatrixA[i][j];}
    //going down or right
    else if(MincostMat[i][j]==0)
    { MincostMat[i][j]=costMatrixA[i][j] + min(FindMinCostA(i + 1, j, n), FindMinCostA(i, j + 1, n));
    return MincostMat[i][j];
    }
    else 
    return MincostMat[i][j];
}
//Simple recursion which returns the maximum cost of going from i,j to n,n
long long FindMaxCostB(int i, int j, int n)
{
    //going out of bounds
    if (i >= n||j>=n)
        return 0;
    //going out of bounds
    //if (j >= n)
        //return 0;
    //reaching the last cell
    if (i == n - 1 && j == n - 1)
        {MaxcostMat[i][j]=costMatrixB[i][j];
            return costMatrixB[i][j];}
    //going down or right
    else if(MaxcostMat[i][j]==0)
    { MaxcostMat[i][j]=costMatrixB[i][j] + max(FindMaxCostB(i + 1, j, n), FindMaxCostB(i, j + 1, n));
    return MaxcostMat[i][j];
    }
    else 
    return MaxcostMat[i][j];
}



int main()
{     int i, j, k;
    initialise();
    
  //  srand(time(0));
    // initialisation
    for (i = 0; i < sizen; i++)
    {
        for (j = 0; j < sizen; j++)
        {
            costMatrixA[i][j] = 1 + rand() % 10;
            costMatrixB[i][j] = 1 + rand() % 10;
            productMat[i][j] = 0;
        }
    }

   
 
    for (i=0;i<sizen;i++)
    {
        for(j=0;j<sizen;j++)
        {
            MincostMat[i][j]=FindMinCostA(i,j,sizen);
          //  matA[i][j]=MincostMat[i][j];
            MaxcostMat[i][j]=FindMaxCostB(i,j,sizen);
           // matB[i][j]=MaxcostMat[i][j];           
        }
    }

    
    corners ai = { 0, sizen, 0, sizen };
    corners bi = { 0, sizen, 0, sizen };
    corners ci = { 0, sizen, 0, sizen };
    //srand(time(0));
     
    mul(MincostMat, MaxcostMat, productMat, ai, bi, ci);
  
      //filter of size 4 x n
    long long filterArray[4][sizen];
    for (i = 0; i < 4; i++)
    {
        for (j = 0; j < sizen; j++)
            filterArray[i][j] = rand() % 2;
    }
    // matrix of dimension (sizen/c) x 1 where c = 4
    long long finalMat[sizen / 4];
    // applying the filter
    for (i = 0; i < sizen - 4; i += 4)
    {
        long long sum = 0;
        // dot product of 4xn portion of productMat
        for (j = 0; j < sizen; j++)
        {
            for (int filterRow = 0; filterRow < 4; filterRow++)
            {
                sum += productMat[i + filterRow][j];
                if(filterArray[filterRow][j]!=1)
                {
                    sum-=productMat[i + filterRow][j];
                }
            }

        } finalMat[i / 4] = sum;
    }
       return 0;
}