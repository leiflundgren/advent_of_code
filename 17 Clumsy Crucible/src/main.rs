fn main() {
    println!("Hello, world!");
    let _g : i32 = add(1, 2);
    let _b : i32 = bad_add(1, 2);
}

pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

// This is a really bad adding function, its purpose is to fail in this
// example.
#[allow(dead_code)]
fn bad_add(a: i32, b: i32) -> i32 {
    a - b
}

#[cfg(test)]
mod tests;
