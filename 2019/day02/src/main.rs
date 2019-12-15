use std::fs;

fn main() {
    let contents = fs::read_to_string("input.txt").expect("couldn't read file!");
    let digs: Vec<&str> = contents.split(',').collect();
    let prog: Vec<usize> = digs.iter().map(|x| x.parse().expect("bad int")).collect();

    // part 1
    let part1 = run(&prog, 12, 2);
    println!("part1: {}", part1);

    // part 2
    // what init params yield 19690720?
    let n = prog.len();
    for x in 0..n {
        for y in 0..n {
            let result = run(&prog, x, y);
            if result == 19690720 {
                println!("x, y => result: {}, {} => {}", x, y, 100 * x + y);
            }
        }
    }
}

fn run(prog_init: &Vec<usize>, x: usize, y: usize) -> usize {
    let mut prog = prog_init.clone();
    prog[1] = x;
    prog[2] = y;

    let mut pc = 0;
    let mut op = &prog[pc];
    while *op != 99 {
        match *op {
            1 => {
                let a1 = prog[prog[pc + 1]];
                let a2 = prog[prog[pc + 2]];
                let dest = prog[pc + 3];
                prog[dest] = a1 + a2;
            }
            2 => {
                let a1 = prog[prog[pc + 1]];
                let a2 = prog[prog[pc + 2]];
                let dest = prog[pc + 3];
                prog[dest] = a1 * a2;
            }
            _ => {
                println!("bad op {}!", *op);
            }
        }

        pc += 4;
        op = &prog[pc];
    }
    return prog[0];
}
