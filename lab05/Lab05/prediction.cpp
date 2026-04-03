#include "prediction.h"

Prediction::Prediction(QString _prediction, double _probability)
{
    prediction = _prediction;
    probability = _probability;
};

QString Prediction::getPrediction()
{
    return prediction;
}

double Prediction::getProbability()
{
    return probability;
}
