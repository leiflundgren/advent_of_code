//mod map {

#[allow(unused_imports)]
use std::str::Lines;

use array2d::Array2D;

#[derive(Copy, Clone)]
#[derive(Debug)]
enum State {
    Normal,
    Visited,
}
// impl Clone for State {
//     fn clone(&self) -> Self {
//         *self
//     }
// }



#[derive(Debug)]
#[derive(Copy, Clone)]
pub struct Coord {
    x:usize,
    y:usize,
}

// impl<T> Copy for Node {}

// impl Clone for Node {
//     fn clone(&self) -> Self {
//         Node { cost:self.cost, state: self.state }
//     }
// }

#[derive(Debug)]
pub struct Map {
    nodes:Array2D<i32>,

}
impl Map {
    pub fn new(width:usize, height:usize) -> Self {
        Self {
            nodes : Array2D::filled_with(0, height, width),
        }
    }
    pub fn set(&mut self, pos:Coord, cost:i32) -> () {
        self.nodes.set(pos.y, pos.x, cost);
    }
    pub fn get(&self, pos:Coord) -> Option<&i32> {
        return self.nodes.get(pos.y, pos.x);
    }
    pub fn is_empty(&self) -> bool {
        return self.nodes.row_len() <= 0;
    }

    pub fn get_height(&self) -> usize { return self.nodes.row_len() }
    pub fn get_width(&self) -> usize { return self.nodes.column_len() }

    pub fn parse(s0:&str) -> Self {
        let s = s0.trim();
        let lines: Vec<&str> = s.lines().collect();
        let width = lines[0].trim().len();
        let height = lines.len();
        let mut m : Map = Self::new(width, height);
        let mut y=0;
    
        lines.iter().for_each(|line: &&str| {
            let mut x = 0;
            line.chars().for_each(|c:char| {
                let p = c.to_digit(10);
                if p.is_some() {
                    m.set(Coord { x: x, y: y }, p.unwrap() as i32);
                    x+=1;
                }
            });
            y+=1;
        });
        return m;
    }

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
        println!("Hello, tst!"); 
    }

    fn parse_test_map() -> Map {
        return Map::parse(INPUT_MAP)
    }

    #[test]
    fn test_parse() {
        let m : Map = parse_test_map();
        assert!(! m.is_empty());

        {
            let c = Coord{ x:1, y:1};
            let n = m.get(c);
            assert!(n.is_some());
            assert_eq!(2, *n.unwrap());
        }


        {
            let c = Coord{ x:2, y:1};
            let n = m.get(c);
            assert!(n.is_some());
            assert_eq!(1, *n.unwrap());
        }
    }

} 
//} mod map;
