use std::{collections::VecDeque, fmt::{self, Debug}, mem};

use crate::map::Map;
use crate::map::Coord;

#[derive(PartialEq, Copy, Clone, Debug)]
pub enum Direction {
    North,
    East,
    South,
    West,
}

#[derive(Debug)]
pub struct PathNode {
    x: i32,
    y: i32,
    cost: i32,
}

impl PathNode{
    pub fn new(x: i32,y: i32, cost: i32,)  -> Self {
        PathNode { x : x, y : y, cost : cost }
    }
}

// Implement `Display` for `PathNode`.
impl fmt::Display for PathNode {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // Use `self.number` to refer to each positional data point.
        write!(f, "({}, {}): {}", self.x, self.y, self.cost)
    }
}


pub fn get_direction(o_n1:Option<&PathNode>, o_n2:Option<&PathNode>) -> Direction {
    match o_n1 {
        None => Direction::South,
        Some(n1) => { 
            match o_n2 {
                None => panic!("2nd node is None. Cannot deduce direction"),
                Some(n2) => 
                { 
                    if n1.x == n2.x {
                        if n1.y + 1 == n2.y { Direction::South }
                        else if n1.y == n2.y + 1 { Direction::North }
                        else { panic!("Invalid direction n1:{x1},{y1} n2:{x2},{y2}", x1=n1.x, y1=n1.y, x2=n2.x, y2=n2.y) }
                    }
                    else if n1.y == n2.y {
                        if n1.x + 1 == n2.x { Direction::East }
                        else if n1.x == n2.x + 1 { Direction::West }
                        else { panic!("Invalid direction n1:{x1},{y1} n2:{x2},{y2}", x1=n1.x, y1=n1.y, x2=n2.x, y2=n2.y) }
                    }
                    else { panic!("Invalid direction n1:{x1},{y1} n2:{x2},{y2}", x1=n1.x, y1=n1.y, x2=n2.x, y2=n2.y) }
                }
            }
        }
    }
}

pub struct Path {
    head : VecDeque<PathNode>,
    map : Map,
}

impl Path {
    /// Creates a new Path
    /// x_min/y_min are inclusive  x_max/y_max are exclusive
    /// I.e if the coordinates are 0--10, min value for coord i 0, max value used is 9
    pub fn new(map: Map ) -> Self {
        Path { head : VecDeque::new(), map : map }
    }

    pub fn get_direction(& self, depth:usize) -> Direction {
        
        let len : usize = self.head.len();
        
        if depth > len { 
            Direction::South 
        }
        else if depth < len {
            let n2 = self.head.get(depth);
            let n1 = self.head.get(depth+1);
            get_direction(n1, n2)
        }
        else { 
            panic!("Attempt to get depth {depth} when list.len is {len}")
        }        
    }

    pub fn get_x_min(&self) -> i32 { 0 }
    pub fn get_y_min(&self) -> i32 { 0 }
    pub fn get_x_max(&self) -> i32 { self.map.get_width() as i32 }
    pub fn get_y_max(&self) -> i32 { self.map.get_height() as i32 }

    pub fn add_step(&mut self, x:i32, y:i32, cost:i32) {
        assert!( match self.head.front() {
            None => true,
            Some(front) => (front.x - x).abs() == 1 || (front.y - y).abs() == 1
        });
        self.head.push_front(PathNode::new(x, y, cost));
    }

    // If we have travelled same direction last `depth` steps, return that direction. None otherwise.
    pub fn same_direction_last(& self, depth:usize) -> Option<Direction> {
        if depth <1 { return  None; }
        if self.head.len() <= depth { return None; }

        let mut n0 : Option<&PathNode> = self.head.get(0);
        let mut n1 : Option<&PathNode> = self.head.get(1);

        // Remember, nodes are stored latest first, so we moved from n1 -> n0
        let mut d1 = get_direction(n1, n0);
        
        for i in 2..depth {            
            let n2: Option<&PathNode> = self.head.get(i);
            let d2 = get_direction(n2, n1);
            if d1 != d2 { return None; } // changed dir within depth

            n1 = n2;
            d1 = d2;
        }

        return Some(d1);
    }

