package day02

import (
	"fmt"
	"os"
	"testing"
)

var test_input string = `11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124`

var expected_invalids_A [][]int = nil
var expected_invalids_B [][]int = nil

var id_ranges []Range

func sum(arr []int) int {
	n := 0
	for _, v := range arr {
		n += v
	}
	return n
}

func test_range(t *testing.T, i int, testName string) int {
	r := id_ranges[i]
	var expected_invalids_ [][]int
	var want []int = nil

	if testName == "A" {
		expected_invalids_ = expected_invalids_A
	} else {
		expected_invalids_ = expected_invalids_B
	}
	if expected_invalids_ != nil && len(expected_invalids_) > i {
		want = expected_invalids_[i]
	}

	invalids := find_invalid_ids(r, testName == "A")
	str_ids := ""
	for _, v := range invalids {
		str_ids += fmt.Sprintf("%d ", v)
	}
	if want != nil {
		if len(invalids) != len(want) {
			t.Errorf("test %s range %d: got %d invalids, want %d\n%s", testName, i, len(invalids), len(want), str_ids)
		} else {
			for j := 0; j < len(want); j++ {
				if invalids[j] != want[j] {
					t.Errorf("test %s range %d: invalids[%d]=%d, want[%d]=%d", testName, i, j, invalids[j], j, want[j])
				}
			}
		}
	}

	return sum(invalids)
}

func Test_A(t *testing.T) {

	sum := 0
	for i := 0; i < len(id_ranges); i++ {
		sum += test_range(t, i, "A")
	}

	expected_sum := 1227775554
	if sum != expected_sum {
		t.Errorf("Total sum of invalid IDs: got %d, want %d", sum, expected_sum)
	}
}

func Test_B(t *testing.T) {

	sum := 0
	for i := 0; i < len(id_ranges); i++ {
		sum += test_range(t, i, "B")
	}

	expected_sum := 4174379265
	if sum != expected_sum {
		t.Errorf("Total sum of invalid IDs: got %d, want %d", sum, expected_sum)
	}
}

func TestInput(t *testing.T) {

	// Stop simple tests
	expected_invalids_A = nil
	expected_invalids_B = nil

	content, _ := os.ReadFile("input.txt")
	id_ranges = parse_IDs(string(content))

	sum := 0
	for i := 0; i < len(id_ranges); i++ {
		sum += test_range(t, i, "A")
	}

	fmt.Printf("A: Total sum of invalid IDs: %d\n", sum)

	sum = 0
	for i := 0; i < len(id_ranges); i++ {
		sum += test_range(t, i, "B")
	}

	fmt.Printf("B: Total sum of invalid IDs: %d\n", sum) // 44143124633
}

func TestMain(m *testing.M) {

	id_ranges = parse_IDs(test_input)

	expected_invalids_A = [][]int{
		{11, 22},
		{99},
		{1010},
		{1188511885},
		{222222},
		{},
		{446446},
		{38593859},
	}

	expected_invalids_B = [][]int{
		{11, 22},
		{99, 111},
		{999, 1010},
		{1188511885},
		{222222},
	}

	exitVal := m.Run()

	os.Exit(exitVal)
}
