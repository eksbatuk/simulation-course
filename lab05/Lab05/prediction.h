#ifndef PREDICTION_H
#define PREDICTION_H
#include <QString>

class Prediction
{
private:
    double probability;
    QString prediction;

public:
    Prediction(QString _prediction, double _probability);
    double getProbability();
    QString getPrediction();
};

#endif // PREDICTION_H
