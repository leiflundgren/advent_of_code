package day02

import (
	"os"
	"testing"
)

var test_input string = `11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124`

var expected_invalids [][]int = nil

var id_ranges []Range

func sum(arr []int) int {
	n := 0
	for _, v := range arr {
		n += v
	}
	return n
}

func test_range(t *testing.T, i int) int {
	r := id_ranges[i]
	invalids := find_invalid_ids(r)
	if expected_invalids != nil && len(expected_invalids) > i {
		want := expected_invalids[i]
		if len(invalids) != len(want) {
			t.Errorf("range %d: got %d invalids, want %d", i, len(invalids), len(want))
		} else {
			for j := 0; j < len(want); j++ {
				if invalids[j] != want[j] {
					t.Errorf("range %d: invalids[%d]=%d, want[%d]=%d", i, j, invalids[j], j, want[j])
				}
			}
		}
	}

	return sum(invalids)
}

func Test_A(t *testing.T) {

	sum := 0
	for i := 0; i < len(id_ranges); i++ {
		sum += test_range(t, i)
	}

	expected_sum := 1227775554
	if sum != expected_sum {
		t.Errorf("Total sum of invalid IDs: got %d, want %d", sum, expected_sum)
	}
}

func TestInput(t *testing.T) {

	content, _ := os.ReadFile("input.txt")
	id_ranges = parse_IDs(string(content))

	expected_invalids = nil
	// Disable test for now

	// if err != nil {
	// 	panic(err)
	// }

	// //lines []string
	// lines := strings.FieldsFunc(string(content), func(c rune) bool { return c == '\n' || c == '\r' })

	// dials := ParseDials(lines)
	// zeroA := CountZerosA(dials) // 1145
	// zeroB := CountZerosB(dials) // 6561
	// fmt.Printf("Number of zeroes: A=%d B=%d\n", zeroA, zeroB)
}

func TestMain(m *testing.M) {

	id_ranges = parse_IDs(test_input)

	expected_invalids = [][]int{
		{11, 22},
		{99},
		{1010},
		{1188511885},
		{222222},
		{},
		{446446},
		{38593859},
	}

	exitVal := m.Run()

	os.Exit(exitVal)
}
