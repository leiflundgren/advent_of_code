package day03

import (
	"fmt"
	"os"
	"strings"
	"testing"
)

var test_input []string

func test_range(t *testing.T, i int, testName string, testInput []string, expected []int) int {
	maxj := find_max_joltage(testInput[i], testName == "A")

	if expected != nil && len(expected) > i {
		if maxj != expected[i] {
			t.Errorf("Test %s-%d: got %d, want %d", testName, i, maxj, expected[i])
			return -1
		}
	}
	fmt.Printf("Test %s-%d: max joltage: %d\n", testName, i, maxj)
	return maxj
}

func Test_A(t *testing.T) {

	expected := []int{98, 89, 78, 92}

	sum := 0
	for i := 0; i < len(test_input); i++ {
		sum += test_range(t, i, "A", test_input, expected)
	}

	expected_sum := 357
	if sum != expected_sum {
		t.Errorf("Total sum of invalid IDs: got %d, want %d", sum, expected_sum)
	}
}

// func Test_B(t *testing.T) {

// 	sum := 0
// 	for i := 0; i < len(id_ranges); i++ {
// 		sum += test_range(t, i, "B")
// 	}

// 	expected_sum := 4174379265
// 	if sum != expected_sum {
// 		t.Errorf("Total sum of invalid IDs: got %d, want %d", sum, expected_sum)
// 	}
// }

func TestInput(t *testing.T) {

	// Stop simple tests
	content, _ := os.ReadFile("input.txt")
	lines := strings.Split(string(content), "\n")

	sum := 0
	for i := 0; i < len(lines); i++ {
		sum += test_range(t, i, "A", lines, nil)
	}

	fmt.Printf("A: Total sum of invalid IDs: %d\n", sum) // 16854

	// sum = 0
	// for i := 0; i < len(id_ranges); i++ {
	// 	sum += test_range(t, i, "B")
	// }

	// fmt.Printf("B: Total sum of invalid IDs: %d\n", sum) // 44143124633
}

func TestMain(m *testing.M) {

	test_input = []string{
		"987654321111111",
		"811111111111119",
		"234234234234278",
		"818181911112111",
	}

	exitVal := m.Run()

	os.Exit(exitVal)
}
