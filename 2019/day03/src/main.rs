use std::collections::HashMap;
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

fn steps(line: String) -> Vec<Step> {
    let parts = line.split(',');
    return parts
        .map(|x| {
            if x.len() < 2 {
                return Step::R(0);
            }
            let first = &x[..1];
            let num: isize = x[1..].parse().expect("bad number!");
            match first {
                "R" => Step::R(num),
                "L" => Step::L(num),
                "U" => Step::U(num),
                "D" => Step::D(num),
                _ => Step::R(0),
            }
        })
        .collect();
}

fn do_n(
    n: isize,
    cur_dist: &mut isize,
    pts: &mut HashMap<[isize; 2], isize>,
    pt: &mut [isize; 2],
    dx: isize,
    dy: isize,
) {
    let mut i = 0;
    while i < n {
        i += 1;
        *cur_dist += 1;
        pt[0] += dx;
        pt[1] += dy;
        if !pts.contains_key(pt) {
            pts.insert(*pt, *cur_dist);
        }
    }
}

fn points(steps: &Vec<Step>) -> HashMap<[isize; 2], isize> {
    let mut pts = HashMap::new();
    let mut cur = [0, 0];
    let mut dist = 0;
    for step in steps {
        match step {
            Step::R(num) => do_n(*num, &mut dist, &mut pts, &mut (cur), 1, 0),
            Step::L(num) => do_n(*num, &mut dist, &mut pts, &mut (cur), -1, 0),
            Step::U(num) => do_n(*num, &mut dist, &mut pts, &mut (cur), 0, 1),
            Step::D(num) => do_n(*num, &mut dist, &mut pts, &mut (cur), 0, -1),
        }
    }
    pts
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("couldn't read file!");
    let lines: Vec<&str> = contents.lines().collect();
    let l1 = lines[0];
    let l2 = lines[1];

    let steps1 = steps(l1.to_string());
    let steps2 = steps(l2.to_string());

    let points1 = points(&steps1);
    let points2 = points(&steps2);

    // part 1
    let mut intxs = Vec::new();
    for (&pt, &dist) in &points2 {
        if points1.contains_key(&pt) {
            intxs.push(pt);
        }
    }

    let dists = intxs.iter().map(|pt| pt[0].abs() + pt[1].abs());
    let mut min = 0;
    if let Some(d) = dists.min() {
        min = d;
    }

    println!("part 1: min distance to an intersection is {}", min);

    // part 2
    let mut combined_steps = Vec::new();
    for (&pt, &dist2) in &points2 {
        if let Some(dist1) = points1.get(&pt) {
            combined_steps.push(dist1 + dist2);
        }
    }

    min = 0;
    if let Some(d) = combined_steps.iter().min() {
        min = *d;
    }
    println!("part 2: min combined steps to an intersection is {}", min);
}
