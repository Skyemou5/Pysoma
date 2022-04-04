use std::path::PathBuf;




struct Client {
    cwd: PathBuf,
    writer: Writer,
}

impl Client {
    fn new(writer: Writer) -> client {
        client {
            cwd: PathBuf::from("/"),
            writer,
        }
    }
}

#[async]
fn handle_cmd(mut self, cmd: Command) -> Result<Self> {
    println!("Received command: {:?}", cmd);
    match cmd {
        Command::Pwd => {
            let msg = format!("{}", self.cwd.to_str().unwrap_or(""));
            if !msg.is_empty() {
                let message = format!("\"/{}\" ", msg);
                self = await!(self

fn main() {
    println!("Hello, world!");
}
