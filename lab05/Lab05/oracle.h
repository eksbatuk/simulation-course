#ifndef ORACLE_H
#define ORACLE_H
#include "prediction.h"

class Oracle
{
private:
    QString prediction;

public:
    Oracle();
    const QString getPrediction() const;
};

#endif // ORACLE_H
