use aoc_2023::module_runner::SolutionRunner;
use test_case::test_case;

#[test_case(1, 2, "55358")]
#[test_case(1, 1, "56042")]
#[test_case(2, 1, "2265")]
#[test_case(2, 2, "64097")]
#[test_case(3, 1, "532445")]
#[test_case(3, 2, "79842967")]
#[test_case(4, 1, "24542")]
#[test_case(4, 2, "8736438")]
fn completed_solutions(day: u8, part: u8, expected: &str) {
    let actual = SolutionRunner::new(day, part).solve().unwrap();
    assert_eq!(actual, expected, "actual: {} != expected: {}", actual, expected);
}
