using advent_of_code;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NUnit.Framework;

namespace Tests
{
    [TestFixture]
    public class TheTests
    {

        public class Case
        {
            public string Input;
            public Card Card;
            public int ExpectedPoints;

            public override string ToString()
            {
                return $"{Card} Points:{ExpectedPoints}\r\n{Input}";
            }
        }

        public static string[] simple =
@"
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
".Trim().Split('\r', '\n', StringSplitOptions.RemoveEmptyEntries);



        public readonly static Case[] cases = new Case[] {
            new Case 
            {
                Input = simple[0],
                Card = new Card (1),
                ExpectedPoints=8,
            },
            new Case
            {
                Input = simple[1],
                Card = new Card (2),
                ExpectedPoints=2,
            },
            new Case
            {
                Input = simple[2],
                Card = new Card (3),
                ExpectedPoints=2,
            },
            new Case
            {
                Input = simple[3],
                Card = new Card (4),
                ExpectedPoints=1,
            },
            new Case
            {
                Input = simple[4],
                Card = new Card (5),
                ExpectedPoints=0,
            },
            new Case
            {
                Input = simple[5],
                Card = new Card (6),
                ExpectedPoints=0,
            },
        };

        [Test, TestCaseSource(nameof(cases))]
        public void TestIt(Case c)
        {
            Card actual = Card.Parse(c.Input);
            Assert.That(c.ExpectedPoints != actual.Points, $"Expected points: {c.ExpectedPoints} actual:{actual.Points}");
        }


    }
}
