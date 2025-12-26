package day05

import (
	"fmt"
	"slices"
	"strings"
)

type Range struct {
	Start int
	End   int
}

// Implementing the String method from fmt.Stringer interface
func (r *Range) String() string {
	return fmt.Sprintf("[%d -- %d]", r.Start, r.End)
}

func make_range(start int, end int) Range {
	return Range{Start: start, End: end}
}
func sort_ranges(a Range, b Range) int {
	if a.Start != b.Start {
		return a.Start - b.Start
	} else {
		return a.End - b.End
	}
}

type Input struct {
	Ranges []Range
	IDs    []int
}

var Zero_Range = Range{Start: 0, End: 0}

func parse_IDs(input string) Range {

	j := strings.Index(input, "-")
	if j == -1 {
		panic("Invalid input format for Range: " + input)
	}

	var a int
	var b int

	fmt.Sscanf(input[:j], "%d", &a)
	fmt.Sscanf(input[j+1:], "%d", &b)

	return Range{Start: a, End: b}
}

func parse_input(lines []string) Input {
	ranges := make([]Range, 0)
	ids := make([]int, 0)

	reached_ids := false
	for _, line := range lines {
		if line == "" {
			reached_ids = true
			continue
		} else if !reached_ids {
			r := parse_IDs(line)
			ranges = append(ranges, r)
		} else {
			var id int
			fmt.Sscanf(line, "%d", &id)
			ids = append(ids, id)
		}
	}

	return Input{Ranges: ranges, IDs: ids}
}

func (r *Range) contains(id int) bool {
	return id >= r.Start && id <= r.End
}

func (inp *Input) ranges_contins(id int) bool {

	for _, r := range inp.Ranges {
		if r.contains(id) {
			return true
		}
	}
	return false
}

func (inp *Input) find_fresh() []int {
	fresh_ids := make([]int, 0)
	for _, id := range inp.IDs {
		if inp.ranges_contins(id) {
			fresh_ids = append(fresh_ids, id)
		}
	}
	return fresh_ids
}

func do_intersect(r1 Range, r2 Range) bool {
	return r1.Start <= r2.End && r2.Start <= r1.End || r2.Start <= r1.End && r1.Start <= r2.End
}

func merge_ranges(r1 Range, r2 Range) Range {
	//fmt.Printf("Merging %v and %v\n", r1, r2)
	return Range{Start: min(r1.Start, r2.Start), End: max(r1.End, r2.End)}
}

func merge_intersecting_ranges(ranges []Range) []Range {
	if len(ranges) <= 1 {
		return ranges
	}

	cpy := make([]Range, len(ranges))
	copy(cpy, ranges)
	slices.SortFunc(cpy, sort_ranges)

	ret := make([]Range, 0, len(ranges))
	r1 := cpy[0]
	for i, j := 0, 1; ; {

		if j == len(cpy) { // end
			ret = append(ret, r1)
			break
		}

		r2 := cpy[j]

		if !do_intersect(r1, r2) {
			ret = append(ret, r1)
			i = j
			j = i + 1
			r1 = r2
			continue
		}

		r1 = merge_ranges(r1, r2)
		j++
	}
	return ret
}

func count_ranges(ranges []Range) int {
	count := 0
	for _, r := range ranges {
		count += r.End - r.Start + 1
	}
	return count
}
