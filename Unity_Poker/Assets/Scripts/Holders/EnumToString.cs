using System;
using System.ComponentModel;
using System.Reflection;

public static class EnumToString
{
    /// <summary> Turns a enum into a string. </summary>
    /// <param name="value"> This enum to get the string of. </param>
    /// <returns> The enum as a string. </returns>
    public static string GetDescription(this Enum value)
    {
        Type type = value.GetType();
        string name = Enum.GetName(type, value);
        
        if (name != null)
        {
            FieldInfo field = type.GetField(name);
            if (field != null)
            {
                if (Attribute.GetCustomAttribute(field, typeof(DescriptionAttribute)) is DescriptionAttribute attr)
                {
                    return attr.Description;
                }
            }
        }

        return null;
    }
}