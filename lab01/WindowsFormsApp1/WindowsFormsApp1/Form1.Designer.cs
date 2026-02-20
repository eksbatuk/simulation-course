using System.Drawing;

namespace WindowsFormsApp1
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.Windows.Forms.DataVisualization.Charting.ChartArea chartArea1 = new System.Windows.Forms.DataVisualization.Charting.ChartArea();
            System.Windows.Forms.DataVisualization.Charting.Legend legend1 = new System.Windows.Forms.DataVisualization.Charting.Legend();
            this.button1 = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.height = new System.Windows.Forms.TextBox();
            this.speed = new System.Windows.Forms.TextBox();
            this.angle = new System.Windows.Forms.TextBox();
            this.size = new System.Windows.Forms.TextBox();
            this.weight = new System.Windows.Forms.TextBox();
            this.step = new System.Windows.Forms.TextBox();
            this.chart1 = new System.Windows.Forms.DataVisualization.Charting.Chart();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.lable7 = new System.Windows.Forms.Label();
            this.maxHeight = new System.Windows.Forms.Label();
            this.lastSpeed = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.maxLength = new System.Windows.Forms.Label();
            this.label9 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.chart1)).BeginInit();
            this.SuspendLayout();
            // 
            // button1
            // 
            this.button1.Font = new System.Drawing.Font("Microsoft Sans Serif", 25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.button1.Location = new System.Drawing.Point(78, 615);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(376, 265);
            this.button1.TabIndex = 0;
            this.button1.Text = "Launch";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(102, 45);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(74, 25);
            this.label1.TabIndex = 1;
            this.label1.Text = "Height";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(102, 134);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(74, 25);
            this.label2.TabIndex = 2;
            this.label2.Text = "Speed";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(102, 230);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(67, 25);
            this.label3.TabIndex = 3;
            this.label3.Text = "Angle";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(102, 323);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(54, 25);
            this.label4.TabIndex = 4;
            this.label4.Text = "Size";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(102, 403);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(79, 25);
            this.label5.TabIndex = 5;
            this.label5.Text = "Weight";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(102, 488);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(56, 25);
            this.label6.TabIndex = 6;
            this.label6.Text = "Step";
            // 
            // height
            // 
            this.height.Location = new System.Drawing.Point(274, 39);
            this.height.Name = "height";
            this.height.Size = new System.Drawing.Size(100, 31);
            this.height.TabIndex = 7;
            this.height.Text = "0";
            // 
            // speed
            // 
            this.speed.Location = new System.Drawing.Point(274, 128);
            this.speed.Name = "speed";
            this.speed.Size = new System.Drawing.Size(100, 31);
            this.speed.TabIndex = 8;
            this.speed.Text = "10";
            // 
            // angle
            // 
            this.angle.Location = new System.Drawing.Point(274, 224);
            this.angle.Name = "angle";
            this.angle.Size = new System.Drawing.Size(100, 31);
            this.angle.TabIndex = 9;
            this.angle.Text = "45";
            // 
            // size
            // 
            this.size.Location = new System.Drawing.Point(274, 317);
            this.size.Name = "size";
            this.size.Size = new System.Drawing.Size(100, 31);
            this.size.TabIndex = 10;
            this.size.Text = "1";
            // 
            // weight
            // 
            this.weight.Location = new System.Drawing.Point(274, 397);
            this.weight.Name = "weight";
            this.weight.Size = new System.Drawing.Size(100, 31);
            this.weight.TabIndex = 11;
            this.weight.Text = "1";
            // 
            // step
            // 
            this.step.Location = new System.Drawing.Point(274, 488);
            this.step.Name = "step";
            this.step.Size = new System.Drawing.Size(100, 31);
            this.step.TabIndex = 12;
            this.step.Text = "0,01";
            // 
            // chart1
            // 
            this.chart1.BorderlineWidth = 7;
            chartArea1.AxisX.Maximum = 15D;
            chartArea1.AxisX.Minimum = 0D;
            chartArea1.AxisY.Maximum = 10D;
            chartArea1.AxisY.Minimum = 0D;
            chartArea1.Name = "ChartArea1";
            this.chart1.ChartAreas.Add(chartArea1);
            legend1.Name = "Legend1";
            this.chart1.Legends.Add(legend1);
            this.chart1.Location = new System.Drawing.Point(531, 39);
            this.chart1.Name = "chart1";
            this.chart1.Size = new System.Drawing.Size(1355, 841);
            this.chart1.TabIndex = 13;
            this.chart1.Text = "chart1";
            // 
            // lable7
            // 
            this.lable7.AutoSize = true;
            this.lable7.Location = new System.Drawing.Point(1906, 70);
            this.lable7.Name = "lable7";
            this.lable7.Size = new System.Drawing.Size(121, 25);
            this.lable7.TabIndex = 14;
            this.lable7.Text = "Max Height";
            // 
            // maxHeight
            // 
            this.maxHeight.AutoSize = true;
            this.maxHeight.Location = new System.Drawing.Point(2148, 70);
            this.maxHeight.Name = "maxHeight";
            this.maxHeight.Size = new System.Drawing.Size(0, 25);
            this.maxHeight.TabIndex = 15;
            // 
            // lastSpeed
            // 
            this.lastSpeed.AutoSize = true;
            this.lastSpeed.Location = new System.Drawing.Point(2148, 134);
            this.lastSpeed.Name = "lastSpeed";
            this.lastSpeed.Size = new System.Drawing.Size(0, 25);
            this.lastSpeed.TabIndex = 17;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(1906, 134);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(121, 25);
            this.label8.TabIndex = 16;
            this.label8.Text = "Last Speed";
            // 
            // maxLength
            // 
            this.maxLength.AutoSize = true;
            this.maxLength.Location = new System.Drawing.Point(2148, 204);
            this.maxLength.Name = "maxLength";
            this.maxLength.Size = new System.Drawing.Size(0, 25);
            this.maxLength.TabIndex = 19;
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(1906, 204);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(125, 25);
            this.label9.TabIndex = 18;
            this.label9.Text = "Max Lenght";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(12F, 25F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(2303, 949);
            this.Controls.Add(this.maxLength);
            this.Controls.Add(this.label9);
            this.Controls.Add(this.lastSpeed);
            this.Controls.Add(this.label8);
            this.Controls.Add(this.maxHeight);
            this.Controls.Add(this.lable7);
            this.Controls.Add(this.chart1);
            this.Controls.Add(this.step);
            this.Controls.Add(this.weight);
            this.Controls.Add(this.size);
            this.Controls.Add(this.angle);
            this.Controls.Add(this.speed);
            this.Controls.Add(this.height);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.button1);
            this.Name = "Form1";
            this.Text = "Form1";
            ((System.ComponentModel.ISupportInitialize)(this.chart1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();
            // 
            // timer1
            // 
            timer1.Interval = 10;
            timer1.Tick += timer1_Tick;

        }

        #endregion

        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox height;
        private System.Windows.Forms.TextBox speed;
        private System.Windows.Forms.TextBox angle;
        private System.Windows.Forms.TextBox size;
        private System.Windows.Forms.TextBox weight;
        private System.Windows.Forms.TextBox step;
        private System.Windows.Forms.DataVisualization.Charting.Chart chart1;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.Label lable7;
        private System.Windows.Forms.Label maxHeight;
        private System.Windows.Forms.Label lastSpeed;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.Label maxLength;
        private System.Windows.Forms.Label label9;
    }
}

