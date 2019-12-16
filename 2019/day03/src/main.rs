use std::collections::HashSet;
use std::fs;

enum Step {
    R(isize),
    U(isize),
    L(isize),
    D(isize),
}

fn str_of_step(s: &Step) -> String {
    match s {
        Step::R(n) => format!("R{}", n),
        Step::L(n) => format!("L{}", n),
        Step::U(n) => format!("U{}", n),
        Step::D(n) => format!("D{}", n),
    }
}

// TODO: write as safe
unsafe fn steps(line: String) -> Vec<Step> {
    let parts = line.split(',');
    return parts
        .map(|x| {
            if x.len() < 2 {
                return Step::R(0);
            }
            let first = x.chars().next();
            let num: isize = x.get_unchecked(1..x.len()).parse().expect("bad number!");
            match first {
                Some('R') => Step::R(num),
                Some('L') => Step::L(num),
                Some('U') => Step::U(num),
                Some('D') => Step::D(num),
                _ => Step::R(0),
            }
        })
        .collect();
}

fn do_n(n: isize, pts: &mut HashSet<[isize; 2]>, pt: &mut [isize; 2], dx: isize, dy: isize) {
    let mut i = 0;
    while i < n {
        i += 1;
        pt[0] += dx;
        pt[1] += dy;
        pts.insert(*pt);
    }
}

fn points(steps: &Vec<Step>) -> HashSet<[isize; 2]> {
    let mut pts: HashSet<[isize; 2]> = HashSet::new();
    let mut cur = [0, 0];
    for step in steps {
        match step {
            Step::R(num) => do_n(*num, &mut pts, &mut (cur), 1, 0),
            Step::L(num) => do_n(*num, &mut pts, &mut (cur), -1, 0),
            Step::U(num) => do_n(*num, &mut pts, &mut (cur), 0, 1),
            Step::D(num) => do_n(*num, &mut pts, &mut (cur), 0, -1),
        }
    }
    pts
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("couldn't read file!");
    let lines: Vec<&str> = contents.lines().collect();
    let l1 = lines[0];
    let l2 = lines[1];

    unsafe {
        let steps1 = steps(l1.to_string());
        let steps2 = steps(l2.to_string());

        let points1 = points(&steps1);
        let points2 = points(&steps2);

        let mut intxs: Vec<[isize; 2]> = Vec::new();
        for pt in points2 {
            if points1.contains(&pt) {
                intxs.push(pt);
            }
        }

        let dists = intxs.iter().map(|pt| pt[0].abs() + pt[1].abs());
        let mut min = 0;
        if let Some(d) = dists.min() {
            min = d;
        }

        println!("part 1: min distance to an intersection is {}", min);
    }
}
