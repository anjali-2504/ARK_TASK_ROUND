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

void FindMaxCostB(long long grid[][sizen], int row, int col)
{

    for (int i = 0; i < row; i++)
        for (int j = 0; j < col; j++)
            MaxcostMat[i][j] = -10;

    // direction arrays for simplification of getting
    // neighbour
    int dx[] = {-1, 0};
    int dy[] = {0, -1};

    set<cell> st;

    st.insert(cell(3, 3, 0));

    MaxcostMat[3][3] = grid[3][3];
 
    while (!st.empty())
    {

        cell k = *st.begin();
        st.erase(st.begin());

        for (int i = 0; i < 2; i++)
        {
            int x = k.x + dx[i];
            int y = k.y + dy[i];

            if (!isInsideGrid(x, y))
                continue;

          
            if (MaxcostMat[x][y] < (MaxcostMat[k.x][k.y] + grid[x][y]))
                { 
                        MaxcostMat[x][y] =MaxcostMat[k.x][k.y] + grid[x][y];
    
                        st.insert(cell(x, y,MaxcostMat[x][y]));

                    }
               
        }
    }

    return;
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
    FindMaxCostB(costMatrixB, sizen, sizen);
    
  
    int jj, kk, bsize=50;
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
