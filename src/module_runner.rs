use std::fs;
// use std::fmt;
// use std::io;
use crate::{error, days};

#[derive(Debug, Clone)]
pub struct SolutionRunner {
    day: u8,
    part: u8
}

impl SolutionRunner {
    pub fn solve(&self) -> Result<String, error::Error> {
        let filename = match self.day {
            x if x < 10 => format!("day0{}.txt", x),
            x => format!("day{}.txt", x)
        };
        let crate_root = env!("CARGO_MANIFEST_DIR");
        let data_dir = format!("{}/data/{}", &crate_root, &filename);
        let data = fs::read_to_string(data_dir);
        match data {
            Ok(d) => match (self.day, self.part) {
                (1, 1) => Ok(days::day01::part1(d)),
                (1, 2) => Ok(days::day01::part2(d)),
                // (2, 1) => Ok(days::day02::part1(d)),
                // (2, 2) => Ok(days::day02::part2(d)),
                // (3, 1) => Ok(days::day03::part1(d)),
                // (3, 2) => Ok(days::day03::part2(d)),
                // (4, 1) => Ok(days::day04::part1(d)),
                // (4, 2) => Ok(days::day04::part2(d)),
                // (5, 1) => Ok(days::day05::part1(d)),
                // (5, 2) => Ok(days::day05::part2(d)),
                // (6, 1) => Ok(days::day06::part1(d)),
                // (6, 2) => Ok(days::day06::part2(d)),
                // (7, 1) => Ok(days::day07::part1(d)),
                // (7, 2) => Ok(days::day07::part2(d)),
                // (8, 1) => Ok(days::day08::part1(d)),
                // (8, 2) => Ok(days::day08::part2(d)),
                // (9, 1) => Ok(days::day09::part1(d)),
                // (9, 2) => Ok(days::day09::part2(d)),
                // (10, 1) => Ok(days::day10::part1(d)),
                // (10, 2) => Ok(days::day10::part2(d)),
                // (11, 1) => Ok(days::day11::part1(d)),
                // (11, 2) => Ok(days::day11::part2(d)),
                // (12, 1) => Ok(days::day12::part1(d)),
                // (12, 2) => Ok(days::day12::part2(d)),
                // (13, 1) => Ok(days::day13::part1(d)),
                // (13, 2) => Ok(days::day13::part2(d)),
                // (14, 1) => Ok(days::day14::part1(d)),
                // (14, 2) => Ok(days::day14::part2(d)),
                // (15, 1) => Ok(days::day15::part1(d)),
                // (15, 2) => Ok(days::day15::part2(d)),
                // (16, 1) => Ok(days::day16::part1(d)),
                // (16, 2) => Ok(days::day16::part2(d)),
                // (17, 1) => Ok(days::day17::part1(d)),
                // (17, 2) => Ok(days::day17::part2(d)),
                // (18, 1) => Ok(days::day18::part1(d)),
                // (18, 2) => Ok(days::day18::part2(d)),
                // (19, 1) => Ok(days::day19::part1(d)),
                // (19, 2) => Ok(days::day19::part2(d)),
                // (20, 1) => Ok(days::day20::part1(d)),
                // (20, 2) => Ok(days::day20::part2(d)),
                // (21, 1) => Ok(days::day21::part1(d)),
                // (21, 2) => Ok(days::day21::part2(d)),
                // (22, 1) => Ok(days::day22::part1(d)),
                // (22, 2) => Ok(days::day22::part2(d)),
                // (23, 1) => Ok(days::day23::part1(d)),
                // (23, 2) => Ok(days::day23::part2(d)),
                // (24, 1) => Ok(days::day24::part1(d)),
                // (24, 2) => Ok(days::day24::part2(d)),
                // (25, 1) => Ok(days::day25::part1(d)),
                // (25, 2) => Ok(days::day25::part2(d)),
                (d, p) => Err(error::Error::NoSolution(error::ForDayPart::new(d, p)))
            }
            Err(e) => Err(error::Error::FileNotFound(e))
        }
    }
    pub fn new(day: u8, part: u8) -> SolutionRunner {
        SolutionRunner { day, part }

    }
}