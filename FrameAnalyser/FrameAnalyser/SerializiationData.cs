using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FrameAnalyser
{
    [Serializable]
    public class SerializiationData
    {
        public string url;

        public SerializiationData(string url)
        {
            this.url = url;
        }
    }
}
