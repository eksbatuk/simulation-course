#ifndef MAGICBALL_H
#define MAGICBALL_H
#include "prediction.h"

class MagicBall
{
private:
    std::vector<Prediction> predictionList;
    QString prediction;

public:
    MagicBall();
    const QString getPrediction() const;
};

#endif // MAGICBALL_H
