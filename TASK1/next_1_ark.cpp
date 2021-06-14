#include <bits/stdc++.h>
#include <iostream>

using namespace std;
const int sizen = 500;

long long costMatrixA[sizen][sizen];
long long costMatrixB[sizen][sizen];

long long productMat[sizen][sizen];
long long MincostMat[sizen][sizen];
long long MaxcostMat[sizen][sizen];
void initialise()
{
    for (int i = 0; i < sizen; i++)
        for (int j = 0; j < sizen; j++)
        {
            MincostMat[i][j] = 0;
            MaxcostMat[i][j] = 0;
        }
}

//Simple recursion  which returns the minimum cost of going from i,j to n,n
long long FindMinCostA(int i, int j, int n)
{
    //going out of bounds
    if (i >= n || j >= n)
        return 0;
    //going out of bounds
    // else if (j >= n)
    //   return 0;
    //reaching the last cell
    else if (i == n - 1 && j == n - 1)
    {
        MincostMat[i][j] = costMatrixA[i][j];
        return costMatrixA[i][j];
    }
    //going down or right
    else if (MincostMat[i][j] == 0)
    {
        MincostMat[i][j] = costMatrixA[i][j] + min(FindMinCostA(i + 1, j, n), FindMinCostA(i, j + 1, n));
        return MincostMat[i][j];
    }
    else
        return MincostMat[i][j];
}
//Simple recursion which returns the maximum cost of going from i,j to n,n
long long FindMaxCostB(int i, int j, int n)
{
    //going out of bounds
    if (i >= n || j >= n)
        return 0;
    //going out of bounds
    //if (j >= n)
    //return 0;
    //reaching the last cell
    if (i == n - 1 && j == n - 1)
    {
        MaxcostMat[i][j] = costMatrixB[i][j];
        return costMatrixB[i][j];
    }
    //going down or right
    else if (MaxcostMat[i][j] == 0)
    {
        MaxcostMat[i][j] = costMatrixB[i][j] + max(FindMaxCostB(i + 1, j, n), FindMaxCostB(i, j + 1, n));
        return MaxcostMat[i][j];
    }
    else
        return MaxcostMat[i][j];
}

int main()
{
    int i, j, k;
    initialise();

    srand(time(0));
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

    for (i = 0; i < sizen; i++)
    {
        for (j = 0; j < sizen; j++)
        {
            MincostMat[i][j] = FindMinCostA(i, j, sizen);
            //  matA[i][j]=MincostMat[i][j];
            MaxcostMat[i][j] = FindMaxCostB(i, j, sizen);
            // matB[i][j]=MaxcostMat[i][j];
        }
    }
    int jj, kk, bsize=4;
    long long sum;
    for (jj = 0; jj < sizen; jj += bsize)
    {
        for (i = 0; i < sizen; i++)
            for (j = jj; j < min(jj + bsize, sizen); j++)
                productMat[i][j] = 0;
        for (kk = 0; kk < sizen; kk += bsize)
        {
            for (i = 0; i < sizen; i++)
            {
                for (j = jj; j < min(jj + bsize, sizen); j++)
                {
                    sum = 0;
                    for (k = kk; k < min(kk + bsize, sizen); k++)
                    {
                        sum += MincostMat[i][k] * MaxcostMat[k][j];
                    }
                    productMat[i][j] += sum;
                }
            }
        }
    }
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
                if (filterArray[filterRow][j] != 1)
                {
                    sum -= productMat[i + filterRow][j];
                }
            }
        }
        finalMat[i / 4] = sum;
    }
    return 0;
}
