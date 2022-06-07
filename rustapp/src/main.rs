// use std::path::PathBuf;
use std::io;
// use std::env;
extern crate yaml_rust;
use yaml_rust::{YamlLoader, YamlEmitter};



fn yes_no_question(question: &str) {
    println!("{:?}",question);
    let mut answer = String::new();
    io::stdin().read_line(&mut answer).expect("error");
    println!("You entered {}", answer);
}


fn main() {
    //yes_no_question("this is a question")
    //println!("{:?}", std::env::current_exe());
}
