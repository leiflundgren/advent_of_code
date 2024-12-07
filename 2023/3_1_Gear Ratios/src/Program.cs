using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace advent_of_code
{
    public class Program
    {

        public static void Main(string[] args)
        {
            string path = Environment.CurrentDirectory;
            Console.WriteLine("Path: " + path);

            path = Path.GetFullPath(Path.Combine(path, "..\\..\\..\\..\\input.txt"));
            Console.WriteLine("Path: " + path);

            string input = File.ReadAllText(path);


            Parts parts = Parts.Parse(input);

            int sum = parts.PartNumbers.Sum();

            //foreach ( string line in lines)
            //{
            //    if  (string.IsNullOrEmpty(line)) continue;

            //    Game g = Game.Parse(line);

            //    if ( !g.IsPossible(MasterSet))
            //    {
            //        Console.WriteLine(g + " impossible!");
            //    }
            //    else
            //    {
            //        Console.WriteLine(g + " possible");
            //        sum += g.N;
            //    }
            //}

            Console.WriteLine($"{sum}"); // 519444

        }
    }
}
