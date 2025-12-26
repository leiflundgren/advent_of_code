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

func Test_B(t *testing.T) {

	cpy := make([]Range, len(test_input.Ranges))
	copy(cpy, test_input.Ranges)
	slices.SortFunc(cpy, sort_ranges)
	sorted := make([]Range, 4)
	sorted[0] = make_range(3, 5)
	sorted[1] = make_range(10, 14)
	sorted[2] = make_range(12, 18)
	sorted[3] = make_range(16, 20)

	if !slices.Equal(cpy, sorted) {
		t.Errorf("FAIL: Expected sorted ranges %v, got %v", sorted, cpy)
	}

	actual := merge_intersecting_ranges(test_input.Ranges)
	if len(actual) != 2 {
		t.Errorf("FAIL: Expected 2 ranges,  got %d", len(test_input.IDs))
	}

	cnt := count_ranges(actual)
	if cnt != 14 {
		t.Errorf("FAIL: Expected total count of merged ranges to be 14, got %d", cnt)
	}
}

func TestInput(t *testing.T) {

	t0 := time.Now()

	// Stop simple tests
	content, _ := os.ReadFile("input.txt")
	test_input := parse_input(strings.Split(string(content), "\n"))

	actual := test_input.find_fresh()

	fmt.Printf("A: Total sum of fresh: %d took %s\n", len(actual), time.Since(t0)) // 1363

	t0 = time.Now()

	ranges := merge_intersecting_ranges(test_input.Ranges)

	cnt := count_ranges(ranges)
	fmt.Printf("B: Total sum of fresh ingredients: %d took %s\n", cnt, time.Since(t0)) // 8184

}

func TestMain(m *testing.M) {

	exitVal := m.Run()

	os.Exit(exitVal)
}
