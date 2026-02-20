using System;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        private Series currentSeries;
        double v, vx, vy, k, m, S, x, y, y0, alpha, dt, t, ymax, xmax;
        const double g = 9.81, C = 0.15, rho = 1.29;

        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            dt = double.Parse(step.Text);
            v = double.Parse(speed.Text);
            y0 = double.Parse(height.Text);
            alpha = double.Parse(angle.Text);
            m = double.Parse(weight.Text);
            S = double.Parse(size.Text);

            k = 0.5 * C * rho * S / m;
            alpha = alpha * Math.PI / 180.0;

            vx = v * Math.Cos(alpha);
            vy = v * Math.Sin(alpha);

            y = y0;
            x = 0;
            ymax = 0;
            xmax = 0;

            currentSeries = new Series
            {
                ChartType = SeriesChartType.Line,
                Name = $"dt={dt:F5}"
            };

            chart1.Series.Add(currentSeries);

            currentSeries.Points.AddXY(x, y);

            timer1.Start();
        }

        private void timer1_Tick(object sender, EventArgs e)
        {

            v = Math.Sqrt(vx * vx + vy * vy);

            x = x + vx * dt;
            y = y + vy * dt;

            vx = vx - k * vx * v * dt;
            vy = vy - (g + k * vy * v) * dt;

            if (y > ymax) ymax = y;
            if (x > xmax) xmax = x;

            currentSeries.Points.AddXY(x, y);

            if (y <= 0)
            {
                timer1.Stop();
                maxHeight.Text = ymax.ToString("F2");
                maxLength.Text = xmax.ToString("F2");
                lastSpeed.Text = v.ToString("F2");
            }
        }
    }
}
