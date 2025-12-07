package day02

import (
	"fmt"
)

type Range struct {
	Start int
	End   int
}

func find_invalid_ids(r Range, isA bool) []int {
	invalids := make([]int, 0)
	for id := r.Start; id <= r.End; id++ {
		s := fmt.Sprintf("%d", id)
		if isA {
			if only_repeated_seqyences_twice(s) {
				invalids = append(invalids, id)
			}
		} else {
			if only_repeated_seqyences(s) {
				invalids = append(invalids, id)
			}
		}
	}
	return invalids
}

func only_repeated_seqyences(s string) bool {
	n := len(s)
	for i := 1; i < n; i++ {
		if (n % i) == 0 { // check len is devisible by i
			part1 := s[:i]

			all_match := true
			for j := i; j < n; j += i {
				partj := s[j : j+i]
				if partj != part1 {
					all_match = false
					break
				}
			}
			if all_match {
				return true
			}
		}
	}
	return false
}

func only_repeated_seqyences_twice(s string) bool {
	n := len(s)
	if n%2 != 0 {
		return false
	}
	half := n / 2
	return s[:half] == s[half:]
}

func parse_IDs(input string) []Range {
	parts := make([]Range, 0)
	n := len(input)
	if n == 0 {
		return parts
	}

	i := 0
	for i < n {
		// parse first number
		j := i
		for j < n && input[j] != '-' && input[j] != ',' {
			j++
		}
		astr := input[i:j]
		var a int
		fmt.Sscanf(astr, "%d", &a)

		// skip '-'
		if j < n && input[j] == '-' {
			j++
		}

		// parse second number
		k := j
		for k < n && input[k] != ',' {
			k++
		}
		var b int
		fmt.Sscanf(input[j:k], "%d", &b)

		r := Range{Start: a, End: b}
		parts = append(parts, r)

		// move past comma if present
		i = k

		for i < n && (input[i] == ',' || input[i] == '\n' || input[i] == '\r') {
			i++
		}
	}

	return parts
}
