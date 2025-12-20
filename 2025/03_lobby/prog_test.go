package day03

import (
	"fmt"
	"os"
	"strings"
	"testing"
	"time"
)

var test_input = []string{
	"987654321111111",
	"811111111111119",
	"234234234234278",
	"818181911112111",
}

func test_range(t *testing.T, i int, testName string, testInput []string, expected []int) int {
	maxj := find_max_joltage(testInput[i], testName == "A")

	if expected != nil && len(expected) > i {
		if maxj != expected[i] {
			t.Errorf("Test %s-%d: got %d, want %d", testName, i, maxj, expected[i])
			return -1
		}
	}
	// fmt.Printf("Test %s-%d: max joltage: %d\n", testName, i, maxj)
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

func Test_B(t *testing.T) {

	expected := []int{987654321111, 811111111119, 434234234278, 888911112111}

	sum := 0
	for i := 0; i < len(test_input); i++ {
		sum += test_range(t, i, "B", test_input, expected)
	}

	expected_sum := 3121910778619
	if sum != expected_sum {
		t.Errorf("Total sum of invalid IDs: got %d, want %d", sum, expected_sum)
	}
}

func TestInput(t *testing.T) {

	t0 := time.Now()

	// Stop simple tests
	content, _ := os.ReadFile("input.txt")
	lines := strings.Split(string(content), "\n")

	sum := 0
	for i := 0; i < len(lines); i++ {
		sum += test_range(t, i, "A", lines, nil)
	}

	fmt.Printf("A: Total sum of invalid IDs: %d took %s\n", sum, time.Since(t0)) // 16854

	t0 = time.Now()
	sum = 0
	// for i := 0; i < len(id_ranges); i++ {
	// 	sum += test_range(t, i, "B")
	// }

	fmt.Printf("B: Total sum of invalid IDs: %d took %s\n", sum, time.Since(t0)) // 16854

}

func TestMain(m *testing.M) {

	exitVal := m.Run()

	os.Exit(exitVal)
}
