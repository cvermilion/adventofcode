use std::fs;

fn main() {
    let contents = fs::read_to_string("input.txt").expect("couldn't read file!");
    let lines: Vec<&str> = contents.lines().collect();

    // part 1
    let mut fuel: i32 = 0;
    for line in &lines {
        let x: i32 = line.parse().expect("bad number!");
        fuel += (x / 3) - 2;
    }
    println!("total fuel required (part 1): {}", fuel);

    // part 2
    fuel = 0;
    for line in &lines {
        let mut x: i32 = line.parse().expect("bad number!");
        loop {
            let next_fuel = (x / 3) - 2;
            if next_fuel > 0 {
                fuel += next_fuel;
                x = next_fuel;
            } else {
                break;
            }
        }
    }
    println!("total fuel required (part 2): {}", fuel);
}
