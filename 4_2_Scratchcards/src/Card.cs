using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace advent_of_code
{
    public class Card
    {
        public int CardID;
        public int[] Numbers;
        public int[] Winners;

        public int[] MatchedWinners => Numbers.Intersect(Winners).ToArray();

        public int Points => ((int)Math.Round(Math.Pow(2, MatchedWinners.Length)))/2;

        public Card(int id)
        {
            this.CardID = id;
            this.Numbers = new int[0];
            this.Winners = new int[0];
        }

        public static Card Parse(string input)
        {
            var regex = new System.Text.RegularExpressions.Regex(@"^Card +(\d+)\: (.*)\|(.*)$");
            var match = regex.Match(input); 
            if (match == null) throw new ArgumentException($"invalid input line\n{input}");

            string[] numbers = match.Groups[2].Value.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);
            string[] winners = match.Groups[3].Value.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);

            Card c = new Card(int.Parse(match.Groups[1].Value));
            c.Numbers = Array.ConvertAll(numbers, int.Parse);
            c.Winners = Array.ConvertAll(winners, int.Parse);

            return c;
        }

        public override string ToString()
        {
            return $"Card {CardID}: " + string.Join(" ", Numbers) + " | " + string.Join(" ", Winners);
        }

    }
}
