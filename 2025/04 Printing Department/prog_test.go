package day04

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
var expected_positions_b [][2]int

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

func Test_B(t *testing.T) {

	expanded := add_outer_edges(test_input)
	sum := 0

	for i := 0; i < 10; i++ {

		fmt.Printf("Iteration %d\n", i)
		for _, line := range expanded {
			fmt.Println(line)
		}
		fmt.Println("")

		accessible_rolls := find_rolls_with_n_free_edges(expanded, 5)

		if len(accessible_rolls) == 0 {
			break
		}

		// if len(expected_positions_b) > i {
		// 	for _, p := range expected_positions_b[i] {
		// 		if !slices.Contains(accessible_rolls, p) {
		// 			t.Errorf("FAIL: Position %v not found but expected", p)
		// 		}
		// 	}
		// 	for _, p := range accessible_rolls {
		// 		if !slices.Contains(expected_positions_b[i], p) {
		// 			t.Errorf("FAIL: Position %v not found but expected", p)
		// 		}
		// 	}

		// 	if len(accessible_rolls) != len(expected_positions_b[i]) {
		// 		t.Errorf("FAIL: Number of accessible rolls: got %d, want %d", len(accessible_rolls), len(expected_positions_b[i]))
		// 	}
		// }

		setIndices(accessible_rolls, '.', expanded)

		sum += len(accessible_rolls)
	}

	expected_sum := 43
	if sum != expected_sum {
		t.Errorf("FAIL: Total sum of accessible rolls: got %d, want %d", sum, expected_sum)
	}
}

func TestInput(t *testing.T) {

	t0 := time.Now()

	// Stop simple tests
	content, _ := os.ReadFile("input.txt")
	input := strings.Split(string(content), "\n")

	expanded := add_outer_edges(input)
	accessible_rolls := find_rolls_with_n_free_edges(expanded, 5)

	fmt.Printf("A: Total sum of accessible rolls: %d took %s\n", len(accessible_rolls), time.Since(t0)) // 1363

	t0 = time.Now()

	sum := 0
	for i := 0; ; i++ {

		fmt.Printf("Iteration %d\n", i)
		for _, line := range expanded {
			fmt.Println(line)
		}

		accessible_rolls := find_rolls_with_n_free_edges(expanded, 5)

		if len(accessible_rolls) == 0 {
			break
		}

		sum += len(accessible_rolls)
		fmt.Printf("iter %d  Found %d accessible rolls\n", i, len(accessible_rolls))

		setIndices(accessible_rolls, '.', expanded)
	}

	fmt.Printf("B: Total sum of accessible rolls: %d took %s\n", sum, time.Since(t0)) // 8184

}

func TestMain(m *testing.M) {

	init_expected_positions()

	exitVal := m.Run()

	os.Exit(exitVal)
}
