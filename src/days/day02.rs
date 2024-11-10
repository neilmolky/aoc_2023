use crate::error;
use std::cmp::max;

#[derive(PartialEq, Eq)]
enum Colour {
    Red,
    Green,
    Blue,
}

fn get_colour(s: &str) -> Colour {
    match s {
        "red" => Colour::Red,
        "blue" => Colour::Blue,
        "green" => Colour::Green,
        _ => panic!("not a colour {s}"),
    }
}

struct CubeCount {
    colour: Colour,
    count: u32,
}

impl CubeCount {
    fn build(pair: &str) -> CubeCount {
        let parts: Vec<&str> = pair.split(" ").collect();
        if parts.len() == 2 {
            let colour = get_colour(parts[1]);
            let count: u32 = parts[0].parse().expect(parts.join(", ").as_str());
            CubeCount { colour, count }
        } else {
            panic!("expected length 2 array, found [{}]", parts.join(", "))
        }
    }

    fn new(colour: &str, count: u32) -> CubeCount {
        let colour = get_colour(colour);
        CubeCount { colour, count }
    }

    fn fits_within(&self, other: &Handful) -> bool {
        other
            .cube_sets
            .iter()
            .filter(|other_item| self.colour == other_item.colour && self.count <= other_item.count)
            .next()
            .is_some()
    }
}

struct Bag {
    red: u32,
    green: u32,
    blue: u32,
}

impl Bag {
    fn new(red: u32, green: u32, blue: u32) -> Bag {
        Bag { red, green, blue }
    }

    fn empty_bag() -> Bag {
        Bag::new(0, 0, 0)
    }

    fn update(&self, c: &CubeCount) -> Bag {
        let mut blue = self.blue;
        let mut red = self.red;
        let mut green = self.green;
        match c.colour {
            Colour::Blue => blue = max(blue, c.count),
            Colour::Red => red = max(red, c.count),
            Colour::Green => green = max(green, c.count),
        }
        Bag { red, green, blue }
    }
}
struct Handful {
    cube_sets: Vec<CubeCount>,
}

impl Handful {
    fn build(segment: &str) -> Handful {
        let cube_sets: Vec<CubeCount> = segment.split(", ").map(CubeCount::build).collect();
        Handful { cube_sets }
    }
    fn new(cube_sets: Vec<CubeCount>) -> Handful {
        Handful { cube_sets }
    }

    fn is_contained_within(&self, other: &Handful) -> bool {
        self.cube_sets
            .iter()
            .all(|self_item| self_item.fits_within(other))
    }
}

struct Game {
    turns: Vec<Handful>,
}

impl Game {
    fn build(line: &str) -> Game {
        let turns: Vec<Handful> = line
            .split(": ")
            .last()
            .unwrap()
            .split("; ")
            .map(Handful::build)
            .collect();
        Game { turns }
    }
    fn smallest_possible_bag(&self) -> Bag {
        self.turns.iter().fold(Bag::empty_bag(), |bag, handful| {
            handful.cube_sets.iter().fold(bag, |acc, c| acc.update(c))
        })
    }
}

pub fn part1(input: String) -> Result<String, error::Error> {
    let bag = Handful::new(vec![
        CubeCount::new("red", 12),
        CubeCount::new("green", 13),
        CubeCount::new("blue", 14),
    ]);
    let sum_valid_game_idx = input
        .lines()
        .map(Game::build)
        .enumerate()
        .filter(|(_, g)| g.turns.iter().all(|t| t.is_contained_within(&bag)))
        .map(|(x, _)| x + 1)
        .sum::<usize>()
        .to_string();
    Ok(sum_valid_game_idx)
}

pub fn part2(input: String) -> Result<String, error::Error> {
    let result = input
        .lines()
        .map(Game::build)
        .map(|game| game.smallest_possible_bag())
        .map(|bag| bag.blue * bag.green * bag.red)
        .sum::<u32>()
        .to_string();
    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &'static str = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green";

    #[test]
    fn test_part1() {
        let input = INPUT.to_string();

        let result = part1(input);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "8")
    }
    #[ignore]
    #[test]
    fn test_part2() {
        let input = INPUT.to_string();
        let result = part1(input);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "2286")
    }
}
