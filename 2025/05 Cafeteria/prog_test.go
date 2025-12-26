package day05

import (
	"fmt"
	"os"
	"slices"
	"strings"
	"testing"
	"time"
)

var test_input = parse_input(
	strings.Split(
		`3-5
10-14
16-20
12-18

1
5
8
11
17
32`, "\n"))

var expected_a = map[int]bool{1: false, 5: true, 8: false, 11: true, 17: true, 32: false}

//var expected_positions_b [][2]int

func Test_A(t *testing.T) {

	if len(test_input.Ranges) != 4 {
		t.Errorf("FAIL: Expected 4 ranges,  got %d", len(test_input.Ranges))
	}
	if len(test_input.IDs) != 6 {
		t.Errorf("FAIL: Expected 6 ranges,  got %d", len(test_input.IDs))
	}

	actual := test_input.find_fresh()
	if len(actual) != 3 {
		t.Errorf("FAIL: Expected 3 fresh things,  got %d", len(test_input.IDs))
	}

	for id, is_fresh := range expected_a {
		found := slices.Contains(actual, id)
		if found != is_fresh {
			t.Errorf("FAIL: ID %d expected fresh=%v, got %v", id, is_fresh, found)
		}
	}
}

func TestInput(t *testing.T) {

	t0 := time.Now()

	// Stop simple tests
	content, _ := os.ReadFile("input.txt")
	input := parse_input(strings.Split(string(content), "\n"))

	actual := input.find_fresh()

	fmt.Printf("A: Total sum of fresh: %d took %s\n", len(actual), time.Since(t0)) // 1363

	// t0 = time.Now()

	// sum := 0
	// for i := 0; ; i++ {

	// 	fmt.Printf("Iteration %d\n", i)
	// 	for _, line := range expanded {
	// 		fmt.Println(line)
	// 	}

	// 	accessible_rolls := find_rolls_with_n_free_edges(expanded, 5)

	// 	if len(accessible_rolls) == 0 {
	// 		break
	// 	}

	// 	sum += len(accessible_rolls)
	// 	fmt.Printf("iter %d  Found %d accessible rolls\n", i, len(accessible_rolls))

	// 	setIndices(accessible_rolls, '.', expanded)
	// }

	// fmt.Printf("B: Total sum of accessible rolls: %d took %s\n", sum, time.Since(t0)) // 8184

}

func TestMain(m *testing.M) {

	exitVal := m.Run()

	os.Exit(exitVal)
}
