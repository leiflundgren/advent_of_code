mod lib {

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
    cost:u32,
    state:State,
}
impl Node {
    pub fn new(cost:u32) -> Self {
        Node { cost:cost, state:State::Normal }
    }
}
impl Default for Node {
    fn default() -> Self {
        Node::new(0)
    }
}


struct Coord {
    x:usize,
    y:usize,
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
    pub fn set(&mut self, pos:Coord, n:Node) -> () {
        self.nodes.set(pos.y, pos.x, n);
    }
    pub fn get(&self, pos:Coord) -> Option<&Node> {
        return self.nodes.get(pos.x, pos.y);
    }
    pub fn is_empty(&self) -> bool {
        return self.nodes.row_len() <= 0;
    }
}

fn parse_map(s:&str) -> Map {
    let lines: Vec<&str> = s.lines().collect();
    let mut m : Map = Map::new(lines.len(), lines[0].len());
    let mut y=0;
    lines.iter().for_each(|line: &&str| {
        let mut x = 0;
        line.chars().for_each(|c:char| {
            let d = c.to_digit(10).unwrap();
            let n = Node::new(d);
            m.set(Coord { x: x, y: y }, n);
            x+=1;
        });
        y+=1;
    });
    return m;
}


#[cfg(test)]
mod tests {
    


    // Note this useful idiom: importing names from outer (for mod tests) scope.
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

    #[test]
    fn test_hello_world() {
        println!("Hello, test!"); 
    }


    #[test]
    fn test_parse() {
        let m : Map = parse_map(INPUT_MAP);
        assert!(! m.is_empty())
    }

}
}