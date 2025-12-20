package day03

import (
	"strings"
)

func add_outer_edges(lines []string) []string {
	linelen := len(lines[0])
	edge := strings.Repeat(".", linelen+2)
	newlines := make([]string, 0, len(lines)+2)
	newlines = append(newlines, edge)
	for _, line := range lines {
		newlines = append(newlines, "."+line+".")
	}
	newlines = append(newlines, edge)
	return newlines
}

func inner_points(lines []string) [][2]int {
	points := make([][2]int, (len(lines)-2)*(len(lines[0])-2))
	pos := 0
	for i := 1; i < len(lines)-1; i++ {
		for j := 1; j < len(lines[i])-1; j++ {
			points[pos] = [2]int{i, j}
			pos++
		}
	}
	return points
}

func num_free_edges(lines []string, i, j int) int {
	directions := [][2]int{{-1, 0}, {1, 0}, {0, -1}, {0, 1}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1}}
	free := 0
	for _, d := range directions {
		ni, nj := i+d[0], j+d[1]
		if lines[ni][nj] == '.' {
			free++
		}
	}
	return free
}

func find_rolls_with_n_free_edges(lines []string, n int) [][2]int {
	points := inner_points(lines)
	matching := make([][2]int, 0)
	for _, p := range points {
		i, j := p[0], p[1]
		if lines[i][j] != '@' {
			continue
		}

		free := num_free_edges(lines, i, j)
		if free >= n {
			matching = append(matching, [2]int{i, j})
		}
	}
	return matching
}
