use crate::list::List;
use crate::list::Link;
use crate::list::Node;
use crate::map;

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
    head : List<PathNode>
}

impl Path {
    pub fn new() -> Self {
        Path { head : List::new() }
    }

    pub fn get_direction(& self, depth:i32) -> Direction {
        let mut lnk = &self.head;

        for n in 0..depth  {
            match lnk {
                Link::Empty => None,
                Link::More(node) => {
                    lnk = &node.next;
                }
            }
        }

        match self.head.peek(0) {
            Link::Empty => Direction::South,
            Link::More(node) => *node.elem            
        }
    }

    // pub fn sameDirectionLast

    pub fn possible_next_all(& self) {
        not_impl!()
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