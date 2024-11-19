use std::collections::HashMap;

use crate::error;

fn to_ints(s: &str) -> Vec<u32> {
    s
        .trim_ascii()
        .split_ascii_whitespace()
        .map(|x| x.parse().unwrap())
        .collect()
}

struct Card {
    winners: Vec<u32>,
    on_card: Vec<u32>
}
impl Card {
    fn build(line: (&str, &str)) -> Card {
        let winners = to_ints(line.0);
        let on_card = to_ints(line.1);
        Card { winners, on_card }
    }
    fn count_matches(&self) -> usize {
        self.on_card.clone().iter().filter(|n| self.winners.contains(n)).count()
    }

    fn score(&self) -> usize {
        let count_matches = self.count_matches();
        if count_matches == 0 {
            count_matches
        } else {
            2_usize.pow((count_matches as i32 - 1) as u32)
        }
    }
}

pub fn part1(input: String) -> Result<String, error::Error> {
    let total = input
        .lines()
        .map(|ln| ln.rsplit_once(':').unwrap().1.rsplit_once('|').unwrap())
        .map(|x | Card::build(x.into()))
        .map(|c| c.score())
        .sum::<usize>()
        .to_string();
    Ok(total.clone())
}

pub fn part2(input: String) -> Result<String, error::Error> {
    let cards: HashMap<usize, Card> = input
        .lines()
        .map(|ln| ln.rsplit_once(':').unwrap().1.rsplit_once('|').unwrap())
        .map(|x| Card::build(x.into()))
        .enumerate()
        .collect();
    let mut counter: HashMap<usize, usize> = HashMap::new();
    for card_no in 0..cards.len() {

        let multiple = counter.entry(card_no).or_insert(1).clone();
        let start = card_no + 1;
        let stop: usize = card_no + 1 + cards[&card_no].count_matches();
        for i in start..stop {
            counter.entry(i).and_modify(|v| {*v += multiple}).or_insert(1 + multiple);
        }
    }
    let total = counter
        .values()
        .fold(0, |x, y| x + y);
    Ok(total.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11";
    #[test]
    fn test_part1() {
        let input = INPUT.to_string();
        let result = part1(input);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "13")
    }
    #[test]
    fn test_part2() {
        let input = INPUT.to_string();
        let result = part2(input);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "30")
    }
}
