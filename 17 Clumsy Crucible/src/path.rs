use std::{collections::VecDeque, mem};

use crate::map;

#[derive(PartialEq, Copy, Clone)]
pub enum Direction {
    North,
    East,
    South,
    West,
}

pub struct PathNode {
    x: i32,
    y: i32,
    cost: i32,
}

pub fn get_direction(n1:&PathNode, n2:&PathNode) -> Direction {
    if n1.x == n2.x {
        if n1.y == n2.y + 1 { Direction::South }
        else if n1.y == n2.y - 1 { Direction::North }
        else { panic!("Invalid direction n1:{x1},{y1} n2:{x2},{y2}", x1=n1.x, y1=n1.y, x2=n2.x, y2=n2.y) }
    }
    else if n1.y == n2.y {
        if n1.x == n2.x + 1 { Direction::East }
        else if n1.x == n2.x - 1 { Direction::West }
        else { panic!("Invalid direction n1:{x1},{y1} n2:{x2},{y2}", x1=n1.x, y1=n1.y, x2=n2.x, y2=n2.y) }
    }
    else { panic!("Invalid direction n1:{x1},{y1} n2:{x2},{y2}", x1=n1.x, y1=n1.y, x2=n2.x, y2=n2.y) }
}

pub struct Path {
    head : VecDeque<PathNode>
}

impl Path {
    pub fn new() -> Self {
        Path { head : VecDeque::new() }
    }

    pub fn get_direction(& self, depth:usize) -> Direction {
        
        if depth == 0 { 
            Direction::South 
        }
        else if depth <= self.head.len() {
            let n1 = self.head.get(depth-1).unwrap();
            let n2 = self.head.get(depth).unwrap();
            get_direction(n1, n2)
        }
        else { 
            panic!("Attempt to get depth {depth} when list.len is {len}", depth=depth, len=self.head.len())
        }        
    }

    // If we have travelled same direction last `depth` steps, return that direction. None otherwise.
    pub fn same_direction_last(& self, depth:usize) -> Option<Direction> {
        if depth <1 { return  None; }
        if self.head.len() < depth { return None; }

        let mut n0 : &PathNode = self.head.get(0).unwrap();
        let mut n1 : &PathNode = self.head.get(1).unwrap();

        let mut d1 = get_direction(n0, n1);
        
        for i in 2..depth {            
            let n2 = self.head.get(i).unwrap();
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
    use super::*;

    #[test]
    fn basics() {
        // let mut list = List::new();

        // // Check empty list behaves right
        // assert_eq!(list.pop(), None);

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