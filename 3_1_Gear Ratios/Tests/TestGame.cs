using advent_of_code;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

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
            public bool isPossible;


            public Case(string input, Game expected, Set masterSet, bool isPossible)
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
                this.isPossible= isPossible;
            }

            public override string ToString()
            {
                return Input;
            }
        }

        public static Set MasterSet = new Set(12,13, 14);
        public readonly static Case[] cases = new Case[] {

            new Case("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", new Game(1, new Set(4, 0, 3), new Set(1,2,6), new Set(0,2,0)), MasterSet, true),
            new Case("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", new Game(2, new Set(0,2,1), new Set(1,3,4), new Set(0,1,1)), MasterSet, true),
            new Case("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", new Game(3, new Set(20,8,6), new Set(4,13,5), new Set(1,5, 0)), MasterSet, false),
            new Case("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", new Game(4, new Set(3,1,6), new Set(6,3,0), new Set(14,3,15)), MasterSet, false),
            new Case("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", new Game(5, new Set(6,3,1), new Set(1,2,2)), MasterSet, true),
        };

        [Test, TestCaseSource(nameof(cases))]
        public void TestParseGame(Case c)
        {
            Game actual = Game.Parse(c.Input);
            Assert.AreEqual(c.Expected, actual);

            bool possible = actual.IsPossible(c.masterSet);
            Assert.AreEqual(c.isPossible, possible);
        }

    }
}
