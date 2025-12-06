package day01

import (
	"fmt"
)

type Direction rune

const (
	Left  = 'L'
	Right = 'R'
)

var dirName = map[Direction]string{
	Left:  "L",
	Right: "R",
}

func (ss Direction) String() string {
	return dirName[ss]
}

type Dial struct {
	movement int
}

func getDirection(self Dial) Direction {
	if self.movement < 0 {
		return Left
	} else {
		return Right
	}
}

func parseDial(input string) Dial {
	var dir rune
	var n int
	if _, err := fmt.Sscanf(input, "%c%d", &dir, &n); err != nil {
		return Dial{}
	}
	if dir == Left {
		n = -n
	}
	return Dial{movement: n}
}

func ParseDials(inputs []string) []Dial {
	res := make([]Dial, 0, len(inputs))
	for _, s := range inputs {
		if s == "" {
			continue
		}
		res = append(res, parseDial(s))
	}
	return res
}

func abs_int(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func sign_int(n int) int {
	if n < 0 {
		return -1
	}
	return 1
}

// / returns [new position] and [number of zeroes crossed]
func turn(start int, movement int, test_b bool, idx int) (int, int) {
	new := (start + movement)
	newPos := new % 100

	sign := sign_int(movement)
	steps := abs_int(movement)

	at_zero := 0
	zeroesPassed := 0

	if test_b {
		if sign >= 0 {
			zeroesPassed = abs_int(start+movement) / 100
		} else {
			moves_beyond_zero := steps - start
			zeroesPassed = moves_beyond_zero / 100
		}

		// if newPos == 0 && start != 0 {
		// 	at_zero = 1
		// } else
		if sign < 0 && steps >= start && start > 0 { // left over zero
			at_zero = 1
		}

		// else if start < newPos && movement < 0 { // left over zero
		// 	at_zero = 1
		// } else if start > 0 && newPos < 0 && movement < 0 { // left over zero
		// 	at_zero = 1
		// } else if start > newPos && movement > 0 { // right over zero
		// 	at_zero = 1
		// }
	} else { // A
		if newPos == 0 {
			at_zero = 1
		}
	}

	if newPos < 0 {
		newPos += 100
	}
	return newPos, zeroesPassed + at_zero
}

func CountZerosA(dials []Dial) int {
	idx := 50
	zeros := 0

	for _, d := range dials {
		next, z := turn(idx, d.movement, false, -1)
		zeros += z
		idx = next
	}
	return zeros
}

func CountZerosB(dials []Dial) int {
	idx := 50
	zeros := 0

	for _, d := range dials {
		next, z := turn(idx, d.movement, true, -1)
		zeros += z
		idx = next
	}
	return zeros
}
