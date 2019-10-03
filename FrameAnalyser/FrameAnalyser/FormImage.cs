using AForge.Imaging;
using AForge.Imaging.Filters;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace FrameAnalyser
{
    public partial class FormImage : Form
    {


        private System.Windows.Forms.Timer timer1 = new System.Windows.Forms.Timer() { 
            Enabled = true, 
            Interval = 200 //0.5 sec
        };

        string ip;
        SerializiationData data;

        public FormImage()
        {
            InitializeComponent();

            timer1.Tick += new System.EventHandler(Ticks);

            BinarySerialization.Deserialize<SerializiationData>(out data);

            ip = data.url.Substring(data.url.IndexOf("http://"), data.url.IndexOf("/tmp"));
            ip = ip.Remove(0, 7);
        }

        Bitmap bmp;
        //do every Timer.Tick
        private void Ticks(object sender, EventArgs e)
        {
            //update picture
            Task.Run(() => { 
                bmp = LoadPicture(data.url);
                pictureBox1.Image = bmp;

            });

            try
            {
                
                //выделение желтого цвета
                EuclideanColorFiltering filter = new EuclideanColorFiltering();
                filter.CenterColor = new RGB(224, 209, 3); //желтый цвет
                filter.Radius = 100;
                filter.ApplyInPlace(bmp);

                ////Класс считает и извлекает отдельные объекты на изображениях
                BlobCounter blobCounter = new BlobCounter();
                blobCounter.ProcessImage(bmp);

                Rectangle[] rects = blobCounter.GetObjectsRectangles(); //центр обьекта

                int x = rects[0].X;
                int y = rects[0].Y;
                /*
                CameraRotation("right");
                if (x < 400)
                {
                    CameraRotation("right");
                    return;
                }
                if (x > 900)
                {
                    CameraRotation("left");
                    return;
                }
                if (y < 300)
                {
                    CameraRotation("up");
                    return;
                }
                if (y > 500)
                {
                    CameraRotation("down");
                    return;
                }
                CameraRotation("stop");
                */
            }
            catch (Exception ex){
                label1.Text = ex.ToString();
            }

        }

        private void CameraRotation(string side)
        {
            Task.Run(()=>{ 
                string query = "http://" + ip + "/web/cgi-bin/hi3510/ptzctrl.cgi?-step=0&-act=" + side;
                HttpWebRequest httpWebRequest = (HttpWebRequest)WebRequest.Create(query);

                String username = "admin";
                String password = "admin";
                String encoded = System.Convert.ToBase64String(System.Text.Encoding.GetEncoding("ISO-8859-1").GetBytes(username + ":" + password));

                httpWebRequest.Headers.Add("Authorization", "Basic " + encoded);

                httpWebRequest.GetResponse();
            }); 
        }

        private Bitmap LoadPicture(string url)
        {
            HttpWebRequest wreq;
            HttpWebResponse wresp;
            Stream mystream;
            Bitmap bmp;

            bmp = null;
            mystream = null;
            wresp = null;
            try
            {
                wreq = (HttpWebRequest)WebRequest.Create(url);
                wreq.AllowWriteStreamBuffering = true;

                String username = "admin";
                String password = "admin";
                String encoded = System.Convert.ToBase64String(System.Text.Encoding.GetEncoding("ISO-8859-1").GetBytes(username + ":" + password));

                wreq.Headers.Add("Authorization", "Basic " + encoded);

                wresp = (HttpWebResponse)wreq.GetResponse();

                if ((mystream = wresp.GetResponseStream()) != null)
                    bmp = new Bitmap(mystream);
            }
            finally
            {
                if (mystream != null)
                    mystream.Close();

                if (wresp != null)
                    wresp.Close();
            }
            return (bmp);
        }


        //exit
        private void FormImage_FormClosed(object sender, FormClosedEventArgs e) => Application.Exit();
    }
}
