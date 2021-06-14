// C++ program to get least cost path in a grid from
// top-left to bottom-right
#include <bits/stdc++.h>
#include <iostream>

using namespace std;
const int sizen = 500;
#define MAX_THREAD 4

long long costMatrixA[sizen][sizen];
long long costMatrixB[sizen][sizen];

long long productMat[sizen][sizen];
long long MincostMat[sizen][sizen];
long long MaxcostMat[sizen][sizen];

int step_i = 0;
  
void* multi(void* arg)
{
    int core = step_i++;
  
    // Each thread computes 1/4th of matrix multiplication
    for (int i = core * sizen / 4; i < (core + 1) * sizen/ 4; i++) 
        for (int j = 0; j < sizen; j++) 
            for (int k = 0; k < sizen; k++) 
                productMat[i][j] += MincostMat[i][k] * MaxcostMat[k][j];
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



// structure for information of each cell
struct cell
{
	int x, y;
	long long distance;
	cell(int x, int y, long long distance) :
		x(x), y(y), distance(distance) {}
};

// Utility method for comparing two cells
bool operator<(const cell& a, const cell& b)
{
	if (a.distance == b.distance)
	{
		if (a.x != b.x)
			return (a.x < b.x);
		else
			return (a.y < b.y);
	}
	return (a.distance < b.distance);
}

// Utility method to check whether a point is
// inside the grid or not
bool isInsideGrid(int i, int j)
{
	return (i >= 0 && i < sizen && j >= 0 && j < sizen);
}

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

// Method returns minimum cost to reach bottom
// right from top left
void FindMinCostA(long long grid[sizen][sizen], int row, int col)
{
	

	// initializing distance array by INT_MAX
	for (int i = 0; i < row; i++)
		for (int j = 0; j < col; j++)
			MincostMat[i][j] = INT_MAX;

	// direction arrays for simplification of getting
	// neighbour
	int dx[] = { 0, -1};
	int dy[] = { -1, 0};

	set<cell> st;

	// insert (0, 0) cell with 0 distance
	st.insert(cell(sizen-1, sizen-1, 0));

	// initialize distance of (0, 0) with its grid value
	MincostMat[sizen-1][sizen-1] = grid[sizen-1][sizen-1];

	// loop for standard dijkstra's algorithm
	while (!st.empty())
	{
		// get the cell with minimum distance and delete
		// it from the set
		cell k = *st.begin();
		st.erase(st.begin());

		// looping through all neighbours
		for (int i = 0; i < 2; i++)
		{
			int x = k.x + dx[i];
			int y = k.y + dy[i];

			// if not inside boundary, ignore them
			if (!isInsideGrid(x, y))
				continue;
            //print()
			// If distance from current cell is smaller, then
			// update distance of neighbour cell
			if (MincostMat[x][y] > MincostMat[k.x][k.y] + grid[x][y])
			{
			
				if (MincostMat[x][y] != INT_MAX)
					st.erase(st.find(cell(x, y, MincostMat[x][y])));

				MincostMat[x][y] = MincostMat[k.x][k.y] + grid[x][y];
               // cout<<(dis[x][y])<<endl;
				st.insert(cell(x, y, MincostMat[x][y]));
			}
		}
	}

}

// Driver code to test above methods
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
    FindMinCostA(costMatrixA,sizen,sizen);
 
    for (i=0;i<sizen;i++)
    {
        for(j=0;j<sizen;j++)
        {
           
          //  matA[i][j]=MincostMat[i][j];
            MaxcostMat[i][j]= FindMaxCostB(i,j,sizen);
           // matB[i][j]=MaxcostMat[i][j];

            
        }
    }
     pthread_t threads[MAX_THREAD];
  
    // Creating four threads, each evaluating its own part
    for (int i = 0; i < MAX_THREAD; i++) {
        int* p;
        pthread_create(&threads[i], NULL, multi, (void*)(p));
    }
  
    // joining and waiting for all threads to complete
    for (int i = 0; i < MAX_THREAD; i++) 
        pthread_join(threads[i], NULL);    

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
