use crate::error;
enum FirstLast<T> {
    Empty,
    Full(T, T)
}


impl FirstLast<char> {
    fn get_string(&self) -> String{
        match &self {
            FirstLast::Full(x, y) => format!("{}{}", x, y),
            FirstLast::Empty => panic!("can't get from empty FirstLast")
        }
    }
}

const NUMS: &'static str  = "one
two
three
four
five
sixstatic
seven
eight
nine";

fn parse_number(number: &str) -> char {
    if number.len() == 1 {
        number.parse().unwrap()
    } else {
        NUMS.lines()
            .enumerate()
            .filter(|(_, y)| y.starts_with(number))
            .map(|x| x.0 + 1)
            .next()
            .unwrap()
            .to_string()
            .parse()
            .unwrap()
    }
}

fn span(acc: FirstLast<char>, next: char) -> FirstLast<char> {

    match (acc, next) {
        (FirstLast::Empty, _) => FirstLast::Full(next, next),
        (FirstLast::Full(a, _), _) =>FirstLast::Full(a, next)
    }
}

pub fn part1(_input: String) -> Result<String, error::Error> {
    let total: String = _input
        .lines()
        .map(|line| {
            let container: FirstLast<char> = FirstLast::Empty;
            let digits: u32 = line
                .chars()
                .filter(|c| c.is_ascii_digit())
                .fold(container, span)
                .get_string()
                .parse()
                .unwrap();
            digits
        })
        .reduce(|x, y| x + y)
        .unwrap()
        .to_string();
    Ok(total)
}
    

const DIGITS: &'static str = "one
two
three
four
five
six
seven
eight
nine
1
2
3
4
5
6
7
8
9";

fn get_digit(line: &str, acc: FirstLast<char>) -> u32 {
    if line.len() == 0 {
        acc.get_string().parse().unwrap()
    } else {
        let found = DIGITS
            .lines()
            .filter(|d| line.starts_with(d))
            .next();
        let new_acc = match found {
            Some(x) => span(acc, parse_number(x)),
            None => acc
        };
        get_digit(&line[1..], new_acc)
    }
}

pub fn part2(_input: String) -> Result<String, error::Error> {
    let result = _input
        .lines()
        .map(|line| get_digit(line, FirstLast::Empty))
        .reduce(|x, y| x + y)
        .unwrap()
        .to_string();
    Ok(result)
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = "1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet".to_string();
        let result = part1(input);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "142")

    }
    #[test]
    fn test_part2() {
        let input = "two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen".to_string();
        let result = part2(input);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "281")
    }
    // #[test]
    // fn test_get_digit() {
    //     let input = "1three4twone";
    //     assert_eq!(get_digit(input, 11)

    // }

}