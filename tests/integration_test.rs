use aoc_2023::module_runner::SolutionRunner;

struct Solution {
    day: u8,
    part: u8,
    answer: String
}

impl Solution {
    fn new(day:u8, part:u8, answer_ptr: &str) -> Solution {
        let answer = answer_ptr.to_string();
        Solution {day, part, answer}
    }
}

#[test]
fn completed_solutions() {
    let solved = vec![
        Solution::new(1, 1, "56042"),
        Solution::new(1, 2, "55358")
    ];
    for s in solved {
        let actual = SolutionRunner::new(s.day, s.part).solve();
        assert!(actual.is_ok());
        assert_eq!(actual.unwrap(), s.answer);
    }
}