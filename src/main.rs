use std::env;
use aoc_2023::module_runner::SolutionRunner;

fn help() {
    println!("usage:
day {{1..25}} <integer>
    The day to solve
part {{1|2}} <integer>
    The part to solve");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    match args.len() {
        3 => {
            let day: i32 = match args[1].parse() {
                Ok(x) if 1 <= x && x <= 25 => x,
                _ => {
                    help();
                    return
                }
            };
            let part: i32 = match args[2].parse() {
                Ok(x) if x == 1 || x == 2 => x,
                _ => {
                    help();
                    return
                }
            };
            let runner = SolutionRunner::build(day, part);
            runner.solve();
        }
        _ => help()
    }
    return
}