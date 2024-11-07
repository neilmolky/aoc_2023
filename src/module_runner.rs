use std::fs;
use std::env::current_exe;
use crate::day01;

pub struct SolutionRunner {
    day: i32,
    part: i32
}

impl SolutionRunner {
    pub fn solve(&self) {
        let data = &self.data();
        match data {
            Ok(x) => match (&self.day, &self.part) {
                (1, 1) => day01::part1(x),
                (d, p) => println!("solution not implemented for day {} part {}", d, p)
            }
            Err(e) => eprint!("{}", e.to_string())
        }
    }
    pub fn build(day: i32, part: i32) -> SolutionRunner {
        return SolutionRunner { day, part }
    }
    fn data(&self) -> Result<String, std::io::Error> {
        let filename = match self.day {
            x if x < 10 => format!("day_0{}.txt", x),
            x => format!("day_{}.txt", x),
        };
        let data_dir = format!(
            "{}/data/{}",
            env!("CARGO_MANIFEST_DIR"), 
            filename
        );
        fs::read_to_string(data_dir)
    }
}