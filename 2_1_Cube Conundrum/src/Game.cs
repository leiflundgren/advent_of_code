using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace advent_of_code
{
    public class Game
    {
        public readonly List<Set> Sets;
        public readonly int N;
        
        public Game(int n, params Set[] sets)
            : this(n, (ICollection<Set>)sets)
        {}
        public Game(int n, ICollection<Set> sets)
        {
            this.N = n;
            this.Sets = new List<Set>(sets);
        }

        public static Game Parse(string input)
        {
            // Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

            int n;
            List<Set> sets = new List<Set>();


            int colon = input.IndexOf(':');
            string strN = input.Substring(5, colon-5);
            n = int.Parse(strN);
            string[] parts = input.Substring(colon + 1).Split(';', StringSplitOptions.TrimEntries);
            foreach ( string set_str in parts)
            {
                sets.Add(Set.Parse(set_str));
            }

            return new Game(n, sets);
        }

        public override bool Equals(object? obj) {  return Equals(this, obj as Game); }
        public static bool Equals(Game x, Game y)
        {
            if (object.ReferenceEquals(x, y)) return true;
            if (object.ReferenceEquals(x, null) || object.ReferenceEquals(null, y )) return false;

            if ( x.N != y.N) return false;  
            if ( x.Sets.Count != y.Sets.Count) return false;

            var ex = x.Sets.GetEnumerator();
            var ey = y.Sets.GetEnumerator();

            for (; ; )
            {
                bool mx = ex.MoveNext();
                bool my = ey.MoveNext();
                if (mx != my) return false;

                if (!mx) break;
                if (!ex.Current.Equals(ey.Current)) return false;
            }

            return true;
        }

        public override int GetHashCode()
        {
            return N;
        }

        public override string ToString()
        {
            return $"Game {N}: " + String.Join("; ", Sets.ConvertAll(s => s.ToString()));
        }
    }
}
