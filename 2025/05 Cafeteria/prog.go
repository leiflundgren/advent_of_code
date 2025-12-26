package day05

import (
	"fmt"
	"strings"
)

type Range struct {
	Start int
	End   int
}

type Input struct {
	Ranges []Range
	IDs    []int
}

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
