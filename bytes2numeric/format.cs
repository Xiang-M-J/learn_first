
private object getValue(char type, byte[] data)
{
    int width = data.Length;
    if (type == 'f')
    {
        if (width == 2)
        {
            Half value = BitConverter.ToHalf(data, 0);
            return value;
        }
        else if (width == 4)
        {
            float value;
            value = BitConverter.ToSingle(data);
            return value;
        }
        else if (width == 8)
        {
            double value;
            value = BitConverter.ToDouble(data, 0);
            //}
            return value;
        }
        else
        {
            MessageBox.Show("type: " + type + "\twidth:" + width.ToString() + " is not compatible");
            return 0;
        }

    }
    else if (type == 'i')
    {
        if (width == 2)
        {
            return BitConverter.ToInt16((byte[])data, 0);
        }
        else if (width == 4)
        {
            return BitConverter.ToInt32((byte[])data, 0);
        }
        else if (width == 8)
        {
            return BitConverter.ToInt64((byte[])data, 0);
        }
        else
        {
            MessageBox.Show("type: " + type + "\twidth:" + width.ToString() + " is not compatible");
            return 0;
        }
    }
    else if(type == 'u')
    {
        if(width == 2)
        {
            return BitConverter.ToUInt16((byte[])data, 0);
        }
        else if(width == 4)
        {
            return BitConverter.ToUInt32((byte[])data, 0);
        }
        else if(width == 8)
        {
            return BitConverter.ToUInt64((byte[])data, 0);
        }
        else
        {
            MessageBox.Show("type: " + type + "\twidth:" + width.ToString() + " is not compatible");
            return 0;
        }
    }
    else if (type == 'b')
    {
        if (width == 4)
        {
            return BitConverter.ToBoolean((byte[])data, 0);
        }
        else
        {
            MessageBox.Show("type: " + type + "\twidth:" + width.ToString() + " is not compatible");
            return 0;
        }
    }
    else if (type == 'c')
    {
        if (width == 8)
        {
            float real = BitConverter.ToSingle((byte[])data.Take(4), 0);
            float imag = BitConverter.ToSingle(data, 4);
            Complex x = new Complex(real, imag);
            return x;
        }
        else if (width == 16)
        {
            double real = BitConverter.ToSingle((byte[])data.Take(8), 0);
            double imag = BitConverter.ToSingle(data, 8);
            Complex x = new Complex(real, imag);
            return x;
        }
        else
        {
            MessageBox.Show("type: " + type + "\twidth:" + width.ToString() + " is not compatible");
            return 0;
        }
    }
    //BitConverter.
    else if(type =='U') {
        try
        {
            return BitConverter.ToString(data, 0);
        }
        catch
        {
            MessageBox.Show("type: " + type + "\twidth:" + width.ToString() + " is not compatible");
            return "";
        }
    }

    return 0;
}
