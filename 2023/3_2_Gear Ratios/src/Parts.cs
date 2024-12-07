using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace advent_of_code
{
    public class Parts
    {
        public Parts(List<Item> items, List<(int l, int c)> gears)
        {
            Items = items;
            Gears = gears;
        }

        public List<int> PartNumbers => Items.ConvertAll(itm => itm.N);

        public List<(int l, int c)> Gears { get; private set; } = new List<(int l, int c)> { };
        public List<Item> Items { get; private set; }

        public static bool IsSymbol(char c)
        {
            return c != '\r' && c != '\n' && c != '.' && !('0' <= c && c <= '9');
        
        }

        public List<Item> FindAdjacent(int l, int c)
        {
            return Items.FindAll(itm => itm.IsAdjacant(l, c));
        }
        public int GearRatio(int l, int c)
        {
            var adjacent = FindAdjacent(l, c);
            if (adjacent.Count != 2)
                return 0;

            int ratio = 1;
            foreach (Item itm in adjacent)
                ratio *= itm.N;
            return ratio;
        }

        public int SumGearRatio()
        {
            return Gears.ConvertAll(g => GearRatio(g.l, g.c)).Sum();
        }

        public static Parts Parse(string input)
        {

            EngineSchematic map = new EngineSchematic(input);

            List<Item> items = new List<Item> ();

            for (int l = 0; l < map.Map.Length; l++)
            {
                string line = map.Map[l];
                int col_start = -1;
                for (int col = 0; ;++col)
                {
                    if (col >= line.Length)
                    {
                        if (col_start >= 0)
                        {
                            CreateItem(map, items, l, line, ref col_start, col);
                        }
                        break; // next line
                    }

                    char chr = line[col];
                    if (col_start < 0 && !char.IsDigit(chr))
                    {
                        continue;
                    }

                    if (col_start < 0)
                    {
                        col_start = col;
                    }
                    else if (!char.IsDigit(chr))
                    {
                        CreateItem(map, items, l, line, ref col_start, col);
                      
                    }
                }
            }

            List<(int l, int c)> Gears = new List<(int l, int c)> { };

            // 2nd iter, find all gears
            for (int l = 0; l < map.Map.Length; l++)
            {
                string line = map.Map[l];
                for (int c = 0; c < line.Length; ++c)
                {
                    if (line[c] == '*')
                        Gears.Add((l, c));
                }
            }

            return new Parts(items, Gears);

            static void CreateItem(EngineSchematic map, List<Item> ls, int l, string line, ref int col_start, int col)
            {
                string strN = line.Substring(col_start, col-col_start);
                int n = int.Parse(strN);
                Item itm = new Item(l, col_start, col, n);
                col_start = -1;

                if ( map.AdjacentToSymbol(itm) )
                {
                    Console.WriteLine($"    Adjacent {itm}");
                    ls.Add(itm);
                }
                else
                {
                    Console.WriteLine($"NOT Adjacent {itm}");
                }
            }
        }

        public class EngineSchematic
        {
            public string[] Map;

            public char CharAt(int l, int c) { return !IsOnMap(l, c) ? '\0' : Map[l][c]; }

            public EngineSchematic(string input)
            {
                Map = input.Split(new char[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);
            }

            public bool IsOnMap(int l, int c)
            {
                return l >= 0 && l < Map.Length && c >= 0 && c < Map[l].Length;
            }

            public bool AdjacentToSymbol(Item itm)
            {
                List<(int l, int c)> pos = itm.GetSurrounding();

                pos.RemoveAll( lc => !IsOnMap(lc.l, lc.c));

                foreach ( (int l, int c) in pos)
                {
                    char chr = CharAt(l, c);
                    if (chr == '\0') continue;
                    
                    if ( Parts.IsSymbol(chr) )
                        return true;
                }

                return false;
            }

        }

        public class Item
        {
            public int lineno;
            public int start_col;
            public int end_col;
            public int N;

            public Item() { }

            public Item(int lineno, int start_col, int end_col, int n)
                : this()
            {
                this.lineno = lineno;
                this.start_col = start_col;
                this.end_col = end_col;
                N = n;
            }

            public List<(int l, int c)> GetSurrounding()
            {
                List<(int,int)> res = new List<(int, int)>();

                // add strict above + below
                foreach (int col in Enumerable.Range(start_col-1, 2+end_col - start_col))
                {
                    res.Add((lineno - 1, col));
                    res.Add((lineno + 1, col));
                }

                // add right/left, incl diagonal
                res.Add((lineno, start_col-1));
                res.Add((lineno, end_col));
                res.Sort(new SortLineCol());
                return res;
            }

            public bool IsAdjacant(int l, int c)
            {
                return GetSurrounding().Contains((l, c));
            }

            public class SortLineCol : IComparer<(int l, int c)>
            {
                public int Compare((int l, int c) x, (int l, int c) y)
                {
                    int diff = x.l - y.l;
                    if ( diff == 0 ) diff = x.c - y.c;

                    return diff;
                }
            }

            public override string ToString()
            {
                return $"line:{lineno}  col:{start_col}-{end_col} N:{N}";
            }

        }


    }
}