#[allow(unused_imports)]
use std::str::Lines;

use array2d::{Array2D, Error};

#[derive(Copy, Clone)]
enum State {
    Normal,
    Visited,
}
// impl Clone for State {
//     fn clone(&self) -> Self {
//         *self
//     }
// }


#[derive(Copy, Clone)]
struct Node {
    cost:i32,
    state:State,
}
impl Node {
    pub fn new(cost:i32) {
        Node { cost:cost, state:State::Normal }
    }
}
impl Default for Node {
    fn default() -> Self {
        Node::new(0)
    }
}

// impl<T> Copy for Node {}

// impl Clone for Node {
//     fn clone(&self) -> Self {
//         Node { cost:self.cost, state: self.state }
//     }
// }

struct Map {
    nodes:Array2D<Node>,

}
impl Map {
    pub fn new(width:usize, height:usize) -> Self {
        Self {
            nodes : Array2D::filled_with(Node::new(0), height, width),
        }
    }
}

fn parse_map(s:&str) -> Map {
    let lines: Vec<&str> = s.lines().collect();
    let mut m : Map = Map::new(lines.len(), lines[0].len());
    let y=0;
    lines.iter().for_each(|line: &str| {


        let x = 0;
        // for_each!(c in line.char() {
        //     let n = new Node {
        //         cost = c.to_digit(10).unwrap();
        //         state = State::Normal;
        //     }
        //     m.set(x, y, n);
        //     x+=1;
        // });
        y+=1;
    });
    return m;
}









#[cfg(test)]
mod tests;


fn main() {
    println!("Hello, world!");
}

