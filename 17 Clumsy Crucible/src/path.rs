use std::{collections::VecDeque, fmt::{self, Debug}, mem};

use crate::map;

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
    head : VecDeque<PathNode>
}

impl Path {
    pub fn new() -> Self {
        Path { head : VecDeque::new() }
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

        let mut d1 = get_direction(n0, n1);
        
        for i in 2..depth {            
            let n2: Option<&PathNode> = self.head.get(i);
            let d2 = get_direction(n1, n2);
            if d1 != d2 { return None; } // changed dir within depth

            n1 = n2;
            d1 = d2;
        }

        return Some(d1);
    }

    pub fn possible_next_all(& self, x:usize, y:usize, max_x:usize, max_y:usize) -> Vec<Direction> {
        let repeat_dir = self.same_direction_last(3);
        let mut dirs : Vec<Direction> = vec![Direction::North, Direction::East, Direction::West, Direction::South];

        dirs
        .retain(|&d| 
            match repeat_dir {
                None => true,
                Some(rd) => d != rd
            }             
            && match d {
                    Direction::North => y > 0 ,
                    Direction::East => x < max_x ,
                    Direction::South => y < max_y ,
                    Direction::West => x > 0,
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

}

#[cfg(test)]
mod test {
    use std::f32::consts::E;

    use super::*;

    #[test]
    fn basics() {
        let mut p = Path::new();

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
} 