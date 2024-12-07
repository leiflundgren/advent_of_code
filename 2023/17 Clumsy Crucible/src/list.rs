//mod list {


use std::mem;

pub struct List<T> {
    head: Link<T>,
}

pub enum Link<T> {
    Empty,
    More(Box<Node<T> >),
}

pub struct Node<T> {
    elem: T,
    next: Link<T>,
}

impl<T> List<T> {
    pub fn new() -> Self {
        List { head: Link::Empty }
    }

    pub fn push(&mut self, elem: T) {
        let new_node = Box::new(Node {
            elem: elem,
            next: mem::replace(&mut self.head, Link::Empty),
        });

        self.head = Link::More(new_node);
    }

    pub fn pop(&mut self) -> Option<T> {
        match mem::replace(&mut self.head, Link::Empty) {
            Link::Empty => None,
            Link::More(node) => {
                self.head = node.next;
                Some(node.elem)
            }
        }
    }

    pub fn peek(&self, depth:i32) -> Option<&T> {

        let mut lnk = &self.head;
        let mut r : Option<&T> = None;

        for n in 0..depth+1  {
            r = match lnk {
                Link::Empty =>  None,
                Link::More(node) => {
                    lnk = &node.next;
                    Some(&node.elem)
                }
            }
        }
        return r
    }

    
    pub fn len(&self) -> i32 {

        fn len_inner<T>(lnk: &Link<T>) -> i32 {
            match lnk {
                Link::Empty => return 0,
                Link::More(node) => 1 + len_inner(&node.next)
            }
        }
        let mut lnk = &self.head;
        return len_inner(lnk);
    }


}

impl<T> Drop for List<T> {
    fn drop(&mut self) {
        let mut cur_link = mem::replace(&mut self.head, Link::Empty);

        while let Link::More(mut boxed_node) = cur_link {
            cur_link = mem::replace(&mut boxed_node.next, Link::Empty);
        }
    }
}

#[cfg(test)]
mod test {
    use super::List;

    #[test]
    fn basics() {
        let mut list = List::new();

        // Check empty list behaves right
        assert_eq!(list.pop(), None);

        assert_eq!(list.len(), 0);

        // Populate list
        list.push(1);
        list.push(2);
        list.push(3);

        assert_eq!(list.len(), 3);

        let n0 = list.peek(0);
        let s0: &i32 = n0.unwrap_or(& -1);

        assert_eq!(list.peek(0), Some(&3));
        assert_eq!(list.peek(1), Some(&2));
        assert_eq!(list.peek(2), Some(&1));
        assert_eq!(list.peek(3), None);
        assert_eq!(*list.peek(3).unwrap_or(&-1), -1);


        // Check normal removal
        assert_eq!(list.pop(), Some(3));
        assert_eq!(list.pop(), Some(2));

        // Push some more just to make sure nothing's corrupted
        list.push(4);
        list.push(5);

        // Check normal removal
        assert_eq!(list.pop(), Some(5));
        assert_eq!(list.pop(), Some(4));

        // Check exhaustion
        assert_eq!(list.pop(), Some(1));
        assert_eq!(list.pop(), None);
    }
} 
// } 
