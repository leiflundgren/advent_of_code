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

            path = Path.GetFullPath(Path.Combine(path, "..\\..\\..\\input.txt"));
            Console.WriteLine("Path: " + path);

            string[] lines = File.ReadAllLines(path);
            


        }
    }
}
