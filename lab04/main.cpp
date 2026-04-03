#include <iostream>
#include <cmath>
#include <iomanip>
#include <chrono>
#include <random>

int generateSeed()
{
    return (std::chrono::duration_cast<std::chrono::seconds>(std::chrono::system_clock::now().time_since_epoch()).count());
}

class RandomGenerator
{
private: 
    long long seed;
    long long M;
    long long b;
    int size = 100000;
    double mean;
    double dispersion;
    double *x;


public:
    RandomGenerator()
    {
        seed = generateSeed();
        M = std::pow(2, 31) - 1;
        b = 16807;
        x = new double[size];
    }

    void generateMCG()
    {
        long long xi = seed;

        for (int i = 0; i < size; i++)
        {
            xi = (xi * b) % M;
            x[i] = static_cast<double>(xi) / M;
        };
    }

    void generateMT()
    {
        std::mt19937_64 gen(seed);
        std::uniform_real_distribution<>xi(0, 1);

        for (int i = 0; i < size; i++)
        {
            x[i] = xi(gen);
        };
    }

    void getStatistics()
    {
        double sum = 0;
        for (int i = 0; i < size; i++) sum += x[i];
        mean = sum / size;

        dispersion = 0;
        for (int i = 0; i < size; i++) dispersion += (x[i] - mean) * (x[i] - mean);
        dispersion /= size;
    }

    void showStatisticsForMCG()
    {
        std::cout << std::fixed << std::setprecision(10) << "Для LCG: Среднее: " << mean << ", " << "Дисперсия: " << dispersion << std::endl;  
    }

    void showStatisticsForMT()
    {
        std::cout << std::fixed << std::setprecision(10) << "Для MT: Среднее: " << mean << ", " << "Дисперсия: " << dispersion << std::endl;  
    }

    void generateBoth()
    {
        generateMCG();
        getStatistics();
        showStatisticsForMCG();

        generateMT();
        getStatistics();
        showStatisticsForMT();
    }

    void print()
    {
        std::cout << x[size/2];
    }
};

int main()
{
    RandomGenerator testGenerator;
    testGenerator.generateMCG();
    testGenerator.print();

    return 0;
}