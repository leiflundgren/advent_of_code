#[allow(unused_imports)]
use std::str::Lines;

use array2d::Array2D;

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
    pub fn new(cost:i32) -> Self {
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
            nodes : Array2D::filled_with(Node::default(), height, width),
        }
    }
    pub fn set(&mut self, x:usize, y:usize, n:Node) -> () {
        self.nodes.set(x, y, n);
    }
    pub fn get(&self, x:usize, y:usize) -> Option<&Node> {
        return self.nodes.get(x, y);
    }
}

fn parse_map(s:&str) -> Map {
    let lines: Vec<&str> = s.lines().collect();
    let mut m : Map = Map::new(lines.len(), lines[0].len());
    let mut y=0;
    lines.iter().for_each(|line: &&str| {
        let mut x = 0;
        line.chars().for_each(|c:char| {
            let n = Node::new(c.to_digit(10).unwrap() as i32);
            m.set(x, y, n);
            x+=1;
        });
        y+=1;
    });
    return m;
}









#[cfg(test)]
mod tests;


fn main() {
    println!("Hello, world!");
}

