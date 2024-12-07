using advent_of_code;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tests
{
    [TestFixture]
    public class TestParts
    {

        public class Case
        {
            public string Input;
            public int[] ExpectedPartNumbers;

            public (int l, int c)[] ExpectedGears { get; }

            public Case(string input, int[] ExpectedPartNumbers, (int l, int c)[] ExpectedGears)
            {
                if (input is null)
                {
                    throw new ArgumentNullException(nameof(input));
                }

                Input = input;
                this.ExpectedPartNumbers = ExpectedPartNumbers;
                this.ExpectedGears = ExpectedGears;
            }

            public override string ToString()
            {
                return string.Join(", ", ExpectedPartNumbers) + "\r\n" +  Input;
            }
        }

        public static string simple =
@"
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
".Trim();



        public readonly static Case[] cases = new Case[] {
            new Case(simple, 
                new int[]{ 467, 35, 633, 617, 592, 755, 664, 598 },
                new (int l, int c)[]{ (1,3), (4, 3), (8,5)}
                ),
        };

        [Test, TestCaseSource(nameof(cases))]
        public void TestParseGame(Case c)
        {
            Parts actual = Parts.Parse(c.Input);

            CollectionAssert.AreEquivalent(c.ExpectedPartNumbers, actual.PartNumbers);
        }

     [Test, TestCaseSource(nameof(cases))]
        public void TestFindGearAdjacant(Case c)
        {
            Parts actual = Parts.Parse(c.Input);

            CollectionAssert.AreEquivalent(c.ExpectedPartNumbers, actual.PartNumbers);
            CollectionAssert.AreEquivalent(c.ExpectedGears, actual.Gears);

        }

    }
}
