use std::io;
use std::fmt;

#[derive(Debug)]
pub enum Error {
    FileNotFound(io::Error),
    NoSolution(ForDayPart)
}

#[derive(Debug, Clone)]
pub struct ForDayPart {
    day: u8,
    part: u8
}
impl ForDayPart {
    pub fn new(day: u8, part: u8) -> ForDayPart {ForDayPart { day, part }}
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match &self {
            Error::NoSolution(e) => 
                write!(f, "No solution found for day {} part {}", e.day, e.part),
            Error::FileNotFound(e) => 
                write!(f, "File read failed with: {}", e),
        }
    }
}