using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;
using System.Threading.Tasks;

namespace FrameAnalyser
{
    class BinarySerialization 
    {
        public static void Serialize(object obj)
        {
            BinaryFormatter formatter = new BinaryFormatter();
            using (FileStream fs = new FileStream("Data.dat", FileMode.OpenOrCreate))
                formatter.Serialize(fs, obj);
        }

        public static DeserializedType Deserialize<DeserializedType>(out DeserializedType dataSerialized)
        {
            try
            {
                BinaryFormatter formatter = new BinaryFormatter();
                using (FileStream fs = new FileStream("Data.dat", FileMode.OpenOrCreate))
                    dataSerialized = (DeserializedType)formatter.Deserialize(fs);
                return dataSerialized;
            }
            catch (Exception)
            {
                object a = null;
                dataSerialized = (DeserializedType)a;
                return default(DeserializedType);
            }
        }
    }
}
