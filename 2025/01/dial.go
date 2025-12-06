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

func CountZeros(dials []Dial) int {
	idx := 50
	zeros := 0

	for _, d := range dials {
		idx = (idx + d.movement) % 100
		if idx == 0 {
			zeros++
		}
	}
	return zeros
}
