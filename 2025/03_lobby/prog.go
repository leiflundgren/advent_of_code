package day03

import "strconv"

func find_max_index(s string, start int, end int) int {
	if start < 0 || start >= end {
		return -1
	}
	maxIdx := start
	for i := start + 1; i < end; i++ {
		if s[i] > s[maxIdx] {
			maxIdx = i
		}
	}
	return maxIdx
}

func indexesOfChar(s string, ch rune) []int {
	idxs := make([]int, 0)
	for i, r := range s {
		if r == ch {
			idxs = append(idxs, i)
		}
	}
	return idxs
}

func find_max_joltage(strBatteries string, isA bool) int {

	max := -1

	maxIdx := find_max_index(strBatteries, 0, len(strBatteries)-1)
	max_joltage := []rune(strBatteries)[maxIdx]

	indicies := indexesOfChar(strBatteries, max_joltage)

	for _, idx := range indicies {
		max2nd := find_max_index(strBatteries, 1+idx, len(strBatteries))
		if max2nd > 0 {
			snum := (string)(strBatteries[idx]) + (string)(strBatteries[max2nd])
			num, _ := strconv.Atoi(snum)
			if num > max {
				max = num
			}
		}
	}

	return max
}