    pub fn possible_next_all(& self, x:i32, y:i32) -> Vec<Direction> {
        let repeat_dir = self.same_direction_last(3);
        let mut dirs : Vec<Direction> = vec![Direction::North, Direction::East, Direction::West, Direction::South];

        dirs
        .retain(|&d| 
            match repeat_dir {
                None => true,
                Some(rd) => d != rd
            }             
            && match d {
                    Direction::North => y > self.get_y_min(),
                    Direction::West => x > self.get_x_min(),
                    Direction::South => y+1 < self.get_y_max(),
                    Direction::East => x+1 < self.get_x_max(),
            });

            // .filter(|&d| match d {
                //     Direction::North => y > 0 && repeat_dir != Some(Direction::North),
                //     Direction::East => x < max_x && repeat_dir != Some(Direction::East),
                //     Direction::South => y < max_y && repeat_dir != Some(Direction::South), 
                //     Direction::West => x > 0 && repeat_dir != Some(Direction::West),
                // })        
                // .collect();  
                
                // unimplemented!("not yet");
                return dirs;
    }

    pub fn guesstimate_cost_distance(manhattan_distance:usize, unit_cost_estimate:f32) -> f32 {
        return unit_cost_estimate * (manhattan_distance as f32)
    }

    pub fn get_manhattan_distance(x1:i32, y1:i32, x2:i32, y2:i32) -> usize {
        return ((x1-x2).abs() + (y1-x2).abs()) as usize
    }
    pub fn guesstimate_best_direction(&self) -> Direction {
        unimplemented!("not get");
    }

}

#[cfg(test)]
mod test {
    use std::f32::consts::E;

    use super::*;

    static INPUT_MAP: &str = r#"
    2413432311323
    3215453535623
    3255245654254
    3446585845452
    4546657867536
    1438598798454
    4457876987766
    3637877979653
    4654967986887
    4564679986453
    1224686865563
    2546548887735
    4322674655533"#;

    fn parse_test_map() -> Map {
        return Map::parse(INPUT_MAP)
    }

    #[test]
    fn basics() {
        let test_map : Map = parse_test_map();
        let mut p = Path::new(test_map);

        p.add_step(0, 0,10);

        assert_eq!(p.get_direction(0), Direction::South);

        p.add_step(0, 1,20);

        assert_eq!(p.get_direction(0), Direction::South);
        assert_eq!(p.get_direction(1), Direction::South);

        p.add_step(1, 1,20);

        assert_eq!(p.get_direction(0), Direction::East);
        assert_eq!(p.get_direction(1), Direction::South);
        assert_eq!(p.get_direction(2), Direction::South);

        p.add_step(1, 0,20);

        assert_eq!(p.get_direction(0), Direction::North);
        assert_eq!(p.get_direction(1), Direction::East);
        assert_eq!(p.get_direction(2), Direction::South);
        assert_eq!(p.get_direction(3), Direction::South);

        p.add_step(0, 0,20);
        
        assert_eq!(p.get_direction(0), Direction::West);
        assert_eq!(p.get_direction(1), Direction::North);
        assert_eq!(p.get_direction(2), Direction::East);
        assert_eq!(p.get_direction(3), Direction::South);
        assert_eq!(p.get_direction(4), Direction::South);
        
        let possible = p.possible_next_all(1, 0);
        assert_eq!(possible, vec![Direction::East, Direction::West, Direction::South]);

        // // Populate list
        // list.push(1);
        // list.push(2);
        // list.push(3);

        // // Check normal removal
        // assert_eq!(list.pop(), Some(3));
        // assert_eq!(list.pop(), Some(2));

        // // Push some more just to make sure nothing's corrupted
        // list.push(4);
        // list.push(5);

        // // Check normal removal
        // assert_eq!(list.pop(), Some(5));
        // assert_eq!(list.pop(), Some(4));

        // // Check exhaustion
        // assert_eq!(list.pop(), Some(1));
        // assert_eq!(list.pop(), None);
    }

    #[test]
    fn same_direction_last() {
        let test_map : Map = parse_test_map();
        let mut p = Path::new(test_map);

        
        let mut d: Option<Direction> = None;
        d = p.same_direction_last(1);
        assert_eq!(None, d);

        p.add_step(0, 0,10);
        d = p.same_direction_last(1);
        assert_eq!(None, d);

        p.add_step(0, 1,20);
        assert_eq!(Some(Direction::South), p.same_direction_last(1));

        p.add_step(0, 2,20);
        assert_eq!(Some(Direction::South), p.same_direction_last(1));
        assert_eq!(Some(Direction::South), p.same_direction_last(2));

        p.add_step(0, 2,20);
        assert_eq!(Some(Direction::South), p.same_direction_last(1));
        assert_eq!(Some(Direction::South), p.same_direction_last(2));
        assert_eq!(Some(Direction::South), p.same_direction_last(3));

        p.add_step(1, 2,20);
        assert_eq!(None, p.same_direction_last(1));
        assert_eq!(Some(Direction::South), p.same_direction_last(2));
        assert_eq!(Some(Direction::South), p.same_direction_last(3));

    }
} 