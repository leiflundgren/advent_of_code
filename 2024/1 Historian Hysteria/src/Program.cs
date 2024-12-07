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
            new Program().run();
        }
        
        List<int> l1 = new List<int>(), l2 = new List<int>();


        void run()
        {
            Init();
            int sum1 = Part1();
            int sum2 = Part2();
            Console.WriteLine($"sum1 {sum1}"); // 3099
            Console.WriteLine($"sum2 {sum2}"); // 
        }

        void Init()
        {
            (int, int) ParseLine(string s)
            {
                int e1 = s.IndexOf(' ');
                if (e1 == -1) throw new ArgumentException("line missing spaces");

                int b2 = e1;
                while (s[b2] == ' ')
                    b2++;

                return (int.Parse(s.Substring(0, e1)), int.Parse(s.Substring(b2)));
            }

            string path = Environment.CurrentDirectory;
            Console.WriteLine("Path: " + path);

            path = Path.GetFullPath(Path.Combine(path, "..\\..\\..\\..\\input.txt"));
            Console.WriteLine("Path: " + path);

            string[] lines = File.ReadAllLines(path);

            foreach (string line in lines)
            {
                if (string.IsNullOrEmpty(line)) continue;

                (int n1, int n2) = ParseLine(line);
                l1.Add(n1);
                l2.Add(n2);
            }

            l1.Sort();
            l2.Sort();
        }

        int Part1()
        {
            int sum1=0;
            foreach ((int n1, int n2) in l1.Zip(l2))
            {
                int dist = Math.Abs(n1 - n2);
                sum1 += dist;
            }
            return sum1;
        }

        int Part2()
        {
            int n1=-1, n2=-1;
            int sum2 = 0;
            bool EnumEnd = false;
            IEnumerator<int> en1 = l1.GetEnumerator();
            IEnumerator<int> en2 = l2.GetEnumerator();

            int current = -1;
            Next(en1);
            Next(en2);

            bool Next(IEnumerator<int> e)
            {
                bool moved = e.MoveNext();
                EnumEnd = !moved;
                if (moved)
                {
                    n1 = en1.Current;
                    n2 = en2.Current; ;
                }
                return moved;
            }

            while (!EnumEnd)
            {
                if (n1 == current)
                    continue;

                current = n1;
                while (n2 < current)
                {
                    if (!Next(en2))
                        break;
                }
                int cnt1=0;
                while (n1 == current)
                {
                    ++cnt1;
                    if (!Next(en1))
                        break;
                }

                int cnt2=0;
                while (n2 == current)
                {
                    ++cnt2;
                    if (!Next(en2))
                        break;
                }



                int similarity = cnt1 * cnt2 * current;
                sum2 += similarity;
            }

            return sum2;

        

        }
    }
}
