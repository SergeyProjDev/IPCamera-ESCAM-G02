using System;
using System.IO;
using System.Net;
using System.Runtime.Serialization.Formatters.Binary;
using System.Windows.Forms;
using System.Xml.Serialization;

namespace FrameAnalyser
{
    public partial class FormIpGetter : Form
    {
        public FormIpGetter()
        {
            InitializeComponent();
        }

        private void ok_Btn_Click(object sender, EventArgs e)
        {
            string url = "http://"+
                        textBox1.Text + "." +
                        textBox2.Text + "." +
                        textBox3.Text + "." +
                        textBox4.Text +
                        "/tmpfs/auto.jpg";

            try
            {
                Autorize(url);
                Serialize(new SerializiationData(url));
                ShowImageForm();
            }
            catch(Exception ex)
            {
                MessageBox.Show("Error!\n\n"+ex);
            }
        }


        private void Autorize(string url)
        {
            HttpWebRequest httpWebRequest = (HttpWebRequest)WebRequest.Create(url);

            String username = "admin";
            String password = "admin";
            String encoded = System.Convert.ToBase64String(System.Text.Encoding.GetEncoding("ISO-8859-1").GetBytes(username + ":" + password));

            httpWebRequest.Headers.Add("Authorization", "Basic " + encoded);

            httpWebRequest.GetResponse();
        }

        private void Serialize(SerializiationData data)
        {
            BinarySerialization.Serialize(data);
        }
        private SerializiationData Deserialize()
        {
            SerializiationData data;
            BinarySerialization.Deserialize<SerializiationData>(out data);
            return data;
        }

        private void ShowImageForm()
        {
            this.Hide();
            new FormImage().Show();
        }


        private void FormIpGetter_Load(object sender, EventArgs e)
        {
            SerializiationData data = Deserialize();
            if (data == null) 
                return;

            string url = data.url;

            initTextBoxes(url);
        }
        
        void initTextBoxes(string url)
        {
            url = url.Replace("http://", "");
            textBox1.Text = url.Substring(0, url.IndexOf('.'));
            url = url.Remove(0, url.IndexOf('.')+1);
            textBox2.Text = url.Substring(0, url.IndexOf('.'));
            url = url.Remove(0, url.IndexOf('.') + 1);
            textBox3.Text = url.Substring(0, url.IndexOf('.'));
            url = url.Remove(0, url.IndexOf('.') + 1);
            textBox4.Text = url.Substring(0, url.IndexOf('/'));
        }
    }
}
