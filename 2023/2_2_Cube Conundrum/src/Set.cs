using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace advent_of_code
{
    public class Set : IEquatable<Set?>
    {
        public readonly int blue, red, green;

        public Set(int red, int green, int blue)
        {
            this.blue = blue;
            this.red = red;
            this.green = green;
        }

        public int PowerOf => red*green*blue;

        public static Set Parse(string s)
        {
            string[] parts = s.Split(',', StringSplitOptions.TrimEntries);

            int r=0, g=0, b=0;
            foreach (string part in parts)
            {
                int space = part.IndexOf(' ');
                if (space == -1) throw new ArgumentException("No space in part");
                int n = int.Parse(part.Substring(0, space));

                if (part.EndsWith("blue"))
                    b = n;
                else if (part.EndsWith("red"))
                    r = n;
                else if (part.EndsWith("green"))
                    g = n;
            }

            return new Set(r, g, b);
        }

        public override bool Equals(object? obj)
        {
            return Equals(obj as Set);
        }

        public bool Equals(Set? other)
        {
            return other is not null &&
                   blue == other.blue &&
                   red == other.red &&
                   green == other.green;
        }


        public override int GetHashCode()
        {
            return HashCode.Combine(blue, red, green);
        }

        public override string ToString()
        {
            return $"{red} Red, {green} Green, {blue} Blue";
        }
    }
}
