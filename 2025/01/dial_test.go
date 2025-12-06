package day01

import (
	"fmt"
	"os"
	"strings"
	"testing"
)

var test_input string = `L68
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

var dials []Dial

func test_dial_helper(t *testing.T, dials []Dial, i int, start int, movement int, zeroesA int, zeroesB int) int {
	got := dials[i].movement
	want := movement

	if got != want {
		t.Errorf("got %q want %q", got, want)
	}

	_, zA := turn(start, dials[i].movement, false, i)
	next, zB := turn(start, dials[i].movement, true, i)
	fmt.Printf("Move %d from %d %d steps to %d A:%d B:%d\n", i, start, got, next, zA, zB)

	if zA != zeroesA {
		t.Errorf("dial %d: got %d zeroes A, want %d", i, zA, zeroesA)
	}
	if zB != zeroesB {
		t.Errorf("dial %d: got %d zeroes B, want %d", i, zB, zeroesB)
	}

	return next
}

func TestBasicParse(t *testing.T) {
	n99, z := turn(1, -2, false, -1)
	if n99 != 99 {
		t.Fatalf("got %d, want 99", n99)
	}
	if z != 0 {
		t.Fatal("no zero when mobve 1 L2")
	}
}

func TestDials(t *testing.T) {

	if len(dials) != 10 {
		t.Fatalf("got %d dials, want 10", len(dials))
	}

	pos := 50
	pos = test_dial_helper(t, dials, 0, pos, -68, 0, 1)
	pos = test_dial_helper(t, dials, 1, pos, -30, 0, 0)
	pos = test_dial_helper(t, dials, 2, pos, 48, 1, 1)
	pos = test_dial_helper(t, dials, 3, pos, -5, 0, 0)
	pos = test_dial_helper(t, dials, 4, pos, 60, 0, 1)
	pos = test_dial_helper(t, dials, 5, pos, -55, 1, 1)
	pos = test_dial_helper(t, dials, 6, pos, -1, 0, 0)
	pos = test_dial_helper(t, dials, 7, pos, -99, 1, 1)
	pos = test_dial_helper(t, dials, 8, pos, 14, 0, 0)
	test_dial_helper(t, dials, 9, pos, -82, 0, 1)

	zeroA := CountZerosA(dials)
	if zeroA != 3 {
		t.Fatalf("got %d zeroes, want 3", zeroA)
	}

	zeroB := CountZerosB(dials)
	if zeroB != 6 {
		t.Fatalf("got %d zeroes, want 6", zeroB)
	}

}

func TestInput(t *testing.T) {
	content, err := os.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}

	//lines []string
	lines := strings.FieldsFunc(string(content), func(c rune) bool { return c == '\n' || c == '\r' })

	dials := ParseDials(lines)
	zeroA := CountZerosA(dials) // 1145
	zeroB := CountZerosB(dials) // 6561
	fmt.Printf("Number of zeroes: A=%d B=%d\n", zeroA, zeroB)
}

func TestMain(m *testing.M) {

	lines := strings.Split(test_input, "\n")
	dials = ParseDials(lines)

	exitVal := m.Run()

	os.Exit(exitVal)
}
