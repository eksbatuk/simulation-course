#include <random>
#include "magicball.h"

MagicBall::MagicBall()
{
    const int predictionsAmount = 8;
    QString _predictionList[predictionsAmount] = {"Да!", "Абсолютно!", "Вероятнее всего.",
                                                  "Спросите позже:<", "Вселенная молчит.",
                                                  "В следующей жизни.", "Абсолютно нет.", "Нет."};
    double _probabilityList[predictionsAmount] = {0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125};

    for (int i = 0; i < predictionsAmount; i++)
    {
        Prediction _prediction(_predictionList[i], _probabilityList[i]);
        predictionList.push_back(_prediction);
    }

    std::sort(predictionList.begin(), predictionList.end(), [](Prediction &a, Prediction &b) {return a.getProbability() > b.getProbability();});

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> distrib(0, 1);
    double probability = distrib(gen);


    int i = 0;
    while (i < predictionsAmount and probability > 0)
    {
        probability -= predictionList[i].getProbability();
        i++;
    }

    prediction = predictionList[i-1].getPrediction();
}

const QString MagicBall::getPrediction() const
{
    const QString _prediction = prediction;
    return _prediction;
}