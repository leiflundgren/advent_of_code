using advent_of_code;
using NUnit.Framework.Internal.Execution;
using NUnit.Framework;
using System;
using System.Collections.Generic;
using System.Diagnostics.Metrics;
using System.Drawing;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;
using static System.Runtime.InteropServices.JavaScript.JSType;

namespace Tests
{
    [TestFixture]
    public class TestGame
    {

        public class Case
        {
            public string Input;
            public Game Expected;

            public Set masterSet;
            public int minCubsMultiplied;
            public bool isPossible;


            public Case(string input, Game expected, Set masterSet, int minCubsMultiplied)
            {
                if (input is null)
                {
                    throw new ArgumentNullException(nameof(input));
                }

                if (expected is null)
                {
                    throw new ArgumentNullException(nameof(expected));
                }

                Input = input;
                Expected = expected;
                this.masterSet = masterSet;
                this.minCubsMultiplied = minCubsMultiplied;
            }


            public override string ToString()
            {
                return Input;
            }
        }
        public static Set MasterSet = new Set(12,13, 14);
        public readonly static Case[] cases = new Case[] {
            // In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
            new Case("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", new Game(1, new Set(4, 0, 3), new Set(1,2,6), new Set(0,2,0)), new Set(4,2,6), 48),
            // Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
            new Case("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", new Game(2, new Set(0,2,1), new Set(1,3,4), new Set(0,1,1)), new Set(1,3,4), 12),
            // Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
            new Case("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", new Game(3, new Set(20,8,6), new Set(4,13,5), new Set(1,5, 0)), new Set(20,13,6), 1560),
            // Game 4 required at least 14 red, 3 green, and 15 blue cubes.
            new Case("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", new Game(4, new Set(3,1,6), new Set(6,3,0), new Set(14,3,15)), new Set(14,3,15), 630),
            // Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
            new Case("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", new Game(5, new Set(6,3,1), new Set(1,2,2)), new Set(6,3,2), 36),
        };

        [Test, TestCaseSource(nameof(cases))]
        public void TestParseGame(Case c)
        {
            Game actual = Game.Parse(c.Input);
            Assert.AreEqual(c.Expected, actual);

            Set min_requiured = actual.MinRequired();
            Assert.AreEqual(c.masterSet, min_requiured);

            Assert.AreEqual(c.minCubsMultiplied, min_requiured.PowerOf);
        }

    }
}
