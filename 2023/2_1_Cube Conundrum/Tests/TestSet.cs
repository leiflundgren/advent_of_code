using advent_of_code;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tests
{
    [TestFixture]
    public class TestSet
    {

        public class Case
        {
            public string Input;
            public Set Expected;

            public Case(string input, Set expected)
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
            }

            public override string ToString()
            {
                return Input;
            }
        }

        public readonly static Case[] cases = new Case[] { 
            new Case("3 blue, 4 red", new Set(4, 0, 3)),
            new Case("4 red,3 blue", new Set(4, 0, 3)),
            new Case("1 red, 2 green, 6 blue", new Set(1, 2, 6)) ,
            new Case("2 green, 1 red, 6 blue", new Set(1, 2, 6)) ,
        };

        [Test, TestCaseSource(nameof(cases))] 
        public void TestParseSet(Case c)
        {
            Set actual = Set.Parse(c.Input);
            Assert.AreEqual(c.Expected, actual);
        }

    }
}
