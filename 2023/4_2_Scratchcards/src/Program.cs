using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
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

            List<string> input = File.ReadAllLines(path).ToList();
            input.RemoveAll(s => string.IsNullOrEmpty(s));

            List<Card> deck = new List<Card>(input.Count+1);
            deck.Add(new Card(0)); // card 0
            List<Card> cards_1_to_N = input.ConvertAll(s => Card.Parse(s));
            deck.AddRange(cards_1_to_N);

            int[] copy_count = Enumerable.Repeat(1, deck.Count).ToArray();
            copy_count[0] = 0;

            for( int id = 1, maxid = cards_1_to_N.Last().CardID; id <= maxid ; ++id)
            {
                Card c = deck[id];
                int count = copy_count[id];

                Console.WriteLine($"Card {c.CardID} has {c.MatchedWinners.Length} winners  ");

                for ( int i=1, len = c.MatchedWinners.Length; i <= len && c.CardID+i < deck.Count ; i++ ) 
                {
                    copy_count[i + c.CardID] += count;
                }
            }


            int sum = copy_count.Sum();
            Console.WriteLine($"{sum}"); // 519444

        }
    }
}
