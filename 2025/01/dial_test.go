package day01

import (
	"strings"
	"testing"
)

func test_dial_helper(t *testing.T, dials []Dial, i int, movement int) {
	got := dials[i].movement
	want := movement

	if got != want {
		t.Errorf("got %q want %q", got, want)
	}
}

func TestDials(t *testing.T) {
	input :=
		`L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
`

	lines := strings.Split(input, "\n")

	dials := ParseDials(lines)

	if len(dials) != 10 {
		t.Fatalf("got %d dials, want 10", len(dials))
	}

	test_dial_helper(t, dials, 0, -68)
	test_dial_helper(t, dials, 1, -30)
	test_dial_helper(t, dials, 2, 48)
	test_dial_helper(t, dials, 3, -5)
	test_dial_helper(t, dials, 4, 60)
	test_dial_helper(t, dials, 5, -55)
	test_dial_helper(t, dials, 6, -1)
	test_dial_helper(t, dials, 7, -99)
	test_dial_helper(t, dials, 8, 14)
	test_dial_helper(t, dials, 9, -82)

	z := CountZeros(dials)
	if z != 3 {
		t.Fatalf("got %d zeroes, want 3", z)
	}

}
