#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <QRandomGenerator>
#include <QPropertyAnimation>
#include <QSequentialAnimationGroup>
#include <QTimer>
#include "magicball.h"
#include "oracle.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

void MainWindow::on_ballButton_clicked()
{
    ballPredict();
}

void MainWindow::ballPredict()
{
    ui->ballText->setText("");
    QPoint pos = ui->ballImage->pos();

    MagicBall magicBall;

    QSequentialAnimationGroup *group = new QSequentialAnimationGroup(this);

    for (int i = 0; i < 20; i++) {
        QPropertyAnimation *anim = new QPropertyAnimation(ui->ballImage, "pos");
        anim->setDuration(50);
        anim->setStartValue(ui->ballImage->pos());
        anim->setEndValue(pos + QPoint(QRandomGenerator::global()->bounded(-10, 11),
                                       QRandomGenerator::global()->bounded(-10, 11)));
        group->addAnimation(anim);
    }

    QPropertyAnimation *returnAnim = new QPropertyAnimation(ui->ballImage, "pos");
    returnAnim->setDuration(50);
    returnAnim->setEndValue(pos);
    group->addAnimation(returnAnim);

    connect(group, &QSequentialAnimationGroup::finished, [=]() {
        ui->ballText->setText(magicBall.getPrediction());
    });

    group->start(QAbstractAnimation::DeleteWhenStopped);
}

void MainWindow::on_oracleButton_clicked()
{
    oraclePredict();
}

void MainWindow::oraclePredict()
{
    Oracle oracle;

    QStringList phrases = {"Настраиваюсь с космосом", "Настраиваюсь с космосом .", "Настраиваюсь с космосом . .", "Настраиваюсь с космосом . . .",
                           "Смотрю в будущее", "Смотрю в будущее .", "Смотрю в будущее . .", "Смотрю в будущее . . .",
                           "Общаюсь с духами", "Общаюсь с духами .", "Общаюсь с духами . .", "Общаюсь с духами . . ."};

    for (const QString &text : phrases)
    {
        ui->oracleText->setText(text);

        QEventLoop loop;
        QTimer::singleShot(500, &loop, &QEventLoop::quit);
        loop.exec();
    }

    ui->oracleText->setText(oracle.getPrediction());
}

MainWindow::~MainWindow()
{
    delete ui;
}






