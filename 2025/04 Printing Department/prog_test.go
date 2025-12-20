package day03

import (
	"fmt"
	"os"
	"slices"
	"strings"
	"testing"
	"time"
)

var test_input = []string{
	"..@@.@@@@.",
	"@@@.@.@.@@",
	"@@@@@.@.@@",
	"@.@@@@..@.",
	"@@.@@@@.@@",
	".@@@@@@@.@",
	".@.@.@.@@@",
	"@.@@@.@@@@",
	".@@@@@@@@.",
	"@.@.@@@.@.",
}

var expected_positions_a [][2]int

func init_expected_positions() {

	lines := []string{
		"..xx.xx@x.",
		"x@@.@.@.@@",
		"@@@@@.x.@@",
		"@.@@@@..@.",
		"x@.@@@@.@x",
		".@@@@@@@.@",
		".@.@.@.@@@",
		"x.@@@.@@@@",
		".@@@@@@@@.",
		"x.x.@@@.x.",
	}

	expected_positions_a = make([][2]int, 0)
	for i, line := range lines {
		for j := 0; j < len(line); j++ {
			if line[j] == 'x' {
				expected_positions_a = append(expected_positions_a, [2]int{i + 1, j + 1})
			}
		}
	}
}

func Test_A(t *testing.T) {

	expanded := add_outer_edges(test_input)
	accessible_rolls := find_rolls_with_n_free_edges(expanded, 5)

	for _, p := range expected_positions_a {
		if !slices.Contains(accessible_rolls, p) {
			t.Errorf("FAIL: Position %v not found but expected", p)
		}
	}
	for _, p := range accessible_rolls {
		if !slices.Contains(expected_positions_a, p) {
			t.Errorf("FAIL: Position %v not found but expected", p)
		}
	}

	if len(accessible_rolls) != len(expected_positions_a) {
		t.Errorf("FAIL: Number of accessible rolls: got %d, want %d", len(accessible_rolls), len(expected_positions_a))
	}

	expected_sum := 13
	if len(accessible_rolls) != expected_sum {
		t.Errorf("FAIL: Total sum of accessible rolls: got %d, want %d", len(accessible_rolls), expected_sum)
	}
}

// func Test_B(t *testing.T) {

// 	expected := []int{987654321111, 811111111119, 434234234278, 888911112111}

// 	sum := 0
// 	for i := 0; i < len(test_input); i++ {
// 		sum += test_range(t, i, "B", test_input, expected)
// 	}

// 	expected_sum := 3121910778619
// 	if sum != expected_sum {
// 		t.Errorf("Total sum of invalid IDs: got %d, want %d", sum, expected_sum)
// 	}
// }

func TestInput(t *testing.T) {

	t0 := time.Now()

	// Stop simple tests
	content, _ := os.ReadFile("input.txt")
	input := strings.Split(string(content), "\n")

	expanded := add_outer_edges(input)
	accessible_rolls := find_rolls_with_n_free_edges(expanded, 5)

	fmt.Printf("A: Total sum of accessible rolls: %d took %s\n", len(accessible_rolls), time.Since(t0)) // 16854

	t0 = time.Now()
	//	fmt.Printf("B: Total sum of invalid IDs: %d took %s\n", sum, time.Since(t0)) // 16854

}

func TestMain(m *testing.M) {

	init_expected_positions()

	exitVal := m.Run()

	os.Exit(exitVal)
}
