#include <iostream>
#include <chrono>
#include <iomanip> 

using namespace std;

void Solve(double timeStep, double sizeStep, double density, double heatCapacity, double thermalConductivity, double size, double tempRight, double tempLeft, double targetTime, double *result)
    {
        int gridSize = size / sizeStep + 1;
        double grid[gridSize];
        double gridNew[gridSize];
        double F[gridSize];
        double alpha[gridSize];
        double beta[gridSize];
        double A, B, C;

        A = thermalConductivity / (sizeStep * sizeStep);
        C = thermalConductivity / (sizeStep * sizeStep);
        B = 2 * thermalConductivity / (sizeStep * sizeStep) + density * heatCapacity / timeStep;

        for (int i = 0; i < gridSize; i++)
            grid[i] = tempRight;

        auto start = chrono::high_resolution_clock::now();
        int timeGridSize = targetTime / timeStep;

        for (int i = 0; i < timeGridSize; i++)
        {
            alpha[0] = 0;
            beta[0] = tempLeft;

            for (int j = 0; j < gridSize; j++)
                F[j] = -density * heatCapacity / timeStep * grid[j];
            
            for (int j = 1; j < gridSize; j++)
            {
                alpha[j] = A / (B - C * alpha[j - 1]);
                beta[j] = (C * beta[j - 1] - F[j]) / (B - C * alpha[j - 1]);
            }
            
            gridNew[gridSize-1] = tempRight;
            gridNew[0] = tempLeft;
            for (int j = gridSize-2; j >= 0; j --)
                gridNew[j] = alpha[j] * gridNew[j+1] + beta[j];

            for (int i = 0; i < gridSize; i++)    
                swap(grid[i], gridNew[i]);
        }

        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> ellapsedTime = end - start;

        result[0] = grid[gridSize/2]; result[1] = ellapsedTime.count();
    }

int main()
{
    double density = 1000;
    double heatCapacity = 4200;
    double thermalConductivity = 0.6;

    double size = 0.02;
    double tempRight = 0;
    double tempLeft = 1000;  
    double targetTime = 200.0;
    
    double *result = new double[2];
    double timeSteps[4] = {0.1, 0.01, 0.001, 0.0001};
    double sizeSteps[4] = {0.01, 0.001, 0.0001, 0.00001};

    cout << "h//t  |     0.1000   |      0.0100     |     0.0010    |     0.0001    |" << endl 
         << "------------------------------------------------------------------------" << endl;

    for (double sizeStep : sizeSteps)
    {
        cout << fixed << setprecision(4) << sizeStep << "|";
        for (double timeStep : timeSteps)
        {
            Solve(timeStep, sizeStep, density, heatCapacity, thermalConductivity, size, tempRight, tempLeft, targetTime, result);

            cout  << result[0] << "*C (" << result[1] << "ms) | ";
        }

        cout << endl;
    }

    return 0;
}