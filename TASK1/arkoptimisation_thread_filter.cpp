#include <bits/stdc++.h>
#include <iostream>

#include <thread>
#include <vector>
#include <atomic>

using namespace std;
#define MAX_THREAD 4
const int sizen =800;
void dot_product(const std::vector<int> &v1, const std::vector<int> &v2, std::atomic<int> &result, int L, int R)
{
    int partial_sum = 0;
    for (int i = L; i < R; ++i)
    {
        partial_sum += v1[i] * v2[i];
    }
    result += partial_sum;
}

std::vector<int> bounds(int parts, int mem)
{
    std::vector<int> bnd;
    int delta = mem / parts;
    int reminder = mem % parts;
    int N1 = 0, N2 = 0;
    bnd.push_back(N1);
    for (int i = 0; i < parts; ++i)
    {
        N2 = N1 + delta;
        if (i == parts - 1)
            N2 += reminder;
        bnd.push_back(N2);
        N1 = N2;
    }
    return bnd;
}
long long costMatrixA[sizen][sizen];
long long costMatrixB[sizen][sizen];

long long productMat[sizen][sizen];
long long MincostMat[sizen][sizen];
long long MaxcostMat[sizen][sizen];

int step_i = 0;

void *multi(void *arg)
{
    int core = step_i++;

    // Each thread computes 1/4th of matrix multiplication
    for (int i = core * sizen / 4; i < (core + 1) * sizen / 4; i++)
        for (int j = 0; j < sizen; j++)
            for (int k = 0; k < sizen; k++)
                productMat[i][j] += MincostMat[i][k] * MaxcostMat[k][j];
}

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

    pthread_t threads[MAX_THREAD];


    for (int i = 0; i < MAX_THREAD; i++)
    {
        int *p;
        pthread_create(&threads[i], NULL, multi, (void *)(p));
    }

    // joining and waiting for all threads to complete
    for (int i = 0; i < MAX_THREAD; i++)
        pthread_join(threads[i], NULL);

   
    //filter of size 4 x n
    vector<int> filterArray;
    for (i = 0; i < 4*sizen; i++)
    {

        filterArray.push_back(rand() % 2);
    }

    // matrix of dimension (sizen/c) x 1 where c = 4
    int nr_threads = 2;
   // cout<<"yes";
    long long finalMat[sizen / 4];
    // applying the filter
    for (i = 0; i <=sizen - 4; i += 4)
    {
       // long long sum = 0;
        vector<int> g1;
        atomic<int> result(0);
        vector<thread> thread1;
        vector<int> limits = bounds(nr_threads, 4 * sizen);
    
        // dot product of 4xn portion of productMat
        for (j = 0; j < sizen; j++)
        {
            for (int filterRow = 0; filterRow < 4; filterRow++)
            {
                g1.push_back(productMat[i + filterRow][j]);
            }
        }

       

        for (int k = 0; k < nr_threads; ++k)
        {
            thread1.push_back(thread(dot_product, ref(g1), ref(filterArray), ref(result), limits[k], limits[k + 1]));
        }
      
            for (auto &t : thread1)
            {if(t.joinable())
               { t.join();
               
               }    
            }
            
       
        finalMat[i / 4] = result;
       
      //  thread1.clear();
        
    
    }
    return 0;
}