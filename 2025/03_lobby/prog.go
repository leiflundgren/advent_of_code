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

var powerOfTen []int

// IntPow calculates n to the mth power. Since the result is an int, it is assumed that m is a positive power
func IntPow(n, m int) int {
	if m == 0 {
		return 1
	}

	if m == 1 {
		return n
	}

	result := n
	for i := 2; i <= m; i++ {
		result *= n
	}
	return result
}

func find_max_joltage(strBatteries string, isA bool) int {

	if !isA {

		length := 12
		powerOfTen = make([]int, length+1)
		powerOfTen[0] = 1
		for i := 1; i <= length; i++ {
			powerOfTen[i] = powerOfTen[i-1] * 10
		}
		return find_max_joltage_cached(strBatteries, 0, length, make(map[[2]int]int))
	}
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

func find_max_joltage_cached(strBatteries string, start int, length int, cache map[[2]int]int) int {

	if length == 0 {
		return 0
	}

	batlen := len(strBatteries)
	if length > 12 {
		panic("invalid argument: length > 12")
	}

	key := [2]int{start, length}
	if v, ok := cache[key]; ok {
		return v
	}

	var v int

	if batlen-start == length {
		v, _ = strconv.Atoi(strBatteries[start:])
	} else {
		// include first
		va, _ := strconv.Atoi(string(strBatteries[start]))
		pow := powerOfTen[length-1]
		vb := find_max_joltage_cached(strBatteries, start+1, length-1, cache)
		v1 := va*pow + vb

		// don't include first
		v2 := find_max_joltage_cached(strBatteries, start+1, length, cache)

		if v1 > v2 {
			v = v1
		} else {
			v = v2
		}
	}

	cache[key] = v
	return v
}
