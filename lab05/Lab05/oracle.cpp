#include <random>
#include "oracle.h"

Oracle::Oracle()
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> distrib(0, 1);
    double probability = distrib(gen);

    if (probability >= 0.5) prediction = "Да!";
    else prediction = "Нет.";
};

const QString Oracle::getPrediction() const
{
    const QString _prediction = prediction;
    return _prediction;
}