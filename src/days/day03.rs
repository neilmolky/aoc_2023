use crate::error;
use std::fmt::Debug;
use std::ops::RangeInclusive;
use std::collections::{HashMap, HashSet};

#[derive(Clone, Copy)]
struct IdxLim {
    start: usize,
    stop: usize
}
#[derive(Clone, Copy)]
struct ArrayLim {
    v_lim: IdxLim,
    h_lim: IdxLim
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
struct Point{ i: usize, j: usize}
impl Point {
    fn new(i:usize, j:usize) -> Point {Point {i, j}}
    fn build(signed_i:i32, signed_j:i32, lim: &ArrayLim) -> Option<Point> {
        if signed_i < lim.v_lim.start as i32 || signed_i > lim.v_lim.stop as i32 || signed_j < lim.h_lim.start as i32 || signed_j > lim.h_lim.stop as i32 {
            None
        } else {
            let (i, j) = (signed_i as usize, signed_j as usize);
            Some(Point::new(i as usize, j as usize))
        }
    }
}

impl IdxLim {
    fn build(arr_len: usize) -> IdxLim {
        let start: usize = 0;
        let stop: usize = arr_len - 1;
        IdxLim { start, stop }
    }

    fn range(&self) -> RangeInclusive<usize> {
        self.start..=self.stop
    }

    fn contains(&self, index: &i32) -> bool {
        self.start as i32 <= *index && self.stop as i32 >= *index
    }
}

impl ArrayLim {
    fn build(s: &String) -> ArrayLim {
        let lim_acc: Option<(usize, usize)> = None;
        let (i, j) = s
            .lines()
            .enumerate()
            .fold(lim_acc, |acc, (v_idx, line)| match acc {
                None => Some((v_idx, line.len())),
                Some((_, j)) => Some((v_idx, j))
            }).unwrap();
        let v_lim = IdxLim::build(i + 1);
        let h_lim = IdxLim::build(j);
        ArrayLim {v_lim, h_lim}
    }
    fn neighbors(&self, points: &ContinuousPoints) -> HashSet<Point> {
        (-1..=1)
            .flat_map(|i| (-1..=1).map(move |j| (i, j)))
            .flat_map(|(i, j)| points.iter().map(move |p| (p.i as i32 + i, p.j as i32 + j)))
            .flat_map(|(i, j)| Point::build(i, j, self))
            .filter(|p| !points.contains(p))
            .collect()
    }
}
type ContinuousPoints = Vec<Point>;

struct Items {
    numbers: Vec<ContinuousPoints>,
    tools: HashMap<Point, char>
}

impl Items {
    fn build(input: &String) -> Items {
        let mut numbers: Vec<ContinuousPoints> = Vec::new();
        // 
        let mut tools: HashMap<Point, char> = HashMap::new();
        for (i, ln) in input.lines().enumerate() {
            // overwrite every line and remember to check at the end of the line if this is empty
            let mut digits: ContinuousPoints = Vec::new();
            for (j, c) in ln.chars().enumerate() {
                // parse digits and tools into their data structures
                if c.is_digit(10) {
                    digits.push(Point::new(i, j));
                } else {
                    if let [_] | [_, ..] = digits.as_slice() {
                        numbers.push(digits.clone());
                        digits = Vec::new();
                    }
                    if c != '.' {
                        tools.insert(Point::new(i, j), c);
                    }                          
                }
            }
            // check complete
            if !digits.is_empty() {
                numbers.push(digits.clone());
            }
        }
        Items { numbers, tools }

    }
}

pub fn part1(input: String) -> Result<String, error::Error> {
    let arr: Vec<Vec<char>> = input
        .lines()
        .map(|l| l.chars().collect())
        .collect();
    let lim = ArrayLim::build(&input);
    let i = Items::build(&input);
    let mut total: u32 = 0;
    for points in i.numbers {
        let integer:u32 = points
            .iter()
            .map(|p| arr[p.i][p.j])
            .fold(String::new(), |acc, x| format!("{acc}{x}"))
            .parse()
            .unwrap();
        if lim
            .neighbors(&points)
            .iter()
            .any(|n| i.tools.get(n).is_some()) {
            println!("({}, {}): {}", points[0].i, points[0].j, integer);
            total = total + integer

        }
    }
    Ok(total.to_string())
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
struct GearCounter {
    count: usize,
    product: u32
}
impl GearCounter {
    fn new(count: usize, product: u32) -> GearCounter {
        GearCounter { count, product }
    }
    fn modify(&mut self, value: u32) {
        self.count += 1;
        self.product *= value;
    }
}

pub fn part2(input: String) -> Result<String, error::Error> {
    let arr: Vec<Vec<char>> = input
        .lines()
        .map(|l| l.chars().collect())
        .collect();
    let lim = ArrayLim::build(&input);
    let i = Items::build(&input);
    let mut gear_map: HashMap<Point, GearCounter> = HashMap::new();
    for points in i.numbers {
        let integer:u32 = points
            .iter()
            .map(|p| arr[p.i][p.j])
            .fold(String::new(), |acc, x| format!("{acc}{x}"))
            .parse()
            .unwrap();
        lim
            .neighbors(&points)
            .iter()
            .filter(|n| i.tools.get(*n).filter(|t| **t == '*').is_some())
            // .reduce(|x, y| x)
            .for_each(|p| {
                gear_map
                    .entry(*p)
                    .and_modify(|c| c.modify(integer))
                    .or_insert(GearCounter::new(1, integer));
        });
    }
    let total = gear_map
        .values()
        .filter(|c| c.count == 2)
        .fold(0, |x, y| x + y.product);


    Ok(total.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &'static str = "467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..";
    #[test]
    fn test_neighpors_zero_corner() {
        let v_lim = IdxLim::build(5);
        let h_lim = IdxLim::build(5);
        let lim = ArrayLim { v_lim, h_lim };
        let points= vec!(Point::new(0,0));
        let expected: HashSet<Point>  = HashSet::from([Point::new(1, 0), Point::new(1, 1), Point::new(0, 1)]);
        let result: HashSet<Point>  = lim.neighbors(&points).iter().copied().collect();

        assert_eq!(result, expected);
    }
    #[test]
    fn test_neighpors_limit_corner() {
        let v_lim = IdxLim::build(5);
        let h_lim = IdxLim::build(5);
        let lim = ArrayLim { v_lim, h_lim };
        let points = vec!(Point::new(4, 4));
        let expected = HashSet::from([Point::new(3, 4), Point::new(3, 3), Point::new(4, 3)]);
        let result: HashSet<Point>  = lim.neighbors(&points).iter().copied().collect();
        assert_eq!(result, expected);
    }
    
    #[test]
    fn test_part1() {
        let input = INPUT.to_string();
        let result = part1(input);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "4361")
    }
    #[ignore]
    #[test]
    fn test_part2() {
        let input = INPUT.to_string();
        let result = part1(input);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "467835")
    }
}
