fn add1(n: &mut [u32; 6]) {
    n[5] += 1;
    // do the carries
    for i in (1..6).rev() {
        if n[i] == 10 {
            n[i] = 0;
            n[i - 1] += 1;
        }
    }
    // bump up each digit to at least the previous one
    // effectively just skips numbers whose digits aren't sorted
    for i in 1..6 {
        if n[i - 1] > n[i] {
            n[i] = n[i - 1];
        }
    }
}

fn test1(n: &[u32; 6]) -> bool {
    // check for two consecutive digits;
    // our add function ensures digits are sorted
    for i in 1..6 {
        if n[i] == n[i - 1] {
            return true;
        }
    }
    return false;
}

fn test2(n: &[u32; 6]) -> bool {
    // check for two consecutive digits
    // that are NOT part of more than two consecutive digits

    // first check the ends
    if (n[0] == n[1] && n[1] != n[2]) || (n[4] == n[5] && n[3] != n[4]) {
        return true;
    }

    // now do the interior -- match that doesn't match its boundaries
    for i in 1..4 {
        if (n[i] == n[i + 1]) && (n[i] != n[i - 1]) && (n[i] != n[i + 2]) {
            return true;
        }
    }
    return false;
}

fn main() {
    let start: [u32; 6] = [3, 8, 2, 3, 4, 5];
    let end = [8, 4, 3, 1, 6, 7];

    // part 1
    let mut cur = start.clone();
    let mut total = 0;

    while cur < end {
        if test1(&cur) {
            total += 1;
        }
        add1(&mut cur);
    }

    println!("part1 total: {}", total);

    // part 2
    cur = start.clone();
    total = 0;

    while cur < end {
        if test2(&cur) {
            total += 1;
        }
        add1(&mut cur);
    }

    println!("part2 total: {}", total);
}
